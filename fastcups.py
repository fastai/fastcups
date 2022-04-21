from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, emit
import random, string, collections, time
from fastcore.utils import *

app = Flask(__name__)
socketio = SocketIO(app)
sid2student, student2color, class2students  = dict(), collections.defaultdict(lambda: 'inactive'), collections.defaultdict(lambda: set())

@app.route("/<class_id>")
def student_interface(class_id):
    student_id = request.cookies.get('student_id') or ''.join(random.choices(string.ascii_letters, k=12))
    class2students[class_id].add(student_id)
    response = make_response(render_template('student.html', cup_state=student2color[student_id], timestamp=time.time(), class_id=class_id))
    response.set_cookie('student_id', student_id)
    return response

@socketio.on('get_cup_color')
def get_cup_color_for_student():
    return student2color[request.cookies['student_id']]

@socketio.on('register_student')
def register_student(timestamp, class_id):
    emit('close_old_tabs', {'student_id': request.cookies.get('student_id'), 'timestamp': timestamp}, broadcast=True, namespace='/')
    sid2student[request.sid] = request.cookies['student_id']
    class2students[class_id].add(request.cookies['student_id'])

def student_count(class_id): return len(L(sid2student.values()).filter(lambda s: s in class2students[class_id])) #return len(sid2student)
def connected_student2color(class_id):
    return {k: v for k, v in student2color.items() if (k in class2students[class_id]) and (k in sid2student.values())}
def active_student_count(class_id): # active student == one who is connected and color != 'inactive'
    return len(L(connected_student2color(class_id).values()).filter(lambda c: c != 'inactive'))

def color_fraction(class_id):
    return {color: L(connected_student2color(class_id).values()).map(eq(color)).sum()/(active_student_count(class_id) or 1)
            for color in ['green', 'yellow', 'red']}

@app.route("/<class_id>/teacher")
def teacher_interface(class_id):
    return render_template('teacher.html', student_count=student_count(class_id),
        active_student_count=active_student_count(class_id), color2frac=color_fraction(class_id))

@socketio.on('color_change')
def handle_color_change(new_color): student2color[request.cookies['student_id']] = new_color

@socketio.on('disconnect')
def handle_disconnect():
    student = sid2student.pop(request.sid, None)
    for cls in class2students: class2students[cls].discard(student)

socketio.run(app, debug=True)

