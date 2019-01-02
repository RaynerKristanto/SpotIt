from main import app
from flask import request, render_template
from utils import *
from room import join_room, create_room, leave_room, Room_Manager


room_manager = Room_Manager()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/join', methods=["POST"])
def join_room_path():
    room_id = request.form["roomID"]
    if room_id == None:
        room_id = request.cookies.get('roomID')
    user_id = request.form["userID"]
    context = Context(room_id=room_id, room_manager=room_manager, user=user_id)
    result = join_room(context)
    print(result)
    return str(result)

@app.route('/create', methods=["POST"])
def create_room_path():
    host_id = request.form["hostID"]
    room_id = request.form["roomID"]
    context = Context(room_id=room_id, room_manager=room_manager, user=host_id)
    result = create_room(context)
    print(result)
    return str(result)

# Route sets the cookie for the room_id user will be attempting to join
#TODO: Send actual page
@app.route('/invite', methods=["GET"])
def invite_room():
    room_id = request.args.get('roomID')
    res = app.make_response("ADDED COOKIE")
    res.set_cookie('roomID', room_id)
    return res


@app.route("/show_rooms", methods=["GET"])
def show_rooms():
    return str(room_manager.get_rooms())
