
import jwt,json
from datetime import datetime, timedelta
from sqlalchemy import desc,func,text
from sqlalchemy.sql import select
from app.services.systemlog_service import SystemlogService
from app.custom_errors.api_error_data import *
from app.config.system_event_type import SystemEventType
from app.config.models import *
from app.config.logger import *
from typing import Union, List

logger = LogConfig.get_logger()


class VirtualParkingServiceBase:
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

    async def has_vp_rw_permission(self,  account: Account):
        if account.customer_id == 0:
            return True

        return False

        # if customer_id is not None and garage_id is not None and db is not None:
        #     # garage_id不是None, 則檢查garage_id 是不是屬於這個customer_id
        #     async with db.acquire() as conn:
        #         query_res = await conn.execute(select([Garage.c.customer_id]).where(Garage.c.garage_id == garage_id).where(Garage.c.customer_id == customer_id))
        #         db_c_id = await query_res.scalar()
        #
        #     if db_c_id is None:
        #         logger.error(
        #             f'the garage id is not belong to this customer id: garage id: {garage_id}, customer id: {customer_id}')
        #         return False

    async def has_vp_read_permission(self, account: Account, customer_id=None, garage_id=None):
        # 看是否為Acer的管理帳號
        if account.customer_id == 0:
            return True

        if customer_id is not None and garage_id is None:
            if account.customer_id == customer_id:
                return True
            else:
                logger.error(f'This account token can not read the customer vp data: account id: {account.customer_id}, customer_id: {customer_id}')
                return False

        if customer_id is None and garage_id is not None:
            # garage_id不是None, 則檢查garage_id 是不是屬於這個customer_id
            async with  self._db.acquire() as conn:
                query_res = [dict(row.items()) async for row in await conn.execute(
                select([Garage.c.garage_id]).where(
                    Garage.c.customer_id == account.customer_id))]

            if query_res is None or query_res == []:
                logger.error(
                    f'the garage id is not belong to this account token id: garage id: {garage_id}, customer id: {account.customer_id}')
                return False
            else:
                if type(garage_id) is not list:
                    g_id_list = [garage_id]
                else:
                    g_id_list = garage_id

                for g_id in g_id_list:
                    match = False
                    for db_g_id_item in query_res:
                        if db_g_id_item['garage_id'] == g_id:
                            match = True
                            break
                    if match is False:
                        logger.error(
                            f'the garage id is not belong to this account token id: garage id: {g_id}, customer id: {account.customer_id}')
                        return False

                return True

        # 不支持的參數用法
        logger.error('The parameter of has_vp_read_permission are not correct')
        return False

