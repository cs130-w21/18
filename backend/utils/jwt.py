from jwt import encode, decode
import os
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Algorithm(Enum):
    HS256 = "HS256"
    RS256 = "RS256" #currently not supported

class JWTStrategy(ABC):

    @classmethod
    @abstractmethod
    def algorithm(cls):
        pass
    
    @classmethod
    @abstractmethod
    def encode(self, payload, additional_headers):
        pass

    @abstractmethod
    def decode(self, token):
        pass

class HSAStrategy(JWTStrategy):
    @classmethod
    def algorithm(cls):
        return Algorithm.HS256.value
    
    @classmethod
    def secret(cls):
        return os.environ['JWT_SECRET']
    
    @classmethod
    def encode(cls, payload, additional_headers):
        return encode(payload, cls.secret(), algorithm=cls.algorithm(), headers=additional_headers)

    @classmethod
    def decode(cls, token):
        return decode(token, cls.secret(), algorithms=[cls.algorithm()])

class JWT:
    @classmethod
    def encode(cls, payload, additional_headers=None, strategy=None):
        if strategy is None:
            strategy = HSAStrategy
        return strategy.encode(payload, additional_headers)
    
    @classmethod
    def decode(cls, token, strategy=None):
        payload = None
        if strategy is None:
            strategy = HSAStrategy
        return strategy.decode(token)


