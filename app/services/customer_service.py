
import jwt,json
from datetime import datetime, timedelta

from app.config.models import Customer,Permission, Account,Garage
from sqlalchemy import desc
from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler


class CustomerService:
    """ every thing about customer """
    _db =None
    _log_service = None
    _syslog = None
    _user: Account = None
    def __init__(self, db, user: Account):
        self._db = db
        self._user =user
        self._log_service = SystemlogService(self._db)
        self._syslog = {}

    async def get_customers(self):
        """ get all customer """
        if self._user.is_superuser:
            async with self._db.acquire() as conn:
                result = [dict(row.items()) async for row in await conn.execute(Customer.select().order_by(desc(Customer.c.create_date)))]
                return result
        else:
            async with self._db.acquire() as conn:
                result = [dict(row.items()) async for row in await conn.execute(Customer.select().where(Customer.c.customer_id == self._user.customer_id).order_by(desc(Customer.c.create_date)))]
                return result
        
    async def get_customer_by_id(self,id):
        """ get customer by id """
        async with self._db.acquire() as conn:
            data= await conn.execute(Customer.select().where((Customer.c.customer_id == id)))
            return await data.fetchone()


