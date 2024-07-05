import time
import eventlet

eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from threading import Event

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

    global thread_stop_event
    thread_stop_event = Event()
    socketio.start_background_task(send_messages)

@socketio.on('disconnect')
def handle_disconnect():
    global thread_stop_event
    thread_stop_event.set()
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8765)
