using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace z4
{
    public partial class ItemsForm1 : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            // Przechowujemy dane w Items dla tego żądania
            Context.Items["Message"] = "Przetwarzanie zakończone pomyślnie";
            Server.Transfer("ItemsForm2.aspx");
        }
    }
}