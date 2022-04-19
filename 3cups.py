from flask import Flask
from flask import render_template, request, current_app
from flask_socketio import SocketIO, emit, send, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

students = set()
student2color = dict()

@app.route("/")
def student_interface():
    return render_template('student.html')

@socketio.on('new_student')
def new_student():
    # This will get triggered when the page at /student is rendered
    # In this most basic version opening a new tab would create a new
    # student. If someone would want to exploit this, they could mess
    # with us. We can make it progressively "more secure" if we would
    # like, just need to replace the SID for something else.
    global students
    students.add(request.sid)

@app.route("/teacher")
def teacher_interface():
    global students
    return render_template(
            'teacher.html',
            student_count=student_count(),
            active_student_count=active_student_count(),
            color2frac=color_fraction()
            )

def student_count():
    return len(students)

def active_student_count():
    return len(student2color)

def color_fraction():
    color2frac= {}
    total = len(student2color)
    for color in ['green', 'yellow', 'red']:
        if total == 0:
            color2frac[color] =0
        else:
            color2frac[color] = sum([c==color for c in student2color.values()])/total
    return color2frac

@socketio.on('disconnect')
def handle_disconnect():
    global students
    # we don't know who is disconnecting
    # might be a student or a teacher, hence discard
    students.discard(request.sid)
    global student2color
    student2color.pop(request.sid, None)

@socketio.on('color_change')
def handle_message(data):
    global student2color
    student2color[request.sid] = data['new_color']

socketio.run(app, debug=True)
