<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs" Inherits="z7.WebForm1" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
</head>
<body>
    <form id="form1" runat="server" enctype="multipart/form-data">
        <h2>Upload file:</h2>
        <input type="file" name="fileInput" value="" />
        <asp:Button ID="btnUpload" runat="server" Text="Prześlij" OnClick="btnUpload_Click" />
    </form>
</body>
</html>
