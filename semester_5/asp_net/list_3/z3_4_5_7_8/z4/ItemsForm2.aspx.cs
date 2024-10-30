using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace z4
{
    public partial class ItemsForm2 : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (Context.Items["Message"] != null)
            {
                Label1.Text = Context.Items["Message"].ToString();
            }
        }
    }
}