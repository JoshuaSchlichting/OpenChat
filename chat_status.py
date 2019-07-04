import db_helper
import time

max_chat_id = None

def monitor_chat():
    global max_chat_id
    if max_chat_id == None:
        max_chat_id = db_helper.get_max_id()

    while(True):
        time.sleep(1)


