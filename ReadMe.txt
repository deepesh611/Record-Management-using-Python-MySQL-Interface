

                                        RECORD MANAGEMENT APPLICATION

This is a basic python program made for workers in management fields. Please read the ' PRE-REQUISITS ' mentioned below. 



PRE-REQUISITS  :- Before running the program, download 
                  'Windows(x86, 32-bit), MSI Installer (mysql-installer-community-8.0.33.0.msi)' 
                  from the link given below.

                   https://dev.mysql.com/downloads/installer/


               :- After installing MySQL, set the password, and install the MySQL-Python Connector
                  using the link given below
                  
                   https://dev.mysql.com/downloads/connector/python/
                  

               :- Now you have to install Python(3.11.4)-[Windows installer (64-bit)/ (32-bits)]according to your OS.

                  https://www.python.org/downloads/release/python-3114/

	       
	       :- Now you have to create two separate excel files, one from which you want to store the data and
		  another one to which you want to add the searched data. The data in the first excel file should
                  be in the same order, along with the column names in same order

                   (Part No,Description,Quantity,Bin location,Price,Net Price,Discount,Gross Price)
		
		  The second excel file should be left blank. Just create the file without adding any data.


               :- After the above installations are done, run the file 'OneTimeRun.py', and Enter your MySQL password and the
                  location of the excel file in it. Remember, the location and password should not change, and if they do, you
                  will have to run this file again and reset the password and path. 


               :- Now You can run the main application 'Record management.py'. 
                  It is suggested to create a shortcut of the file in the desktop, and open it with 'Python Runner', rather than a code editor. 
                  Follow instructions : (Right Click on the 'Record Management.py', 'Show more options', 'create shortcut')
                  Now you can drag that shortcut to the desktop

                  Don't forget to change the Password.




This is a menu driven program, which begins with password checking to ensure that the correct user is 
accessing the file. The preset password is 'admin', and the user is requested to set a new password when 
they first use this program. The user can change the password using the 'change password' option in the 
menu available in the application.

