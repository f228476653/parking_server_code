import json,enum
import datetime
import decimal
from collections import OrderedDict
from pprint import pprint

def custom_json_handler(x):
    if isinstance(x, datetime.datetime):
        return x.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(x, datetime.date):
        return x.strftime('%Y-%m-%d')
    elif isinstance(x, enum.IntEnum):
        return x.value
    elif isinstance(x, decimal.Decimal):
        # wanted a simple yield str(o) in the next line,
        # but that would mean a yield on the line with super(...),
        # which wouldn't work (see my comment below), so...
        return str(x)
    
    raise TypeError("Can't serialize %r" % (x,))

def utc_json_handler(x):
    
    if isinstance(x, datetime.datetime):
        return x.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    elif isinstance(x, datetime.date):
        return x.strftime('%Y-%m-%d')
    elif isinstance(x, enum.IntEnum):
        return x.value
    
    raise TypeError("Type Error")

def serialize_instance(obj):
    d = { '__classname__' : type(obj).__name__}
    d.update(vars(obj))
    return d

def keystore_json_handler(x):
    
    if isinstance(x, KeystoreStatusEnum):
        
        return str(x.value)
    elif isinstance(x, OrderedDict):
        
        return str(x.keys)
    else:
        pprint(x)
        return str(x)

    raise TypeError("Type Error")

