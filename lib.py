
import mysql.connector as mys
import pickle
import emoji
import pwinput
import time
import pandas as pd
from sqlalchemy import create_engine
import warnings
import openpyxl




g = open('satapwd2.dat','rb')
sql_pwd=pickle.load(g)
g.close()

g = open('path1.dat','rb')
xlsx_path1 = pickle.load(g)
g.close()

g = open('path2.dat','rb')
xlsx_path2 = pickle.load(g)
g.close()

g = open('name.dat','rb')
name=pickle.load(g)
g.close()


def check():
    f = open(r'C:\Users\deepe\OneDrive\Desktop\Codings\Record Management\pwd.dat','rb')
    data = pickle.load(f)
    p = pwinput.pwinput(prompt ="\nENTER PASSWORD :\n", mask="*")
    print()
    if p == data:
        pass
    else:
        print('INVALID PASSWORD !') 
        print('   ',(emoji.emojize(":pensive_face:"))*3)
        time.sleep(5)
        quit()
        
        
        
def cng_pwd():
    o = pwinput.pwinput(prompt ="ENTER PREVIOUSLY SET PASSWORD :\n", mask="*")
    print()
    f = open(r'C:\Users\deepe\OneDrive\Desktop\SATA2\satapwd.dat','rb')
    data = pickle.load(f)
    f.close()
    if o == data:
        f = open(r'C:\Users\deepe\OneDrive\Desktop\SATA2\satapwd.dat','wb')
        p = pwinput.pwinput(prompt ="ENTER THE NEW PASSWORD :\n", mask="*")
        print()
        pickle.dump(p,f)
        print('Password was Successfully Changed.\n')
        f.close()
    else:
        print('INVALID PASSWORD !')
        print('   ',(emoji.emojize(":pensive_face:"))*3,'\n')
        pass
    time.sleep(2)



def add():
    sata=mys.connect(host='localhost',user='root',passwd=sql_pwd,database='sata')
    cursor = sata.cursor()
    ans = 'y'
    
    while ans == 'y':
        no = input('Enter Part No. :\n')
        cursor.execute("select * from data where partno like '{0}'".format(no))
        data = cursor.fetchall()
        if data == []:
            name = input("Enter Part Name :\n")
            qty = float(input("Enter Quantity :\n"))
            price = float(input("Enter Price per Piece :\n"))
            disc = float(input("Enter Discount Percent :\n"))  
            loc = input('Enter Location :\n')      
            cursor.execute("insert into data values ('{0}','{1}',{2},'{3}',{4},{5},{6},{7})".format(no,name,qty,loc,price,price*qty,disc,(price*qty)-((price*qty)*(disc/100))))
            sata.commit()
        else:
            print("\nThis Item already exists in the list.\n")
            time.sleep(2)
            qty = int(input("Enter New Quantity :\n"))
            price = float(input("Enter Price per Piece :\n"))
            disc = float(input("Enter Discount Percent :\n"))
            loc = input('Enter Loaction :\n')
            for a,b,c,d,e,f,g,h in data:
                cursor.execute("update data set qty={0} where partno = '{1}'".format(c+qty,no))
                cursor.execute("update data set price = {0} where partno = '{1}'".format(price,no))
                cursor.execute("update data set loc = '{0}' where partno = '{1}'".format(loc,no))
                cursor.execute("update data set net = {0} where partno = '{1}'".format(price*(c+qty),no))
                cursor.execute("update data set disc = {0} where partno = '{1}'".format(disc,no))
                cursor.execute("update data set gross = {0} where partno = '{1}'".format((price*(c+qty))-((price*(c+qty))*(disc/100)),no))
            sata.commit()
            
        print('\nRecord Added.\n')
        time.sleep(1)
        ans = input("Add More \n(Y/N) : ")
        ans = ans.lower()
        
    sata.close()



