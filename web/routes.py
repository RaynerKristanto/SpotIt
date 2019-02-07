from main import app
from flask import request, render_template, jsonify, redirect
from utils import *
from room import join_room, create_room, leave_room, Room_Manager
from flask_socketio import SocketIO, emit

room_manager = Room_Manager()
socketio = SocketIO(app)

@app.route('/')
def index():
    if request.cookies.get("gameStatus") in ["lobby", "game"]:
        return redirect("/reroute")
    else:
        res = app.make_response(render_template('index.html'))
        res.set_cookie('gameStatus', "prelobby")
        return res

@app.route('/<path:path>', methods = ["GET"])
def catch_all(path):
    if request.cookies.get("gameStatus") in ["lobby", "game"]:
        return redirect("/reroute")
    else:
        res = app.make_response(render_template('index.html'))
        res.set_cookie('gameStatus', "prelobby")
        return res


@app.route('/test')
def test():
    res = app.make_response(render_template('test.html'))
    return res

@app.route('/join', methods=["POST"])
def join_room_path():
    room_id = request.form["roomID"]
    user_id = request.form["userID"]
    print("GOT ROOM, room id {}, user id {}".format(room_id, user_id))
    if room_id == None:
        room_id = request.cookies.get('roomID')
    
    context = Context(room_id=room_id, room_manager=room_manager, user=user_id)
    result = join_room(context)
    result_object = result.toDict()
    if result.status == Status.FAILURE:
        return jsonify(result_object)

    payload = {"url":"/room/{}".format(room_id), "users" : list(room_manager.get_room(room_id).members)}
    result_object["payload"] = payload
    socketio.emit('user joined', list(room_manager.get_room(room_id).members))

    res = app.make_response(jsonify(result_object))
    res.set_cookie("roomID", room_id)
    res.set_cookie("userID", user_id)

    return res

@app.route('/create', methods=["POST"])
def create_room_path():
    host_id = request.form["userID"]
    room_id = request.form["roomID"]
    context = Context(room_id=room_id, room_manager=room_manager, user=host_id)
    result = create_room(context)
    result_object = result.toDict()
    #Create URL to go alongside
    payload = {"url":"/room/{}".format(room_id), "users": [host_id]}
    result_object["payload"] = payload
    res = app.make_response(jsonify(result_object))
    res.set_cookie("roomID", room_id)
    res.set_cookie("userID", host_id)
    return res

# Route sets the cookie for the room_id user will be attempting to join
@app.route('/invite', methods=["POST"])
def invite_room():
    room_id = request.args.get('roomID')
    res = app.make_response("ADDED COOKIE")
    res.set_cookie('roomID', room_id)
    return res

#TODO: Send the single-page app
#Depending on whether user has the proper cookies for the session, either move them to lobby, or have them choose a
#username
@app.route('/room', methods=["POST"])
def room_path():
    room_id = request.args.get('roomID')
    current_room_id = request.args.get('roomID')
    res = app.make_response(render_template("room.html", room_name=room_id))
    res.set_cookie("roomID", room_id)
    return res

#TODO: Reads the cookie of the user and sends the pertinent information for the state of the game
@app.route('/status', methods=["POST"])
def get_status_path():
    room_id = request.cookies.get('roomID')
    user_id = request.cookies.get('userID')
    payload = {"userID":user_id, "roomID":room_id}
    res = Result.DEFAULT_SUCCESS().toDict()
    res["payload"] = payload
    return jsonify(res)

@app.route('/room_status', methods=["POST"])
def get_room_status():
    room_id = request.cookies.get('roomID')
    user_id = request.cookies.get('userID')
    if room_id != None:
        payload = {"room_id":room_id, "url":"room/{}".format(room_id), "users": list(room_manager.get_room(room_id).members)}
        res = Result.DEFAULT_SUCCESS().toDict()
        res["payload"] = payload
        return jsonify(res)
    else:
        res = Result.DEFAULT_FAILURE().toDict()
        res["reason"] = "User is not in room"
        return jsonify(res)

# Depending on the state of a user's cookies, reroute them to the appropriate place
@app.route("/reroute", methods=["GET"])
def reroute():
    room_id = request.cookies.get("roomID")
    user_id = request.cookies.get("userID")
    game_status = request.cookies.get("status")
    if game_status == "lobby":
        if room_id != None and user_id != None:
            return redirect("/room?roomID={}".format(room_id))
    if game_status == "game":
        if room_id != None and user_id != None:
            return redirect("/game?roomID={}".format(room_id))

    return redirect("/index")

@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

def is_in_session(request):
    cur_room = request.cookies.get("roomID")
    cur_user = request.cookies.get("userID")
    print(cur_room, cur_user)
    if cur_room != None and cur_user != None:
        return True
    return False

if __name__ == '__main__':
    socketio.run(app)