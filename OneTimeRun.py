
import pickle
import time
import mysql.connector as mys
import lib

lib.check()

def set():
    
    name = input('\nEnter Your Name:\n')
    password=input("\nEnter the MySQL Password :\n")
    path1 = input("\nEnter the Path of the Excel File You wish to Copy Data from:\n")
    path2 = input("\nEnter the path of the Excel file in which you want the Searched data to be stored :\n")
    
    f1 = open('satapwd2.dat','wb')
    f2 = open('path1.dat','wb')
    f3 = open('path2.dat','wb')
    f4 = open('name.dat','wb')
    pickle.dump(password,f1)
    pickle.dump(path1,f2)
    pickle.dump(path2,f3)
    pickle.dump(name,f4)
    f1.close()
    f2.close()
    f3.close()
    f4.close()
    
    sata = mys.connect(host='localhost',user='root',passwd=password)
    cursor=sata.cursor()
    cursor.execute('create database satallc')
    sata.close()
    
    sata = mys.connect(host='localhost',user='root',passwd=password,database='satallc')
    cursor=sata.cursor()
    cursor.execute('create table data(partno text, name text, qty int, loc text, price float,net float,disc float, gross float)')
    sata.close()
    
    print('\nData Stored ! \U0001F44D')
    time.sleep(1)
    
set()