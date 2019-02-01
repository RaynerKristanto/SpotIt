from main import app
from flask import request, render_template, jsonify
from utils import *
from room import join_room, create_room, leave_room, Room_Manager
from flask_socketio import SocketIO, emit

room_manager = Room_Manager()
socketio = SocketIO(app)

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
    return result.toDict()

@app.route('/create', methods=["POST"])
def create_room_path():
    host_id = request.form["hostID"]
    room_id = request.form["roomID"]
    context = Context(room_id=room_id, room_manager=room_manager, user=host_id)
    result = create_room(context)
    print(result)
    result_object = result.toDict()

    #Create URL to go alongside
    payload = {"url":"/room?roomID={}".format(room_id)}
    result_object["payload"] = payload
    return jsonify(result_object)

# Route sets the cookie for the room_id user will be attempting to join
#TODO: Send actual page
@app.route('/invite', methods=["GET"])
def invite_room():
    room_id = request.args.get('roomID')
    res = app.make_response("ADDED COOKIE")
    res.set_cookie('roomID', room_id)
    return res

#TODO: Send the single-page app
#Depending on whether user has the proper cookies for the session, either move them to lobby, or have them choose a
#username
@app.route('/room', methods=["GET"])
def room_path():
    room_id = request.args.get('roomID')
    res = app.make_response(render_template("room.html", room_name=room_id))
    res.set_cookie("roomID", room_id)
    return res


#TODO: Reads the cookie of the user and sends the pertinent information for the state of the game
@app.route('/status', methods=["POST"])
def get_status_path():
    room_id = request.cookies.get('roomID')
    user_id = request.cookies.get('userID')
    payload = {"userID":user_id, "room_id":room_id}
    res = Result.DEFAULT_SUCCESS().toDict()
    res["payload"] = payload
    return str(res)

@app.route("/show_rooms", methods=["GET"])
def show_rooms():
    return str(room_manager.get_rooms())

@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)