from typing_extensions import NotRequired
from typing import TypedDict

'''
Type defs for the various message types
'''


class AddUserMessage(TypedDict):
    userName: str
    password: str
    access: str


class StandardResponse(TypedDict):
    success: bool
    msg: NotRequired[str]


class StandardRequest(TypedDict):
    request: bool


class GetAllUsersMessage(TypedDict):
    users: list[str]


class AuthorizeUserMessage(TypedDict):
    token: str
    access: str

class UpdateAccessMessage(TypedDict):
    userName: str
    access: str

class DeleteUserMessage(TypedDict):
    userName: str