using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace z4
{
    public partial class SessionForm2 : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                if (Session["Username"] != null)
                {
                    Label1.Text = "Witaj " + Session["Username"].ToString();
                } else
                {
                    Label1.Text = "Nie jesteś zalogowany";
                }
            }
        }
    }
}