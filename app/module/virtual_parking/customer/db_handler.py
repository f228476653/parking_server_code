import aiohttp
import json
from app.config.logger import LogConfig
from app.util.str_helper import StringHelper
from app.config.models import CustomerVpArgsTable
from app.module.virtual_parking.customer.models import *
import datetime
from typing import Union, List

logger = LogConfig.get_logger()


class CustomerVpTblHandler:
    """ 讀取寫入 CustomerVpArgsTable Table 的資料 """
    _db = None

    def __init__(self, db):
        self._db = db

    async def get(self, pmsp_customer_id, table_id=None) -> Union[List[CustomerVpTblRow], Exception]:
        async with self._db.acquire() as conn:
            try:
                return await self.get_row(conn, pmsp_customer_id, table_id)
            except Exception as e:
                logger.error(f"Exception for getting customer virtual parking data by customer id: {customer_id}")
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
                logger.error("Exception for add a row for customer virtual parking table")
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
                logger.error("Exception for updating customer virtual parking table")
                logger.exception(e)
                return e

    async def delete(self, customer_id):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                result = await self.delete_row(conn, customer_id)
                await trans.commit()
                return result
            except Exception as e:
                await trans.rollback()
                logger.error("Exception for deleting customer virtual parking table")
                logger.exception(e)
                return e

    async def get_row(self, conn, customer_id, table_id) -> List[CustomerVpTblRow]:
        """ 從table讀取一筆跟 id相符的資料 """
        if table_id is not None:
            row_list = [row async for row in await conn.execute(CustomerVpArgsTable.select()
                                                            .where(CustomerVpArgsTable.c.id == int(table_id))
                                                            .order_by(CustomerVpArgsTable.c.customer_id.desc()).limit(1))]

        else:
            row_list = [row async for row in await conn.execute(CustomerVpArgsTable.select()
                                                            .where(CustomerVpArgsTable.c.customer_id == int(customer_id))
                                                            .order_by(CustomerVpArgsTable.c.customer_id.desc()).limit(1))]
        ret_list = []
        for row in row_list:
            ret_list.append(CustomerVpTblRow(row))

        return ret_list

    async def add_row(self, conn, row_data):
        """ 新增一筆資料到 Table """
        return await conn.execute(CustomerVpArgsTable.insert().values(row_data))

    async def update_row(self, conn, row_data):
        """ 更新一筆資料到 Table """
        return await conn.execute(CustomerVpArgsTable.update().values(row_data).where(CustomerVpArgsTable.c.customer_id == row_data['customer_id']))

    async def delete_row(self, conn, customer_id):
        """ 刪除一筆資料 """
        return await conn.execute(CustomerVpArgsTable.delete().where((CustomerVpArgsTable.c.customer_id == customer_id)))


