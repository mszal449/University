using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace z4
{
    public partial class WebForm1 : Page
    {

        protected void Page_Load(object sender, EventArgs e)
        {
            Application.Lock();
            Application["VisitCount"] = (int)Application["VisitCount"] + 1;
            Application.UnLock();

            Label1.Text = "Liczba odwiedzin: " + Application["VisitCount"].ToString();
        }
    }
}