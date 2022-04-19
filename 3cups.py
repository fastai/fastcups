from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, emit
import random, string, collections

app = Flask(__name__)
socketio = SocketIO(app)
sid2student, student2color  = dict(), collections.defaultdict(lambda: 'inactive')

@app.route("/")
def student_interface():
    student_id = request.cookies.get('student_id')
    if student_id: # a student opened a new tab
        emit('close_old_tabs', student_id, broadcast=True, namespace='/')
    else: # a new student
        student_id = random_string()
    response = make_response(render_template('student.html', cup_state=student2color[student_id]))
    response.set_cookie('student_id', student_id)
    return response

@socketio.on('get_cup_color')
def get_cup_color_for_student():
    return student2color[request.cookies['student_id']]

@socketio.on('register_student')
def register_student():
    sid2student[request.sid] = request.cookies['student_id']

def student_count(): return len(sid2student)
def connected_student2color():
    return {k: v for k, v in student2color.items() if k in sid2student.values()}
def active_student_count(): return sum(isinstance(s, str) for s in connected_student2color().values() if s != 'inactive')

def color_fraction():
    return {color: sum(c==color for c in connected_student2color().values())/(active_student_count() or 1)
            for color in ['green', 'yellow', 'red']}

@app.route("/teacher")
def teacher_interface():
    return render_template( 'teacher.html', student_count=student_count(),
        active_student_count=active_student_count(), color2frac=color_fraction())

@socketio.on('disconnect')
def handle_disconnect():
    sid2student.pop(request.sid, None)

@socketio.on('color_change')
def handle_color_change(new_color): student2color[request.cookies['student_id']] = new_color

def random_string(length=12):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

socketio.run(app, debug=True)

