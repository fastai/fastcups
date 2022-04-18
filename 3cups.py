from flask import Flask
from flask import render_template, request, current_app
from flask_socketio import SocketIO, emit, send, join_room, leave_room

from IPython.core.debugger import set_trace

app = Flask(__name__)
socketio = SocketIO(app)

students = set()

@app.route("/")
def student_interface():
    return render_template('student.html')

@socketio.on('new_student')
def new_student():
    global students
    students.add(request.sid)

    print(request.sid)
    print(len(students))
    print('new_student')

@app.route("/teacher")
def teacher_interface():
    return render_template('teacher.html')

@socketio.on('disconnect')
def handle_disconnect():
    global students
    # we don't know who is disconnecting
    # might be a student or a teacher, hence discard
    students.discard(request.sid)

    print(request.sid)
    print(len(students))

@socketio.on('color_change')
def handle_message(data):
    global students
    print(request.sid)
    print(len(students))

socketio.run(app, debug=True)
