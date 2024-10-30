using System;
using System.IO;
using System.Linq;
using System.Web;
using System.Xml;

namespace z7
{
    public partial class WebForm1 : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {

        }

        protected void btnUpload_Click(object sender, EventArgs e)
        {
            if (Request.Files.Count > 0)
            {
                HttpPostedFile file = Request.Files[0];

                // dane pliku
                string fileName = Path.GetFileNameWithoutExtension(file.FileName);
                long fileSize = file.ContentLength;

                // sygnatura pliku
                byte[] fileBytes = new byte[fileSize];
                file.InputStream.Read(fileBytes, 0, (int)fileSize);
                int bytesum = fileBytes.Sum(b => b) % 0xFFFF;


                // Tworzenie XML-a
                XmlDocument xmlDoc = new XmlDocument();
                XmlElement root = xmlDoc.CreateElement("opis");
                xmlDoc.AppendChild(root);

                XmlElement nameElement = xmlDoc.CreateElement("nazwa");
                nameElement.InnerText = fileName;
                root.AppendChild(nameElement);

                XmlElement sizeElement = xmlDoc.CreateElement("rozmiar");
                sizeElement.InnerText = fileSize.ToString();
                root.AppendChild(sizeElement);

                XmlElement checksumElement = xmlDoc.CreateElement("sygnatura");
                checksumElement.InnerText = bytesum.ToString();
                root.AppendChild(checksumElement);

                string xmlContent = xmlDoc.OuterXml;

                // Zakodowanie nazwy pliku zgodznie z RFC 5987
                string encodedFileName = HttpUtility.UrlEncode(fileName) + ".xml";

                // Ustaw headery odpowiedzi
                Response.Clear();
                Response.ContentType = "application/xml";
                Response.AddHeader("Content-Disposition", $"attachment; filename=\"{fileName}.xml\"; filename*=UTF-8''{encodedFileName}");
                Response.Write(xmlContent);
                Response.End();
            }
        }
    }
}