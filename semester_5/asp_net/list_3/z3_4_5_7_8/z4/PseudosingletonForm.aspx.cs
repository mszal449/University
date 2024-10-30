using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace z4
{
    public partial class PseudosingletonForm : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            Foo myFoo = ApplicationPseudosingleton.TheData;

            Label1.Text = myFoo.Message;
        }
    }
}