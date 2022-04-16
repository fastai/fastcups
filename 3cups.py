from flask import Flask
from flask import render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

students_count = 0

@app.route("/")
def hello_world():
    return render_template('student.html')

@socketio.on('connect')
def handle_student_connect():
    global students_count
    students_count += 1
    print(students_count)

@socketio.on('disconnect')
def handle_student_disconnect():
    global students_count
    students_count -= 1
    print(students_count)

@socketio.on('color_change')
def handle_message(data):
    global counter
    print(data)

socketio.run(app, debug=True)
