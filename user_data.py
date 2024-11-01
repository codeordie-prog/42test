import streamlit as stt
import sqlite3
import json
from streamlit_cookies_manager import EncryptedCookieManager
import uuid


#use cookies to distinguish user_id and to store data

cookies = EncryptedCookieManager(

    prefix = "test42app",
    #password = st.secrets['COOKIES_PASSWORD']
    password = "test42"

)

if not cookies.ready():
    stt.stop()


#initialize a new key 'run_id'

if 'run_id' not in stt.session_state:

    stt.session_state['run_id'] = ""

#database

conn = sqlite3.connect("usersdata.db")
cursor = conn.cursor()


#check if user_id is in cookies else create one

if 'user_id' not in cookies:
    cookies['user_id']=str(uuid.uuid4()) # use this to ensure users don share id
    cookies.save()

user_id = cookies["user_id"]

def load_user_data(user_id):
    cursor.execute("SELECT data FROM session_data WHERE user_id = ?",(user_id,))
    result = cursor.fetchone()
    return json.loads(result[0]) if result else {}


def get_user_data(user_id):
    return load_user_data(user_id=user_id)



"""""
Notes:

check whether you can trace user's cookies, if so use this as a way to retrieve data from the db and maybe implement a new memory

also make sure you check whether its necessary to create the columns in cookies from the streamlit_cookie_manager lib or they are already created

also check whether its really necesarry to initiate keys by default : this code here: # Ensure keys are set before using them in widgets
for key, value in user_data.items():
    st.session_state.setdefault(key, value)

    


"""

