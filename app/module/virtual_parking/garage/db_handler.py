import aiohttp
import json
from app.config.logger import LogConfig
from app.util.str_helper import StringHelper
from app.config.models import GarageVpArgsTable
from app.module.virtual_parking.garage.models import *
import datetime
from typing import Union, List

logger = LogConfig.get_logger()


class GarageVpTblHandler:
    """ 讀取寫入 GarageVpArgsTable Table 的資料 """
    _db = None

    def __init__(self, db):
        self._db = db

    async def get(self, pmsp_garage_id, table_id=None) -> Union[List[GarageVpTblRow], Exception]:
        async with self._db.acquire() as conn:
            try:
                return await self.get_row(conn, pmsp_garage_id, table_id)
            except Exception as e:
                logger.error(f"Exception for getting garage virtual parking data by garage id: {garage_id}")
                logger.exception(e)
                return e

    async def add(self, row_data):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                result = await self.add_row(conn, row_data)
                await trans.commit()
                return result
            except Exception as e:
                await trans.rollback()
                logger.error("Exception for add a row for garage virtual parking table")
                logger.exception(e)
                return e

    async def update(self, row_data):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                result = await self.update_row(conn, row_data)
                await trans.commit()
                return result
            except Exception as e:
                await trans.rollback()
                logger.error("Exception for updating garage virtual parking table")
                logger.exception(e)
                return e

    async def delete(self, garage_id):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                result = await self.delete_row(conn, garage_id)
                await trans.commit()
                return result
            except Exception as e:
                await trans.rollback()
                logger.error("Exception for deleting garage virtual parking table")
                logger.exception(e)
                return e

    async def get_row(self, conn, pmsp_garage_id, table_id=None) -> List[GarageVpTblRow]:
        """ 從table讀取一筆跟 id相符的資料 """
        if table_id is not None:
            row_list = [row async for row in await conn.execute(GarageVpArgsTable.select()
                                                                .where(GarageVpArgsTable.c.id == int(table_id))
                                                                .order_by(GarageVpArgsTable.c.id.desc()).limit(1))]

        else:
            row_list = [row async for row in await conn.execute(GarageVpArgsTable.select()
                                                            .where(GarageVpArgsTable.c.garage_id == int(pmsp_garage_id))
                                                            .order_by(GarageVpArgsTable.c.garage_id.desc()).limit(1))]
        ret_list = []
        for row in row_list:
            ret_list.append(GarageVpTblRow(row))

        return ret_list

    async def add_row(self, conn, row_data):
        """ 新增一筆資料到 Table """
        return await conn.execute(GarageVpArgsTable.insert().values(row_data))

    async def update_row(self, conn, row_data):
        """ 更新一筆資料到 Table """
        return await conn.execute(GarageVpArgsTable.update().values(row_data).where(GarageVpArgsTable.c.garage_id == row_data['garage_id']))

    async def delete_row(self, conn, garage_id):
        """ 刪除一筆資料 """
        return await conn.execute(GarageVpArgsTable.delete().where((GarageVpArgsTable.c.garage_id == garage_id)))


