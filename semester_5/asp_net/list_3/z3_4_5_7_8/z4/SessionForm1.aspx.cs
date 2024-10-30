using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace z4
{
    public partial class SessionForm1 : System.Web.UI.Page
    {
        protected void LoginButton_Click(object sender, EventArgs e)
        {
            Session["Username"] = Username.Text;
            Response.Redirect("SessionForm2.aspx");
        }
    }
}