from enum import IntEnum

class KeystoreValidationEnum(IntEnum):
    VALID = 1 # if check is valid 
    INVALID = 2 # if check is invalid like, decodeError
    EXPIRED = 3 # if expired

    def asdict():
        return [ 
            { 'name':'VALID', 'value':1}
            ,{ 'name':'INVALID', 'value':2}
            ,{ 'name':'EXPIRED', 'value':3}]