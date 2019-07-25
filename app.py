import json
from flask import Flask, render_template, request, jsonify, send_from_directory
import db_helper
from flask_socketio import SocketIO
import flask_socketio
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = ':~.C2%,36afzN6t4'
socketio = SocketIO(app, logger=True)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/chat")
def get_chat_view():
    """
    Returns chat page to client's browser
    :return:
    """
    messages = get_all_chat_dict()
    return render_template("mainchat.html", message_list=messages)


@socketio.on('connect', namespace='/')
def handle_new_connection():
    print("New connection from " + request.remote_addr)


@socketio.on('sendchat')
def handle_incoming_msg(message_dict) -> None:
    """
    Takes new message from client browser and saves to sqlite3 db
    Calls on emit_chat_message() to use socketio to emit new message that
    was just saved.
    :param message_dict:
    :return: None
    """
    id = db_helper.save_chat(
        ip_address=request.remote_addr,
        user_name=message_dict['userName'],
        message=message_dict['message'].strip()
    )
    print(f"{str(id)} - {message_dict['userName']}:\t {message_dict['message'].strip()}")
    emit_chat_message(id)


def emit_chat_message(message_id) -> None:
    """
    Uses socketio to emit a single message
    :param message_id: int
    :return: None
    """
    # Just bring back a single message
    # messages will be a list of one object
    messages = get_all_chat_dict(min_id=message_id, max_id=message_id)
    print("Sending " + str(messages))
    return_dict = {
        'dataRows': messages
    }
    socketio.emit('newMessages', return_dict, broadcast=True, namespace='/')


@socketio.on('requestmessages')
def handle_msg_request(message_dict) -> None:
    """
    Ingests last message ID from client, and sends remaining messages back.
    :param message_dict: dictionary object containing key value pair of 'lastId' and it's int value
    :return: None
    """
    last_id = message_dict['lastId']
    data = get_all_chat_dict(min_id=last_id)
    messages_dict = {}
    if len(data) == 0:
        messages_dict['hasNewData'] = False
        socketio.emit('newMessages', messages_dict)
    message_dict['dataRows'] = data
    flask_socketio.emit('newMessages', message_dict, broadcast=False)

@app.route("/sendchat", methods = ['POST'])
def handle_new_message():
    """
    Takes incoming requests from the chat and sends them off
    to the chat_helper to be logged in the sqlite3 db
    :return: jsonify()
    """

    if request.form['message'].strip() == '':
        return jsonify(messagePosted=False)
    id = db_helper.save_chat(
        ip_address=request.remote_addr,
        user_name=request.form['userName'],
        message=request.form['message'].strip()
    )
    return jsonify(messagePosted=True if id != 0 else False)


@app.route("/requestmessages", methods=['POST'])
def handle_msg_request():
    last_id = int(request.form['lastId'])
    data = get_all_chat_dict(min=last_id)
    if len(data) == 0:
        return jsonify(hasNewData=False)
    return jsonify(hasNewData=True, dataRows=data)



@app.route('/<folderpath>/<filename>')
def send_static(folderpath, filename):
    return send_from_directory(os.path.join('static/', folderpath), filename)


def get_all_chat_dict(min_id=None, max_id=None) -> dict:
    msgs = db_helper.get_messages(min_id, max_id)
    msg_dict = {}
    for message in msgs:
        msg_dict[message.id] = json.loads(message.to_json())
    return msg_dict


def sendAjaxResponse(data):
    return jsonify(data=data)

@socketio.on('message')
def handle_message(message) -> None:
    print(f"Incoming message from {request.remote_addr}: {message}")


if __name__ == '__main__':
    print("Starting!")
    socketio.run(app=app, log_output=True, host='0.0.0.0', port=8000)
    print("Done!")
