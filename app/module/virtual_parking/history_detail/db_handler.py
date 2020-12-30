import aiohttp
import json
from app.config.logger import LogConfig
from app.util.str_helper import StringHelper
from app.config.models import VirtualParkingHistoryDetailTable
from app.module.virtual_parking.history.models import *
import datetime
from typing import Union, List

logger = LogConfig.get_logger()


class HistoryDetailVpTblHandler:
    """ 讀取寫入 VirtualParkingHistoryTable Table 的資料 """
    _db = None

    def __init__(self, db):
        self._db = db

    # async def get_by_table_id(self, table_id) -> Union[List[HistoryVpTblRow], Exception]:
    #     async with self._db.acquire() as conn:
    #         try:
    #             return await self.get_row_by_table_id(conn, table_id)
    #         except Exception as e:
    #             logger.error(f"Exception for getting virtual parking history data by garage id: {table_id}")
    #             logger.exception(e)
    #             return e

    async def add(self, row_data):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                result = await self.add_row(conn, row_data)
                await trans.commit()
                return result
            except Exception as e:
                await trans.rollback()
                logger.error("Exception for add a row for virtual parking history detail table")
                logger.exception(e)
                return e

    # async def update(self, table_id, row_data):
    #     async with self._db.acquire() as conn:
    #         trans = await conn.begin()
    #         try:
    #             result = await self.update_row(conn, table_id, row_data)
    #             await trans.commit()
    #             return result
    #         except Exception as e:
    #             await trans.rollback()
    #             logger.error("Exception for updating virtual parking history table")
    #             logger.exception(e)
    #             return e

    # async def get_row_by_table_id(self, conn, table_id) -> List[HistoryVpTblRow]:
    #     """ 從table讀取一筆跟 id相符的資料 """
    #     row_list = [row async for row in await conn.execute(VirtualParkingHistoryTable.select()
    #                                                         .where(VirtualParkingHistoryTable.c.id == int(table_id))
    #                                                         )]
    #     ret_list = []
    #     for row in row_list:
    #         ret_list.append(HistoryVpTblRow(row))
    #
    #     return ret_list

    async def add_row(self, conn, row_data):
        """ 新增一筆資料到 Table """
        return await conn.execute(VirtualParkingHistoryDetailTable.insert().values(row_data))

    # async def update_row(self, conn, table_id, row_data):
    #     """ 更新一筆資料到 Table """
    #     return await conn.execute(VirtualParkingHistoryTable.update().values(row_data).where(VirtualParkingHistoryTable.c.id == table_id))



