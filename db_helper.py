from message import Message
import sqlite3
import settings
import os
from datetime import datetime

database_path = os.path.join(settings.BASE_DIR, 'chatdb.db')

def get_connection(db_path=database_path):
    """
    Returns a sqlite3 connection
    :param db_path: str path to chat's sqlite3 database
    :return: SQLite database connection object
    """
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Exception as e:
        print(e)

def save_chat(ip_address, user_name, message) -> int:
    """
    Saves a new message to the chat databases and return the id of that new chat message
    :param ip_address: str
    :param user_name: str
    :param message: str
    :return: int
    """
    log_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_connection()
    id = conn.execute("SELECT MAX(MESSAGE_ID)+1 FROM CHAT_LOG;").fetchone()[0]
    query = """
        INSERT INTO CHAT_LOG
        VALUES
        (
            ?, ?, ?, ?, ?
        )"""
    conn.execute(query, (id, log_time, ip_address, user_name, message))
    conn.commit()
    return id


def get_messages(min_id=None, max_id=None) -> list:
    """
    Returns a list of Message() objects
    :param min_id: int representing minimum chat message to grab
    :param max_id: int representing maximum chat message to grab
    :return: list
    """
    sub_text = ''
    if min_id:
        sub_text += f'AND MESSAGE_ID >= {str(min_id)}\n'
    if max_id:
        sub_text+= f'AND MESSAGE_ID <= {str(max_id)}'
    query = f"""
        SELECT 
            MESSAGE_ID,
            LOG_TIME,
            IP_ADDRESS,
            USER_NAME,
            MESSAGE
        FROM
            CHAT_LOG
        WHERE
            MESSAGE_ID != 0
            {sub_text}
        ORDER BY LOG_TIME ASC
        LIMIT 500;"""

    conn = get_connection()
    results = conn.execute(query).fetchall()
    messages = []
    for row in results:
        messages.append(Message(
            id=row[0],
            send_ts=row[1],
            ip_address=row[2],
            user_name=row[3],
            type='text',
            content=row[4]

        ))
    return messages

def get_max_id() -> int:
    """
    Returns max chat id
    :return: int
    """
    query = f"""
          SELECT 
              MAX(MESSAGE_ID)
          FROM
              CHAT_LOG
          WHERE
              MESSAGE_ID != 0;"""

    conn = get_connection()
    return conn.execute(query).fetchone()[0]

