import aiohttp
import json
from app.config.logger import LogConfig
from app.config.models import GaragePaArgsTable, Parking
from app.util.str_helper import StringHelper
import datetime
from typing import Union
from app.module.pay_agent.garage.models import *

logger = LogConfig.get_logger()


class GaragePaTblHandler:
    """ 讀取寫入 GaragePaArgs Table 的資料 """
    _db = None

    def __init__(self, db):
        self._db = db

    async def get(self, pmsp_garage_id, table_id=None) -> Union[GaragePaTblRow, Exception]:
        async with self._db.acquire() as conn:
            try:
                return await self.get_row(conn, pmsp_garage_id, table_id)
            except Exception as e:
                logger.error("Exception for getting payment agent garage table's data from database")
                logger.exception(e)
                return e

    async def get_row(self, conn, pmsp_garage_id, table_id=None) -> GaragePaTblRow:
        """ 從table讀取一筆跟garage id or id相符的資料 """
        if table_id is not None:
            row_list = [row async for row in await conn.execute(GaragePaArgsTable.select()
                                                                .where(GaragePaArgsTable.c.id == int(table_id))
                                                                .order_by(GaragePaArgsTable.c.id.desc()).limit(1))]

        else:
            row_list = [row async for row in await conn.execute(GaragePaArgsTable.select()
                                                                            .where(GaragePaArgsTable.c.pmsp_id == int(pmsp_garage_id))
                                                                            .order_by(GaragePaArgsTable.c.id.desc()).limit(1))]
        if row_list:
            last_row = row_list[0]
            return GaragePaTblRow(last_row)

    async def add(self, row_data):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                result = await self.add_row(conn, row_data)
                await trans.commit()
                return result
            except Exception as e:
                await trans.rollback()
                logger.error("Exception for set payment agent garage table")
                logger.exception(e)
                return e

    async def add_row(self, conn, row_data):
        """ 新增一筆資料到 Table """
        return await conn.execute(GaragePaArgsTable.insert().values(row_data))

    async def update(self, row_data):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                result = await self.update_row(conn, row_data)
                await trans.commit()
                return result
            except Exception as e:
                await trans.rollback()
                logger.error("Exception for set payment agent garage table")
                logger.exception(e)
                return e

    async def update_row(self, conn, row_data):
        """ 更新資料到 Table """
        return await conn.execute(GaragePaArgsTable.update().values(row_data).where(GaragePaArgsTable.c.pmsp_id == row_data['pmsp_id']))

    async def delete_row(self, conn, garage_id):
        return await conn.execute(GaragePaArgsTable.delete().where((GaragePaArgsTable.c.pmsp_id == garage_id)))

