from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, emit
import random, string, collections, time
from fastcore.utils import *

app = Flask(__name__)
socketio = SocketIO(app)
sid2student, student2color  = dict(), collections.defaultdict(lambda: 'inactive')

@app.route("/")
def student_interface():
    student_id = request.cookies.get('student_id') or ''.join(random.choices(string.ascii_letters, k=12))
    response = make_response(render_template('student.html', cup_state=student2color[student_id], timestamp=time.time()))
    response.set_cookie('student_id', student_id)
    return response

@socketio.on('get_cup_color')
def get_cup_color_for_student():
    return student2color[request.cookies['student_id']]

@socketio.on('register_student')
def register_student(timestamp):
    emit('close_old_tabs', {'student_id': request.cookies.get('student_id'), 'timestamp': timestamp}, broadcast=True, namespace='/')
    sid2student[request.sid] = request.cookies['student_id']

def student_count(): return len(sid2student)
def connected_student2color():
    return {k: v for k, v in student2color.items() if k in sid2student.values()}
def active_student_count(): # active student == one who is connected and color != 'inactive'
    return len(L(connected_student2color().values()).filter(lambda c: c != 'inactive'))

def color_fraction():
    return {color: L(student2color.values()).map(eq(color)).sum()/(active_student_count() or 1)
            for color in ['green', 'yellow', 'red']}

@app.route("/teacher")
def teacher_interface():
    return render_template('teacher.html', student_count=student_count(),
        active_student_count=active_student_count(), color2frac=color_fraction())

@socketio.on('color_change')
def handle_color_change(new_color): student2color[request.cookies['student_id']] = new_color

@socketio.on('disconnect')
def handle_disconnect():
    sid2student.pop(request.sid, None)

socketio.run(app, debug=True)

