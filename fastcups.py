from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, emit
import random, string, collections, time
from fastcore.utils import *
from urllib.parse import urlparse

app = Flask(__name__)
socketio = SocketIO(app)
sid2student, student2color, class2students  = dict(), dict(), collections.defaultdict(lambda: set())

@app.route('/')
def root(): return render_template('howto.html', url=f'https://{urlparse(request.base_url).hostname}')

@app.route('/<class_id>')
def student_interface(class_id):
    student_id = request.cookies.get('student_id') or ''.join(random.choices(string.ascii_letters, k=12))
    class2students[class_id].add(student_id)
    response = make_response(render_template('student.html', timestamp=time.time(), class_id=class_id))
    response.set_cookie('student_id', student_id)
    return response

@socketio.on('register_student')
def register_student(timestamp, class_id):
    student_id = request.cookies.get('student_id')
    emit('deactivate_old_tabs', # a student can only have a single tab active
            {'student_id':  student_id, 'timestamp': timestamp}, broadcast=True, namespace='/')
    student2color[student_id] = 'inactive' # upon connecting / opening a new tab a student is in an inactive state
    sid2student[request.sid] = student_id # used for keeping track of connected students
    for cls in class2students: # a student can only be in a single class
        class2students[cls].discard(student_id)
    class2students[class_id].add(student_id)

def student_count(class_id): return L(sid2student.values()).filter(lambda s: s in class2students[class_id]).count()
def connected_student2color(class_id):
    return {k: v for k, v in student2color.items() if (k in class2students[class_id]) and (k in sid2student.values())}
def active_student_count(class_id): # active student == one who is connected and color != 'inactive'
    return L(connected_student2color(class_id).values()).filter(lambda c: c != 'inactive').count()

def color_fraction(class_id):
    return {color: L(connected_student2color(class_id).values()).map(eq(color)).sum()/(active_student_count(class_id) or 1)
            for color in ['green', 'yellow', 'red']}

@app.route('/<class_id>/teacher')
def teacher_interface(class_id):
    return render_template('teacher.html', student_count=student_count(class_id),
        active_student_count=active_student_count(class_id), color2frac=color_fraction(class_id))

@socketio.on('color_change')
def handle_color_change(new_color): student2color[request.cookies['student_id']] = new_color

@socketio.on('disconnect')
def handle_disconnect():
    student = sid2student.pop(request.sid, None)

@patch
def count(self:L): return len(self)

socketio.run(app)

