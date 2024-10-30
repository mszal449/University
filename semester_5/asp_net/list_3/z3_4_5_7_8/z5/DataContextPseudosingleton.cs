using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Diagnostics;
using System.Linq;
using System.Web;

namespace z5
{
    public class DataContextPseudosingleton
    {
        
        public static MockDatabase Instance
        {
            get
            {
                if (HttpContext.Current.Items["DataContext"] == null)
                {
                    HttpContext.Current.Items["DataContext"] = new MockDatabase();
                }

                return (MockDatabase)HttpContext.Current.Items["DataContext"];
            }
        }

        public static void Dispose()
        {
            var connection = HttpContext.Current.Items["DatContext"] as MockDatabase;
            if (connection != null)
            {
                connection.Dispose();
                HttpContext.Current.Items.Remove("DataContext");
            }
        }
    }

    public class MockDatabase : IDisposable
    {
        public string ReadString()
        {
            return "Reading data from the database...";
        }

        public void Dispose()
        {
            Debug.WriteLine("MockDatabase disposed.");
        }
    }

}