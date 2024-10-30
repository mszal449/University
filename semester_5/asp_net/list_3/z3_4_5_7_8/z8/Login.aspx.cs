using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace z8
{
    public partial class login : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (Context.Session["Auth"] != null)
            {
                Response.Redirect("/home");
            }

            // store original return 
            if (!IsPostBack && Request.QueryString["returnUrl"] != null)
            {
                Context.Session["ReturnUrl"] = Request.QueryString["returnUrl"];
            }
        }

        protected void btnLogin_Click(object sender, EventArgs e)
        {
            string username = txtUsername.Text;
            string password = txtPassword.Text;

            if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(password))
            {
                AlertLabel.Text = "Password and username values are required.";
                return;
            }

            if (isValidUser(username, password))
            {
                Context.Session["Auth"] = true;

                // Redirect to the original request URL or home page
                string returnUrl = Context.Session["ReturnUrl"] as string;
                if (!string.IsNullOrEmpty(returnUrl))
                {
                    // Clear the ReturnUrl from the session after redirecting
                    Context.Session.Remove("ReturnUrl");
                    Response.Redirect(returnUrl);
                }
                else
                {
                    Response.Redirect("/"); // Default redirect
                }
            }
            else
            {
                Context.Session["Auth"] = null;
                AlertLabel.Text = "Invalid username or password.";
            }

        }

        private bool isValidUser(string username, string password)
        {
            if (username == "admin" && password == "password") return true;
            return false;
        }
    }
}