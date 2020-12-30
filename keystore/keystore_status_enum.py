from enum import IntEnum

class KeystoreStatusEnum(IntEnum):
    WAITFORAPPROVAL =1
    ENABLED = 2 # if check is valid 
    DISABLED = 3 # if disabled, disabled

    def asdict():
        return [ 
            { 'name':'WAITFORAPPROVAL', 'value':1}
            ,{ 'name':'ENABLED', 'value':2}
            ,{ 'name':'DISABLED', 'value':3}]