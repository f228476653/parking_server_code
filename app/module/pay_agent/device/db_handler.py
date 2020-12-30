import aiohttp
import json
from app.config.logger import LogConfig
from app.util.str_helper import StringHelper
from app.config.models import DevicePaArgsTable
from app.module.pay_agent.device.models import *
import datetime
from typing import Union, List

logger = LogConfig.get_logger()


class DevicePaTblHandler:
    """ 讀取寫入 DevicePaArgs Table 的資料 """
    _db = None

    def __init__(self, db):
        self._db = db

    async def get_by_id(self, table_id) -> Union[List[DevicePaTblRow], Exception]:
        async with self._db.acquire() as conn:
            try:
                return await self.get_row_by_id(conn, table_id)
            except Exception as e:
                logger.error("Exception for getting payment agent device data by id from database")
                logger.exception(e)
                return e

    async def get_by_dev_code(self, g_id, dev_code) -> Union[List[DevicePaTblRow], Exception]:
        async with self._db.acquire() as conn:
            try:
                return await self.get_row_by_dev_code(conn, g_id, dev_code)
            except Exception as e:
                logger.error("Exception for getting payment agent device data by device code from database")
                logger.exception(e)
                return e

    async def get_by_dev_type(self, pmsp_garage_id, dev_type) -> Union[List[DevicePaTblRow], Exception]:
        async with self._db.acquire() as conn:
            try:
                return await self.get_rows_by_dev_type(conn, pmsp_garage_id, dev_type)
            except Exception as e:
                logger.error("Exception for getting payment agent device data by device type from database")
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
                logger.error("Exception for add a row payment agent device table")
                logger.exception(e)
                return e

    async def update(self, table_id, row_data):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                result = await self.update_row(conn, table_id, row_data)
                await trans.commit()
                return result
            except Exception as e:
                await trans.rollback()
                logger.error("Exception for updating payment agent garage table")
                logger.exception(e)
                return e

    async def delete(self, dev_id):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                result = await self.delete_row(conn, dev_id)
                await trans.commit()
                return result
            except Exception as e:
                await trans.rollback()
                logger.error("Exception for deleting payment agent garage table")
                logger.exception(e)
                return e

    async def get_row_by_id(self, conn, table_id) -> List[DevicePaTblRow]:
        """ 從table讀取一筆跟 id相符的資料 """
        row_list = [row async for row in await conn.execute(DevicePaArgsTable.select()
                                                            .where(DevicePaArgsTable.c.device_pa_args_id == int(table_id))
                                                            .order_by(DevicePaArgsTable.c.device_pa_args_id.desc()).limit(1))]
        ret_list = []
        for row in row_list:
            ret_list.append(DevicePaTblRow(row))

        return ret_list

    async def get_row_by_dev_code(self, conn, g_id, dev_code) -> List[DevicePaTblRow]:
        """ 從table讀取一筆跟 id相符的資料 """
        row_list = [row async for row in await conn.execute(DevicePaArgsTable.select()
                                                            .where(DevicePaArgsTable.c.garage_id == int(g_id))
                                                            .where(DevicePaArgsTable.c.device_user_code == str(dev_code))
                                                            .order_by(DevicePaArgsTable.c.device_pa_args_id.desc()).limit(1))]
        ret_list = []
        for row in row_list:
            ret_list.append(DevicePaTblRow(row))

        return ret_list


    async def get_rows_by_dev_type(self, conn, g_id, dev_type) -> List[DevicePaTblRow]:
        """ 從table讀取跟device type相符的資料 """
        row_list = [row async for row in await conn.execute(DevicePaArgsTable.select()
                                                            .where(DevicePaArgsTable.c.garage_id == int(g_id))
                                                            .where(DevicePaArgsTable.c.device_type == int(dev_type))
                                                             )]
        ret_list = []
        for row in row_list:
            ret_list.append(DevicePaTblRow(row))

        return ret_list

    async def add_row(self, conn, row_data):
        """ 新增一筆資料到 Table """
        return await conn.execute(DevicePaArgsTable.insert().values(row_data))

    async def update_row(self, conn, table_id, row_data):
        """ 更新一筆資料到 Table """
        return await conn.execute(DevicePaArgsTable.update().values(row_data).where(DevicePaArgsTable.c.device_pa_args_id == table_id))

    async def delete_row(self, conn,dev_id):
        """ 刪除一筆資料 """
        return await conn.execute(DevicePaArgsTable.delete().where((DevicePaArgsTable.c.device_pa_args_id == dev_id)))


