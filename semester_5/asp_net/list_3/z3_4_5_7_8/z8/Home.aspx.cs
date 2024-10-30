using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace z8
{
    public partial class Home : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (Context.Session["Auth"] == null)
            {
                // Store the current request URL as the returnUrl parameter
                string returnUrl = HttpUtility.UrlEncode(Request.RawUrl);
                Response.Redirect($"/login.aspx?returnUrl={returnUrl}");
            }
        }

        protected void btnLogout_Click(object sender, EventArgs e)
        {
            if (Context.Session["Auth"] != null)
            {
                Context.Session["Auth"] = null;
            }
            Response.Redirect(Request.RawUrl);
        }
    }
}