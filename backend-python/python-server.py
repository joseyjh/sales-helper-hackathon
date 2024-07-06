from threading import Event
from flask_cors import CORS
from flask_socketio import SocketIO
from flask import Flask
import time
import eventlet

eventlet.monkey_patch()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('connect')
def handle_connect():
    print("New client connected")

    def send_messages():
        while not thread_stop_event.is_set():
            content = {
                'timestamp': time.time(),
                'message': "Hello from the server!"
            }
            socketio.emit('message', content)
            socketio.sleep(1)

    # global thread_stop_event
    # thread_stop_event = Event()
    # socketio.start_background_task(send_messages)


@socketio.on('message from simple client')
def handle_message_from_simple_client(message):
    print(message)
    socketio.emit('message', message)


@socketio.on('message event')
def handle_message_from_process_text_file(message):
    print(message)
    socketio.emit('message', message)


@socketio.on('disconnect')
def handle_disconnect():
    global thread_stop_event
    thread_stop_event.set()
    print("Client disconnected")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8765)
