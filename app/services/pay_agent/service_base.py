
import jwt,json
from datetime import datetime, timedelta
from sqlalchemy import desc,func,text
from sqlalchemy.sql import select
from app.services.systemlog_service import SystemlogService
from app.module.pay_agent.common import *
from app.module.pay_agent.order.db_handler import *
from app.module.pay_agent.garage.db_handler import *
from app.module.pay_agent.pklot import *
from app.custom_errors.api_error_data import *
from app.config.system_event_type import SystemEventType
from app.config.models import *
from typing import Union, List

logger = LogConfig.get_logger()


class PayAgentServiceBase:
    """ every thing about tablat transaction data"""
    _db =None
    _log_service = None
    _syslog = None
    _user: Account = None

    def __init__(self, db, user: Account):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}
        self._user = user

    def is_support_pa_type(self, pa_type: int):
        if pa_type == PAType.PKLOT:
            return True
        return False

    async def has_transac_permission(self, account: Account, garage_id, db)->bool:
        if account.customer_id == 0:
            return True

        async with db.acquire() as conn:
            query_res = await conn.execute(select([Garage.c.customer_id]).where(Garage.c.garage_id == garage_id))
            db_c_id = await query_res.scalar()

        if account.customer_id != db_c_id:
            logger.info(f"Garage id is not belong to the token, api request gId:{garage_id}, token cId:{account.customer_id}, garage cId:{db_c_id}")
            return False

        return True

    async def check_transac_permission_and_get_c_id(self, account: Account, garage_id, db)->int:
        async with db.acquire() as conn:
            query_res = await conn.execute(select([Garage.c.customer_id]).where(Garage.c.garage_id == garage_id))
            db_c_id = await query_res.scalar()

        if account.customer_id == 0:
            return db_c_id

        if account.customer_id != db_c_id:
            logger.info(f"Garage id is not belong to the token, api request gId:{garage_id}, token cId:{account.customer_id}, garage cId:{db_c_id}")
            return -1

        return db_c_id



