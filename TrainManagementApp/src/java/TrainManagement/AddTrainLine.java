package TrainManagement;

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */


import java.util.*; 
import java.sql.*; 

public class AddTrainLine {
    // fields of train line
    public int train_line_id;
    public String line_name; 
    public String company_handler; 
    public String is_operational;
    
    // list of train line
    public ArrayList<Integer> list_trainLineID       = new ArrayList<>();
    public ArrayList<String> list_lineName           = new ArrayList<>();
    public ArrayList<String> list_company_handler    = new ArrayList<>();
    public ArrayList<String> list_isOperational     = new ArrayList<>(); // 0 - false, 1 - true
    
    // empty constructor
    public AddTrainLine() {
    
    }
    
    public int register_AddTrainLine() {
       int temp = -1; 
       
       try {
            // Load MySQL JDBC Driver
            Class.forName("com.mysql.cj.jdbc.Driver");
            
            // connect to database
            Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/dbtrains", "root", "Dlsuid12343080#");
            System.out.println("Connection successful!");
            
            // Use the connection (e.g., create a statement, execute queries, etc.)
            
            PreparedStatement psmt = conn.prepareStatement("SELECT MAX(train_line_id) + 1 AS newID FROM train_lines");
            ResultSet rst = psmt.executeQuery();
            
            while(rst.next()) {
                train_line_id = rst.getInt("newID");
            }
            
            psmt = conn.prepareStatement("INSERT INTO train_lines(train_line_id, line_name, company_handler, is_operational) VALUES(?, ?, ?, ?)");
            psmt.setInt(1, train_line_id); 
            psmt.setString(2,line_name);
            psmt.setString(3, company_handler); 
            
            if (is_operational.toLowerCase().equals("true")) {
                temp = 1; 
            } else if (is_operational.toLowerCase().equals("false")) {
                temp = 0; 
            }
            psmt.setInt(4, temp); 
            
            psmt.executeUpdate();
            
            psmt.close();
            conn.close(); // close connection
            
            return 1; // if success
        } catch (ClassNotFoundException e) {
            System.out.println("MySQL JDBC Driver not found: " + e.getMessage());
        } catch (SQLException e) {
            System.out.println("SQL Exception: " + e.getMessage());
        }
        
        return 0; // if failure
    }

} 