
import jwt,json
from datetime import datetime, timedelta

from app.config.models import SystemLog,Event
from sqlalchemy import desc
from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError

class SystemlogService:
    """ every thing about systemlog """
    _db =None
    def __init__(self, db):
        self._db = db

    async def addlog(self, system_log: SystemLog):
        """ addlog """
        async with self._db.acquire() as conn:
            result = await conn.execute(SystemLog.insert(system_log))
            return result.rowcount

    async def delete_alllog(self, system_log: SystemLog):
        """ delete_alllog """
        async with self._db.acquire() as conn:
            result = await conn.execute(SystemLog.delete().where(SystemLog.c.log_id >= 0))
            result = await conn.execute(SystemLog.insert(system_log))
            return result.rowcount

    async def query_by_msg(self, system_log: SystemLog):
        """ query_by_msg """
        async with self._db.acquire() as conn:
            #add log
            #result = await conn.execute(SystemLog.insert(system_log))
            #query
            s = SystemLog.select().where(SystemLog.c.event_message.like('%'+ system_log['query_string'] + '%')).order_by(desc(SystemLog.c.create_date))
            syslog = [dict(row.items()) async for row in await conn.execute(s)]
            return syslog


    async def query_by_date(self, system_log:SystemLog):
        """ query_by_date """
        async with self._db.acquire() as conn:
            #add log
            #result = await conn.execute(SystemLog.insert(system_log))
            #query
            s = SystemLog.select().where(SystemLog.c.create_date.like('%'+ system_log['query_string'] + '%')).order_by(desc(SystemLog.c.create_date))
            syslog = [dict(row.items()) async for row in await conn.execute(s)]
            return syslog

    async def query_by_event(self, system_log:SystemLog):
        """ query_by_event """
        async with self._db.acquire() as conn:
            #add log
            #result = await conn.execute(SystemLog.insert(system_log))
            #query
            s = SystemLog.select().where(SystemLog.c.event_id == system_log['query_string']).order_by(desc(SystemLog.c.create_date))
            syslog = [dict(row.items()) async for row in await conn.execute(s)]
            return syslog

    async def query_SystemEventType(self, system_log):
        """ query_SystemEventType """
        async with self._db.acquire() as conn:
            #add log
            #result = await conn.execute(SystemLog.insert(system_log))
            #query
            s = Event.select().where(Event.c.event_id== system_log['query_string'])
            evn = [dict(row.items()) async for row in await conn.execute(s)]
            return evn