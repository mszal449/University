<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs" Inherits="z5.WebForm1" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
</head>
<body>
    <form id="form1" runat="server">
        <div>
            <h1>Przechowywanie w Application: Dzielone połączenie z innymi użytkownikami, problemy z bezpieczeństwem.</h1>
            <h1>Przechowywanie w Session: Problem z zasobami - połączenei może istnieć nawet gdy użytkownik nie jest aktywny, ale sesja dalej trwa</h1>
            <h1>Przechowywanie w Items: Odpowiednie rozwiązanie</h1>

            <div>
                <asp:Label ID="Label1" runat="server" Text="Data from Database:"></asp:Label>
                <asp:Literal ID="Literal1" runat="server"></asp:Literal>
                <br />
                <asp:Button ID="Button1" runat="server" Text="Load Data" OnClick="Button1_Click" />
            </div>
        </div>
    </form>
</body>
</html>
