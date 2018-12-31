from enum import Enum

class Context:
    room_id = None
    room_manager = None
    user = None
    def __init__(self, room_id=None, room_manager=None, user=None):
        self.room_id = room_id
        self.room_manager = room_manager
        self.user = user

# Object to denote the status of an operation
# Should be model-neutral
class Result:
    def __init__(self, status, message=None):
        self.status = status
        self.message = message

    @staticmethod
    def DEFAULT_SUCCESS():
        return Result(Status.SUCCESS)

    @staticmethod
    def DEFAULT_FAILURE():
        return Result(Status.FAILURE)

    def __str__(self):
        return "<Result Object, STATUS: {}, Message: {}".format(self.status, self.message)


class Status(Enum):
    SUCCESS = 0
    FAILURE = 1