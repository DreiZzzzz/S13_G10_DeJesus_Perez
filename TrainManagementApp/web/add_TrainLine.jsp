<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@page import = "java.util.*, TrainManagement.*" %>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>ADD TRAIN LINE JSP</title>
    </head>
    <body>
        <form action="index.html">
            <jsp:useBean id="B" class= "TrainManagement.AddTrainLine" scope ="session" />
            <%
                String v_line_name = request.getParameter("line_name");
                String v_company_handler = request.getParameter("company_handler");
                String v_operational = request.getParameter("operational");

                B.line_name = v_line_name;
                B.company_handler = v_company_handler;
                B.is_operational = v_operational; 

                int status = B.register_AddTrainLine(); 

                if (status == 1) {
            %>
                   <h1>OPERATION SUCCESSFUL!</h1>
            <%   } else {
            %>     <h1>OPERATION FAILED!</h1>
            <% }
            %>
         <input type="submit" value="Return to Menu">
        </form>
    </body>
</html>
