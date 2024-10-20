"""
This script runs the AIGuide application using a development server.
"""
from flask_socketio import SocketIO
from os import environ
from AIGuide import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
    socketio = SocketIO(app)
    socketio.run(app, debug=True)
