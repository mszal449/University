using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace z3
{
    public partial class WebForm1 : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            // Odczytywanie nagłówków żądania
            foreach (string headerKey in Request.Headers)
            {
                string headerValue = Request.Headers[headerKey];
                Response.Write($"Nagłówek: {headerKey} - Wartość: {headerValue}<br/>");
            }

            // Tworzenie własnego nagłówka odpowiedzi
            Response.Headers.Add("X-Custom-Header", "WlasnaWartosc");

            // Mapowanie ścieżki względnej na ścieżkę fizyczną
            string relativePath = "~/example/path"; // Przykład ścieżki względnej
            string physicalPath = Server.MapPath(relativePath);
            Response.Write($"Ścieżka fizyczna dla '{relativePath}' to: {physicalPath}<br/>");
        }
    }
}