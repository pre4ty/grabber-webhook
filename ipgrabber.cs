using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace cipacipafilip
{
    class ipgrabber
    {
        public static string GetIP()
        {
            string ip = new WebClient().DownloadString("https://api.ipify.org");
            return ip;
        }
    }
}
