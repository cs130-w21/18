from enum import Enum

class Scope(Enum):
    USER_TOP_READ='user-top-read'
    PLAYLIST_MODIFY_PRIVATE='playlist-modify-private'
    PLAYLIST_MODIFY_PUBLIC='playlist-modify-public'
    USER_READ_PRIVATE='user-read-private'

class Scopes:

    scopes=[Scope.USER_TOP_READ, Scope.PLAYLIST_MODIFY_PRIVATE, 
            Scope.PLAYLIST_MODIFY_PUBLIC, Scope.USER_READ_PRIVATE]
    
    @classmethod
    def get_all(cls):
        scopes = cls.scopes
        scopes = " ".join([s.value for s in cls.scopes])
        return scopes
