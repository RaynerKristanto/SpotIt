from utils import Result, Status
from enum import Enum

class Room_Status(Enum):
    CREATE_SUCCESS = 1
    CREATE_FAILURE_NAME_TAKEN = 2
    CREATE_FAILURE_INVALID_NAME = 3

    JOIN_SUCCESS = 4
    JOIN_FAILURE = 5
    JOIN_FAILURE_NAME_TAKEN = 6
    JOIN_FAILURE_INVALID_ROOM = 7

    LEAVE_SUCCESS = 8
    LEAVE_FAILURE = 9

class Room_Manager:
    def __init__(self):
        self.rooms = {}

    def add_room(self, room):
        if room.id not in self.rooms:
            self.rooms[room.id] = room
            return Room_Status.CREATE_SUCCESS
        else:
            return Room_Status.CREATE_FAILURE_NAME_TAKEN

    def remove_room(self, room):
        if room in self.rooms:
            del self.rooms[room]
            return True
        return False

    def get_room(self, room_id):
        if room_id not in self.rooms:
            return None
        return self.rooms[room_id]

    def get_rooms(self):
        return list(map(lambda x : str(self.rooms[x]), list(self.rooms)))


class Room:
    def __init__(self, id=None, host=None):
        self.id = id
        self.host = host
        self.members = {host}

    def add_member(self, member):
        if member == None:
            return Room_Status.JOIN_FAILURE
        elif member in self.members:
            return Room_Status.JOIN_FAILURE_NAME_TAKEN
        else:
            self.members.add(member)
            return Room_Status.JOIN_SUCCESS

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)
            return Room_Status.LEAVE_SUCCESS

        return Room_Status.LEAVE_FAILURE

    def __str__(self):
        return "<Room with ID: {}, Currently {} Members>".format(self.id, len(self.members))

    def members_string(self):
        a = "There are currently {} members: ".format(len(self.members))
        for i in self.members:
            a += str(i) + ", "
        a = a[:-2]
        return a

    def __hash__(self):
        return hash(self.id + "," + self.host)

class Member:
    id = None
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        if isinstance(other, Member):
            return other.id == id
        return False

# TODO: Match error codes with correct message
def create_room(context):
    new_room = Room(id=context.room_id, host=context.user)
    success = context.room_manager.add_room(new_room)
    if success == Room_Status.CREATE_SUCCESS:
        print("Create Room Success")
        return Result.DEFAULT_SUCCESS()
    else:
        print("Create Room Failure, Code:" + str(success))
        return Result.DEFAULT_FAILURE()

def join_room(context):
    requested_room_id = context.room_id
    interested_room = context.room_manager.get_room(requested_room_id)
    if interested_room != None:
        result = interested_room.add_member(context.user)
        if result == Room_Status.JOIN_SUCCESS:
            return Result.DEFAULT_SUCCESS()
        elif result == Room_Status.JOIN_FAILURE_NAME_TAKEN:
            return Result(Status.FAILURE, "Name already taken")
        else:
            return Result.DEFAULT_FAILURE()
    else:
        print("Join Room Failure, Code: " + str(Room_Status.JOIN_FAILURE_INVALID_ROOM))
        return Result(Status.FAILURE, "Room not found")

# TODO: Match error codes with correct message
def leave_room(context):
    requested_room_id = context.args[0]
    interested_room = context.room_manager.get_room(requested_room_id)
    if interested_room != None:
        result = interested_room.remove_member(context.user)
        if result == Room_Status.LEAVE_SUCCESS:
            return Result.DEFAULT_SUCCESS()
        else:
            return Result.DEFAULT_FAILURE()
    else:
        Result.DEFAULT_FAILURE()


