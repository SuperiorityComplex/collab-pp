from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Canvas(_message.Message):
    __slots__ = ["canvas"]
    CANVAS_FIELD_NUMBER: _ClassVar[int]
    canvas: str
    def __init__(self, canvas: _Optional[str] = ...) -> None: ...

class FrontendRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UserRequest(_message.Message):
    __slots__ = ["col", "color", "community", "delay", "row", "username"]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    COL_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_FIELD_NUMBER: _ClassVar[int]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    ROW_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    col: int
    color: str
    community: str
    delay: int
    row: int
    username: str
    def __init__(self, color: _Optional[str] = ..., row: _Optional[int] = ..., col: _Optional[int] = ..., username: _Optional[str] = ..., community: _Optional[str] = ..., delay: _Optional[int] = ...) -> None: ...

class UserResponse(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
