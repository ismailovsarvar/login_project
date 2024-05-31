import utils
from db import cur, conn
from models import User
from sessions import Session

session = Session()

try:
    def get_user_data(prm: str, atr: str | int) -> tuple:
        cur.execute(f"""SELECT * FROM users WHERE {prm} =  %s""", (atr,))
        data = cur.fetchone()
        return data


    def login() -> utils:
        user: Session | None = session.check_session()
        if user:
            return utils.BadRequest('You already logged in', status_code=401)

        username: str = input("Enter your username: ")
        password: str = input("Enter your password: ")
        user_data: tuple = get_user_data(prm='username', atr=username)

        if not user_data:
            return utils.BadRequest('Username not found in my DB')
        _user = User(username=user_data[1],
                     password=user_data[2],
                     role=user_data[3],
                     status=user_data[4],
                     login_try_count=user_data[5]
                     )

        if password != _user.password:
            update_count_query = """UPDATE users SET login_try_count = login_try_count + 1 WHERE username = %s;"""
            cur.execute(update_count_query, (_user.username,))
            conn.commit()
            return utils.BadRequest('Wrong username or password', status_code=401)

        if _user.login_try_count > 3:
            return utils.ResponseData('Your login blocked', status_code=401)

        user = Session(_user)
        user.add_session(_user)
        print("Welcome to profile" + _user.username)

except Exception as error:
    print("Check this: {}".format(error))
