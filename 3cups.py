from flask import Flask
from flask import render_template, request, current_app
from flask_socketio import SocketIO, emit, send, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)
students,student2color = set(),dict()

@app.route("/")
def student_interface(): return render_template('student.html')

@socketio.on('new_student')
def new_student(): students.add(request.sid)

def student_count(): return len(students)
def active_student_count(): return len(student2color)

def color_fraction():
    return {color: sum(c==color for c in student2color.values())/(len(student2color) or 1)
            for color in ['green', 'yellow', 'red']}

@app.route("/teacher")
def teacher_interface(): return render_template( 'teacher.html', student_count=student_count(),
        active_student_count=active_student_count(), color2frac=color_fraction())

@socketio.on('disconnect')
def handle_disconnect():
    # we don't know who is disconnecting; might be a student or a teacher, hence discard
    students.discard(request.sid)
    student2color.pop(request.sid, None)

@socketio.on('color_change')
def handle_message(data): student2color[request.sid] = data['new_color']

socketio.run(app, debug=True)

