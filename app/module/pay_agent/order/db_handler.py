import aiohttp
import json
from app.config.logger import LogConfig
from app.config.models import GaragePaArgsTable, Parking
from app.module.pay_agent.order.models import ParkingTblRow
from app.util.str_helper import StringHelper
import datetime
from typing import Union

logger = LogConfig.get_logger()

class ParkingOrderTblHandler:
    """ 讀取寫入 Parking Table 的資料 """
    _db = None

    def __init__(self, db):
        self._db = db

    async def get(self, parking_id, garage_id):
        async with self._db.acquire() as conn:
            try:
                return await self.get_row(conn, parking_id, garage_id)
            except Exception as e:
                logger.error("Exception for getting payment agent table's data from database")
                logger.exception(e)
                return e

    async def get_row(self, conn, parking_id, garage_id):
        """ 從table讀取一筆跟parking id與garage id相符的資料 """
        row_list = [row async for row in await conn.execute(Parking.select()
                                                                        .where(Parking.c.parking_id == int(parking_id))
                                                                        .where(Parking.c.garage_id == int(garage_id)))]

        if row_list:
            return ParkingTblRow(row_list[-1])




# class DevicePaTblHandler:
#     """ 讀取寫入 DevicePaArgs Table 的資料 """
#     _db = None
#
#     def __init__(self, db):
#         self._db = db
#
#     async def get(self, pmsp_garage_id, table_id=None) -> Union[DevicePaTblRow, Exception]:
#         async with self._db.acquire() as conn:
#             try:
#                 return await self.get_row(conn, pmsp_garage_id, table_id)
#             except Exception as e:
#                 logger.error("Exception for getting payment agent garage table's data from database")
#                 logger.exception(e)
#                 return e
#
#     async def get_row(self, conn, pmsp_garage_id, table_id=None) -> DevicePaTblRow:
#         """ 從table讀取一筆跟garage id or id相符的資料 """
#         if table_id is not None:
#             row_list = [row async for row in await conn.execute(DevicePaArgsTable.select()
#                                                                 .where(DevicePaArgsTable.c.id == int(table_id))
#                                                                 .order_by(DevicePaArgsTable.c.id.desc()).limit(1))]
#
#         else:
#             row_list = [row async for row in await conn.execute(DevicePaArgsTable.select()
#                                                                             .where(DevicePaArgsTable.c.pmsp_id == int(pmsp_garage_id))
#                                                                             .order_by(DevicePaArgsTable.c.id.desc()).limit(1))]
#         if row_list:
#             last_row = row_list[0]
#             return DevicePaTblRow(last_row)
#
#     async def add(self, row_data):
#         async with self._db.acquire() as conn:
#             trans = await conn.begin()
#             try:
#                 result = await self.add_row(conn, row_data)
#                 await trans.commit()
#                 return result
#             except Exception as e:
#                 await trans.rollback()
#                 logger.error("Exception for set payment agent device table")
#                 logger.exception(e)
#                 return e
#
#     async def add_row(self, conn, row_data):
#         """ 新增一筆資料到 Table """
#         return await conn.execute(DevicePaArgsTable.insert().values(row_data))
#
#     async def update(self, row_data):
#         async with self._db.acquire() as conn:
#             trans = await conn.begin()
#             try:
#                 result = await self.update_row(conn, row_data)
#                 await trans.commit()
#                 return result
#             except Exception as e:
#                 await trans.rollback()
#                 logger.error("Exception for set payment agent garage table")
#                 logger.exception(e)
#                 return e
#
#     async def update_row(self, conn, row_data):
#         """ 更新資料到 Table """
#         return await conn.execute(DevicePaArgsTable.update().values(row_data).where(DevicePaArgsTable.c.pmsp_id == row_data['pmsp_id']))
#
#     async def delete_row(self, conn, garage_id):
#         return await conn.execute(DevicePaArgsTable.delete().where((DevicePaArgsTable.c.pmsp_id == garage_id)))
#
