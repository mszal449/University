using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Security;
using System.Web.SessionState;

namespace z5
{
    public class Global : System.Web.HttpApplication
    {
        protected void Application_EndRequest()
        {
            var disposableObj = HttpContext.Current.Items["DataContext"] as IDisposable;
            disposableObj?.Dispose();
        }
    }
}