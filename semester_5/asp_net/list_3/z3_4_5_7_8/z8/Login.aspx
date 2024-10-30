<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Login.aspx.cs" Inherits="z8.login" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
</head>
<body>
    <form id="form1" runat="server">
        <div>
            <asp:Label Text="Username: " runat="server" />
            <asp:TextBox ID="txtUsername" runat="server" />
            <br />
            <asp:Label Text="Password: " runat="server" />
            <asp:TextBox ID="txtPassword" runat="server" textMode="Password"/>
            <br />
            <asp:Button Text="Login" runat="server" OnClick="btnLogin_Click"/>
        </div>
    </form>
    <asp:Label ID="AlertLabel" Text="" runat="server" style="color: red;"/>

    <div>admin : password</div>
</body>
</html>