def delete():
    sata=mys.connect(host='localhost',user='root',passwd=sql_pwd,database='sata')
    cursor = sata.cursor()
    
    ans = 'y'
    while ans == 'y':
        partno = input('Enter Part No.:\n')
        cursor.execute("select * from data where partno = '{0}'".format(partno))
        data = cursor.fetchall()
        
        if data == []:
            print('Record Not Found.\n')
            time.sleep(1)
        else:
            cursor.execute("delete from data where partno = '{0}'".format(partno))
            sata.commit()
            print('Record Deleted.\n')
            time.sleep(1)
            
        ans = input('Delete More ?\n[Y/N] :')
        ans=ans.lower()
        print()
        if ans == 'n' or ans == 'y':
            continue
        else:
            print('INVALID INPUT !\n')
            
    sata.close()
    
    

def search():
    
    sata=mys.connect(host='localhost',user='root',passwd=sql_pwd,database='sata')
    cursor = sata.cursor()
    ans = 'y'
    
    while ans == 'y':
        partno = input('Enter Part No.:\n')
        print()
        cursor.execute("select * from data where partno like '%{0}%'".format(partno))
        data = cursor.fetchall()
        
        if data == []:
            print('Record Not Found.\n')
        else:
            print('PART NO','\t\tNAME','\t\t\tQUANTITY','LOCATION','PRICE\t','NET_PRICE','DISCOUNT(%)','GROSS_PRICE',sep = '\t')
            print('-'*150)
            
            for a,b,c,d,e,f,g,h in data:
                if len(a)<=7:
                    if b is None or len(b)<=7:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                print(a,'','',b,'','','',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                            else:
                                print(a,'','',b,'','','',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                print(a,'','',b,'','','',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                            else:
                                print(a,'','',b,'','','',c,'',d,e,f,'',g,'',h,sep = '\t')
                    
                    elif len(b)>23:
                        if d is None or len(d)<=7 :
                            if e is None or len(str(e))<=7:
                                print(a,'','',b,c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                            else:
                                print(a,'','',b,c,'',d,'',e,f,'',g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                print(a,'','',b,c,'',d,e,'',f,'',g,'',h,sep = '\t')
                            
                            else:
                                print(a,'','',b,c,'',d,e,f,'',g,'',h,sep = '\t')
                    
                    elif len(b)>=16:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                print(a,'','',b,'',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                            else:
                                print(a,'','',b,'',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                print(a,'','',b,'',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                            
                            else:
                                print(a,'','',b,'',c,'',d,'',e,f,'',g,'',h,sep = '\t')     
                    
                    else:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                print(a,'','',b,'',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                            else:
                                print(a,'','',b,'',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                print(a,'','',b,'',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                            
                            else:
                                print(a,'','',b,'',c,'',d,'',e,f,'',g,'',h,sep = '\t')                  
                        
                elif len(a)>=16:
                    if b is None or len(b)<=7:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                print(a,b,'','','','',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                            else:
                                print(a,b,'','','','',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                print(a,b,'','','','',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                            else:
                                print(a,b,'','','','',c,'',d,e,f,'',g,'',h,sep = '\t')  
                    
                    
                    elif len(b)>23:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                print(a,b,c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                            else:
                                print(a,b,c,'',d,'',e,f,'',g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                print(a,b,c,'',d,e,'',f,'',g,'',h,sep = '\t')
                            
                            else:
                                print(a,b,c,'',d,e,f,'',g,'',h,sep = '\t')
                    
                    
                    elif len(b)>=16:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                print(a,b,'',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                            
                            else:
                                print(a,b,'',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                print(a,b,'',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                            
                            else:
                                print(a,b,'',c,'',d,e,f,'',g,'',h,sep = '\t')
                                
                    else:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                print(a,b,'','',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                            
                            else:
                                print(a,b,'','',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                print(a,b,'',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                            
                            else:
                                print(a,b,'',c,'',d,e,f,'',g,'',h,sep = '\t')
                
                else:
                    if b is None or len(b)<8:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                print(a,'',b,'','','',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                            
                            else:
                                print(a,'',b,'','','',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                print(a,'',b,'','','',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                            
                            else:
                                print(a,'',b,'','','',c,'',d,e,f,'',g,'',h,sep = '\t')
                    
                    elif len(b)>23 and len(b)<=30:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                print(a,'',b,c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                            
                            else:
                                print(a,'',b,c,'',d,'',e,f,'',g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                print(a,'',b,c,'',d,e,'',f,'',g,'',h,sep = '\t')
                            
                            else:
                                print(a,'',b,c,'',d,e,f,'',g,'',h,sep = '\t')
                    
                    
                    elif len(b)>=16:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                print(a,'',b,'',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                            
                            else:
                                print(a,'',b,'',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                print(a,'',b,'',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                            else:
                                print(a,'',b,'',c,'',d,e,f,'',g,'',h,sep = '\t')
                        
                    else:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'',b,'','',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                                
                                else:
                                    print(a,'',b,'','',c,'',d,'',e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,'',b,'','',c,'',d,'','',e,f,'',g,'',h,sep = '\t')
                                
                                else:
                                    print(a,'',b,'','',c,'',d,'','',e,f,g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'',b,'','',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,'','',c,'',d,e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,'',b,'','',c,'',d,e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,'','',c,'',d,e,f,g,'',h,sep = '\t')
                        
                        
            time.sleep(2)
            input("\nPress Enter to Continue.")
            print()
            
            rep = input('Do you Wish to add the record(s) to the excel file ?\n[Y/N] :')
            rep=rep.lower()
            
            if rep == 'y':
                warnings.filterwarnings("ignore", category=UserWarning)
                query=f"select * from data where partno like '%{partno}%'"
                data = pd.read_sql(query,sata)
                sata.close()
                existing_data = pd.read_excel(xlsx_path2)  
                comb_data = existing_data._append(data,ignore_index=True)
                comb_data.to_excel(xlsx_path2, index = False)
                
                print("\nRecord Copied\n   \U0001F44D\U0001F44D\U0001F44D\n")
                time.sleep(1)
                
            else:
                print('\nOk\n')
                pass
        
        ans = input('\nSearch More ?\n[Y/N] :')
        ans=ans.lower()
        print()
        
        if ans == 'n' or ans == 'y':
            continue
        else:
            print('INVALID INPUT !\n')
            
    sata.close()
    
    
    
def edit():
    sata=mys.connect(host='localhost',user='root',passwd=sql_pwd,database='sata')
    cursor = sata.cursor()
    ans = 'y'
    while ans == 'y':
        
        partno = input('Enter Part no.:\n')
        cursor.execute("select * from data where partno = '{0}'".format(partno))
        data = cursor.fetchall()
        
        if data == []:
            print('Record Not Found.\n')
            time.sleep(1)
            rep=input("Do You Wish to Add it as a New Item ?\n[Y/N] : ")
            rep=rep.lower()
            
            if rep == 'y':
                print('Ok\n')
                time.sleep(0.5)
                add()
            else:
                print('Ok\n')
                time.sleep(0.5)
                pass
            
        else:
            qty = int(input('Enter New Quantity:\n'))
            name = input("Enter Item Name : \n")
            price = float(input('Enter New Price :\n'))
            disc = float(input("Enter New Discount :\n"))
            loc = input('Enter Loaction :\n')
            cursor.execute("update data set qty = {0} where partno = '{1}'".format(qty,partno))
            cursor.execute("update data set name = '{0}' where partno = '{1}'".format(name,partno))
            cursor.execute("update data set price = {0} where partno = '{1}'".format(price,partno))
            cursor.execute("update data set net = {0} where partno = '{1}'".format(price*qty,partno))
            cursor.execute("update data set loc = '{0}' where partno = '{1}'".format(loc,partno))
            cursor.execute("update data set gross = {0} where partno = '{1}'".format((price*qty)-((price*qty)*(disc/100)),partno))
            cursor.execute("update data set disc = {0} where partno = '{1}'".format(disc,partno))
            sata.commit()
            
            print('\nRecord Edited.\n')
            time.sleep(1)
            
        ans = input('Edit More ?\n[Y/N] :')
        ans=ans.lower()
        print()
        if ans == 'n' or ans == 'y':
            continue
        else:
            print('INVALID INPUT !\n')
            
    sata.close()
    
    

def display():
    sata=mys.connect(host='localhost',user='root',passwd=sql_pwd,database='sata')
    cursor = sata.cursor()
    cursor.execute('select*from data')
    data = cursor.fetchall()
    
    if data == []:
        print('The List is Empty.\n')
        time.sleep(1)
    else:
        print('PART NO','\t\tNAME','\t\t\tQUANTITY','LOCATION','PRICE\t','NET_PRICE','DISCOUNT(%)','GROSS_PRICE',sep = '\t')
        print('-'*150)
        
        for a,b,c,d,e,f,g,h in data:
                if len(a)<=7:
                    if b is None or len(b)<=7:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'','',b,'','','',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,'','','',c,'',d,'',e,'',f
                                          ,g,'',h,sep = '\t')
                            else:
                                if len(str(f))<=7:
                                    print(a,'','',b,'','','',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,'','','',c,'',d,'',e,f,g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'','',b,'','','',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,'','','',c,'',d,e,'',f,g,'',h,sep = '\t')
                            else:
                                if len(str(f))<=7:
                                    print(a,'','',b,'','','',c,'',d,e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,'','','',c,'',d,e,f,g,'',h,sep = '\t')
                    
                    elif len(b)>23:
                        if d is None or len(d)<=7 :
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'','',b,c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,c,'',d,'',e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,'','',b,c,'',d,'',e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,c,'',d,'',e,f,g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'','',b,c,'',d,e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,c,'',d,e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,'','',b,c,'',d,e,f,g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,c,'',d,e,f,'',g,'',h,sep = '\t')
                    
                    elif len(b)>=16:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'','',b,'',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,'',c,'',d,'',e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,'','',b,'',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,'',c,'',d,'',e,f,g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'','',b,'',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,'',c,'',d,e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,'','',b,'',c,'',d,e,f,'',g,'',h,sep = '\t')     
                                else:
                                    print(a,'','',b,'',c,'',d,e,f,g,'',h,sep = '\t')     
                    
                    else:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'','',b,'','',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,'','',c,'',d,'',e,'',f,g,'',h,sep = '\t')
                            else:
                                if len(str(f))<=7:
                                    print(a,'','',b,'','',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,'','',c,'',d,'',e,f,g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'','',b,'','',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,'','',c,'',d,e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,'','',b,'','',c,'',d,e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'','',b,'','',c,'',d,e,f,g,'',h,sep = '\t')                  
                        
                elif len(a)>=16:
                    if b is None or len(b)<=7:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,b,'','','',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,b,'','','',c,'',d,'',e,'',f,g,'',h,sep = '\t')
                            else:
                                if len(str(f))<=7:
                                    print(a,b,'','','','',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,b,'','','','',c,'',d,'',e,f,g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,b,'','','',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,b,'','','',c,'',d,e,'',f,g,'',h,sep = '\t')
                            else:
                                if len(str(f))<=7:
                                    print(a,b,'','','','',c,'',d,e,f,'',g,'',h,sep = '\t')  
                                else:
                                    print(a,b,'','','','',c,'',d,e,f,g,'',h,sep = '\t')  
                    
                    
                    elif len(b)>23:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,b,c,'',d,'',e,'',f,'',g,'',h,sep = '\t')  
                                else:
                                    print(a,b,c,'',d,'',e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,b,c,'',d,'',e,f,'',g,'',h,sep = '\t') 
                                else:
                                    print(a,b,c,'',d,'',e,f,g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,b,c,'',d,e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,b,c,'',d,e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,b,c,'',d,e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,b,c,'',d,e,f,g,'',h,sep = '\t')
                    
                    
                    elif len(b)>=16:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,b,'',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,b,'',c,'',d,'',e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,b,'',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,b,'',c,'',d,'',e,f,g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,b,'',c,'',d,e,'',f,'',g,'',h,sep = '\t')  
                                else:
                                    print(a,b,'',c,'',d,e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,b,'',c,'',d,e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,b,'',c,'',d,e,f,g,'',h,sep = '\t')
                                
                    else:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,b,'','',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,b,'','',c,'',d,'',e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,b,'','',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,b,'','',c,'',d,'',e,f,g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,b,'','',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,b,'','',c,'',d,e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,b,'',c,'',d,e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,b,'',c,'',d,e,f,g,'',h,sep = '\t')
                
                else:
                    if b is None or len(b)<8:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'',b,'','','',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,'','','',c,'',d,'',e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,'',b,'','','',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                                
                                else:
                                    print(a,'',b,'','','',c,'',d,'',e,f,g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'',b,'','','',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,'','','',c,'',d,e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,'',b,'','','',c,'',d,e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,'','','',c,'',d,e,f,g,'',h,sep = '\t')
                    
                    elif len(b)>23 and len(b)<=30:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'',b,c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,c,'',d,'',e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,'',b,c,'',d,'',e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,c,'',d,'',e,f,g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'',b,c,'',d,e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,c,'',d,e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,'',b,c,'',d,e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,c,'',d,e,f,g,'',h,sep = '\t')
                                       
                    elif len(b)>=16:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'',b,'',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,'',c,'',d,'',e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,'',b,'',c,'',d,'',e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,'',c,'',d,'',e,f,g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'',b,'',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,'',c,'',d,e,'',f,g,'',h,sep = '\t')
                            else:
                                if len(str(f))<=7:
                                    print(a,'',b,'',c,'',d,e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,'',c,'',d,e,f,g,'',h,sep = '\t')
                        
                    else:
                        if d is None or len(d)<=7:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'',b,'','',c,'',d,'',e,'',f,'',g,'',h,sep = '\t')
                                
                                else:
                                    print(a,'',b,'','',c,'',d,'',e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,'',b,'','',c,'',d,'','',e,f,'',g,'',h,sep = '\t')
                                
                                else:
                                    print(a,'',b,'','',c,'',d,'','',e,f,g,'',h,sep = '\t')
                        
                        else:
                            if e is None or len(str(e))<=7:
                                if len(str(f))<=7:
                                    print(a,'',b,'','',c,'',d,e,'',f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,'','',c,'',d,e,'',f,g,'',h,sep = '\t')
                            
                            else:
                                if len(str(f))<=7:
                                    print(a,'',b,'','',c,'',d,e,f,'',g,'',h,sep = '\t')
                                else:
                                    print(a,'',b,'','',c,'',d,e,f,g,'',h,sep = '\t')
    
    
        time.sleep(2)
        input("\nPress Enter to Continue.")
        
   
    
def menu():
    try:
        txt1 = 'MENU'
        print( '\n',txt1.center(40,'~'))
        print()
        print(' 1 : ADD A RECORD')
        print(' 2 : DELETE A RECORD')
        print(' 3 : SEARCH A RECORD')
        print(' 4 : EDIT A RECORD')
        print(' 5 : DISPLAY PRICE DETAILS')
        print(' 6 : COPY ALL DATA TO EXCEL')
        print(' 7 : CHANGE PASSWORD')
        print(' 8 : EXIT')
        print()
        
        chc=int(input("ENTER YOUR CHOICE (1-7):\n"))
        print()
        if chc==1:
            add()
        elif chc==2:
            delete()
        elif chc==3:
            search()
        elif chc==4:
            edit()
        elif chc == 5:
            display()
        elif chc == 6:
            copy_all_data_to_excel()
        elif chc == 7:
            cng_pwd()
        elif chc == 8:
            rename_xlsx()
            print('ALL THE CHANGES ARE SUCCESSFULLY SAVED.\n')
            print('\t      \U0001F600\U0001F600\U0001F600\n')
            time.sleep(3)
            quit()
        else:
            print("You have Given a Wrong Input.\n")
            time.sleep(1)
        print()
        
    except ValueError:
        print("\nINVALID INPUT !\n")
        time.sleep(2)



def intro():
    cent = 100
    txt1 = time.ctime()
    new_str = txt1.center(cent, '-')
    print('\n',new_str)
    print()
    time.sleep(0.5)
    print('\t\t\t\t\tWELCOME, ',name,'!\n')
    time.sleep(0.5)
    print()
    print("*"*101)
    print("**                                                                                                 **")
    print("**                         WELCOME TO THE RECORD MANAGEMENT APPLICATION.                           **")
    print("**                                                                                                 **")
    print("*"*101,'\n')
    time.sleep(2)
    
    
    
def show_loading_animation():
    animation = "|/-\\"
    i = 0
    while flag:
        print(f"\tUpdating Database...  {animation[i % len(animation)]}", end="\r")
        i += 1
        time.sleep(0.1)

   
   
def copy_all_data_to_sql():
    
    sata=mys.connect(host='localhost',user='root',passwd=sql_pwd,database='sata')
    cursor = sata.cursor()
    cursor.execute('delete from data')
    sata.commit()
    
    df = pd.read_excel(xlsx_path1)
    db_connection_string = 'mysql://root:'+sql_pwd+'@localhost:3306/sata'
    
    db_engine = create_engine(db_connection_string)
    df.to_sql('data', con=db_engine, if_exists='replace', index=False)
    
    db_engine.dispose()

    cursor.execute('alter table data rename column `part no.` to partno')
    cursor.execute('alter table data rename column Description to name')
    cursor.execute('alter table data rename column Quantity to qty')
    cursor.execute('alter table data rename column `Bin Location` to loc')
    cursor.execute('alter table data rename column discount to disc')
    cursor.execute('alter table data rename column `gross price` to gross')
    cursor.execute('alter table data modify column total decimal(10,3)')
    cursor.execute('alter table data modify column gross decimal(10,3)')
    cursor.execute('alter table data modify column qty int')
    sata.commit()
    
    cursor.execute('update data set disc = 0 where disc is null')
    cursor.execute('update data set total = (price*qty)')
    cursor.execute('update data set gross = (total-(total*(disc/100)))')
    sata.commit()

    global flag
    flag = False
    
 

def copy_all_data_to_excel():
    
    warnings.filterwarnings("ignore", category=UserWarning)
    sata=mys.connect(host='localhost',user='root',passwd=sql_pwd,database='sata')
    data = pd.read_sql_query('select * from data',sata)
    sata.close()
    
    
    data.to_excel(xlsx_path2,index = False)
    print('\nData Copied\n  \U0001F44D\U0001F44D\U0001F44D')
    time.sleep(1)
    


def reset_xlsx():
    
    wb = openpyxl.load_workbook(xlsx_path2)
    sheet = wb.active
    sheet.delete_rows(1, sheet.max_row)
    wb.save(xlsx_path2)
    wb.close()



def rename_xlsx():
    
    df = pd.read_excel(xlsx_path2)
    column_mapping = {'partno': 'Part No.','name': 'Description','qty': 'Quantity','loc': 'Bin Location',
                    'price': 'Price','net' : 'Net Price', 'disc': 'Discount','gross': 'Gross Price'}
    df = df.rename(columns=column_mapping)
    df.to_excel(xlsx_path2, index=False)
