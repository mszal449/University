<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="SessionForm1.aspx.cs" Inherits="z4.SessionForm1" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
</head>
<body>
    <form id="form1" runat="server">
        <div>
            <h1>Type username here</h1>
            <asp:TextBox ID="Username" runat="server"></asp:TextBox>
            <asp:Button Text="Login" runat="server" OnClick="LoginButton_Click" />
        </div>
    </form>
</body>
</html>
