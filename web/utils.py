from enum import Enum
import json
import copy

class Context:
    room_id = None
    room_manager = None
    user = None
    def __init__(self, room_id=None, room_manager=None, user=None):
        self.room_id = room_id
        self.room_manager = room_manager
        self.user = user

# Object to denote the status of an operation
# Should be model-neutral, can be used as REST Response
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
        return "<Result Object, STATUS: {}, Message: {}>".format(self.status, self.message)

    def toDict(self):
        internal_dict_cpy = copy.copy(vars(self))
        for key in internal_dict_cpy:
            internal_dict_cpy[key] = str(internal_dict_cpy[key])
        return internal_dict_cpy


class Status(Enum):
    SUCCESS = 0
    FAILURE = 1