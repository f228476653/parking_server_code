

import datetime

class JsonHelper(object):
    
    @staticmethod
    def date_converter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()