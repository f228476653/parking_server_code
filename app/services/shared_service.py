

class SharedService(Service):
    """ every thing about user , like account, permission, role"""
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None
    def __init__(self, db, user: Account):
        self._db = db
        self._user =user
        self._log_service = SystemlogService(self._db)
        self._syslog = {}

    def get_activate_code_for_pad(self, customer_id: str, garage_id: str):
