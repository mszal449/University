using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace z4
{
    public class Foo
    {
        // Przykładowa właściwość klasy Foo
        public string Message { get; set; } = "Hello from Foo!";
    }


    public class ApplicationPseudosingleton
    {
        const string DATAKEY = "datakey";
        private static readonly object _lock = new object();


        public static Foo TheData
        {
            get
            {
                if (HttpContext.Current.Application[DATAKEY] == null)
                {
                    lock (_lock)
                    {
                        if (HttpContext.Current.Application[DATAKEY] == null)
                        {
                            Foo f = new Foo();
                            HttpContext.Current.Application[DATAKEY] = f;
                        }
                    }
                }

                return (Foo)HttpContext.Current.Application[DATAKEY];
            }
            
        }
    }

    
}