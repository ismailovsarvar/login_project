import threading

import db
import models as m2
from service import login


def user_login():
    try:
        if db:
            while True:
                print('\n1. Sign Up'
                      '\n2. Log In'
                      '\n3. Quit'
                      )
                choice = int(input('Enter your choice: '))

                if choice == 1:
                    print("You are not registered.")

                elif choice == 2:
                    username = input('Enter username: ')
                    password = input('Enter password: ')
                    print(login(username, password))

                elif choice == 3:
                    print("Thank you.")
                    m2.working = False
                    quit()

                else:
                    print("Invalid choice.")
    except Exception as e:
        print(e)


def check_user():
    while True:
        # time.sleep(0.5)
        if not m2.working:
            exit()


thread1 = threading.Thread(target=user_login)
thread2 = threading.Thread(target=check_user)

thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("Thank you.")
