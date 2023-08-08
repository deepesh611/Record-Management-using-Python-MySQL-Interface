
import lib
import threading


lib.check()
lib.reset_xlsx()
lib.intro()

    
n=input("Are There Any To be Updated in the Database ?\n[Y/N] : ")
n=n.lower()
if n=='y':
    lib.flag = True
    thread = threading.Thread(target=lib.copy_all_data_to_sql)
    thread.start()
    print()
    lib.show_loading_animation()
    thread.join()
    lib.flag = False
    lib.time.sleep(0.5)
    print('The Data has been Updated.          \n\t\U0001F44D\U0001F44D')
else:
    print('OK\n')

while True:
    lib.menu()
