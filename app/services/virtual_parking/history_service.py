from app.services.virtual_parking.service_base import *
from app.module.virtual_parking.history.db_handler import *
from app.services.customer_service import *
from app.services.garage_service import *

logger = LogConfig.get_logger()


class HistoryVpService(VirtualParkingServiceBase):
    """ every thing about tablat transaction data"""

    def __init__(self, db, user: Account):
        super().__init__(db, user)

    async def get_vp_history(self, table_id) -> Union[List[HistoryVpTblRow], ErrorMsgBase]:
        """ 讀取VP方案的購買紀錄 """
        tbl = HistoryVpTblHandler(self._db)
        res = await tbl.get_by_table_id(table_id)
        if isinstance(res, Exception):
            return ApiErrorGeneric.UnexpectedError(f'{res}')
        return res

    async def add_vp_points(self, vp_history_add_req: HistoryAddVpApiReq) -> Union[HistoryVpTblRow, ErrorMsgBase]:
        """ 新增VP方案的點數 """
        # 產生要寫入 history virtula parking table 的資料，並寫入table
        tbl = HistoryVpTblHandler(self._db)
        res = await tbl.add(vp_history_add_req)
        if isinstance(res, Exception):
            return ApiErrorGeneric.UnexpectedError(f'{res}')

        check_res = await self.get_vp_history(res.lastrowid)
        if isinstance(check_res, ErrorMsgBase):
            return check_res

        if check_res == []:
            return ApiErrorGeneric.DatabaseError(f'Add vp points is success but can not get data by id {res.lastrowid}')

        return check_res[0]

    async def update_vp_points(self, vp_history_update_req: HistoryUpdateVpApiReq) -> Union[HistoryVpTblRow, ErrorMsgBase]:
        """ 作廢一筆VP方案的點數 """

        #檢查table id是否正確
        row_data = await self.get_vp_history(vp_history_update_req.id)
        if isinstance(row_data, ErrorMsgBase):
            return row_data

        if row_data == []:
            return ApiErrorGeneric.WrongParams(f'找不到與id對應的VP方案紀錄, id:{vp_history_update_req.id}')

        # 產生要寫入 history virtula parking table 的資料，並寫入table
        row_data = vp_history_update_req.gen_vp_history_tbl_data()
        tbl = HistoryVpTblHandler(self._db)

        res = await tbl.update(vp_history_update_req)
        if isinstance(res, Exception):
            return ApiErrorGeneric.UnexpectedError(f'{res}')

        check_res = await self.get_vp_history(vp_history_update_req.id)
        if isinstance(check_res, ErrorMsgBase):
            return check_res

        if check_res == []:
            return ApiErrorGeneric.DatabaseError(
                f'Update vp points is success but can not get data by id {vp_history_update_req.id}')

        return check_res[0]

    async def query_vp_history(self, api_req: HistoryVpQueryApiReq) -> Union[List[dict], ErrorMsgBase]:
        try:
            async with self._db.acquire() as conn:
                cmd = self.sql_cmd_list_vp_history(api_req)
                data = [dict(row.items()) async for row in await conn.execute(cmd)]
        except Exception as e:
            logger.error('Failed to query_vp_history')
            logger.exception(e)
            return ApiErrorGeneric.DatabaseError('Failed to query_vp_history')

        return data

    async def query_vp_detail_history(self, api_req: HistoryDetailVpQueryApiReq) -> Union[List[dict], ErrorMsgBase]:
        try:
            async with self._db.acquire() as conn:
                if api_req.account.customer_id != 0:
                    # 檢查此筆history 資料是不是屬於此token
                    cmd_get_vp_history = self.sql_cmd_get_vp_history_by_id(api_req.hId)
                    vp_h = [dict(row.items()) async for row in await conn.execute(cmd_get_vp_history)]
                    if len(vp_h) != 1:
                        return ApiErrorGeneric.WrongParams(f'There is no vp history data for history id: {api_req.hId}')

                    if vp_h[0]['customer_id'] != api_req.cId:
                        return ApiErrorGeneric.CustomerIdError('vp history customer id != api request token')

                cmd = self.sql_cmd_list_vp_detail_history(api_req)
                data = [dict(row.items()) async for row in await conn.execute(cmd)]
        except Exception as e:
            logger.error('Failed to query_vp_detail_history')
            logger.exception(e)
            return ApiErrorGeneric.DatabaseError('Failed to query_vp_detail_history')

        return data

    def sql_cmd_list_vp_history(self, api_req: HistoryVpQueryApiReq):
        sql_select = f"SELECT *" \
                     f" FROM history_virtual_parking h"

        conditions = []
        if api_req.cId is not None:
            conditions.append(f'h.customer_id = {api_req.cId}')
        if api_req.gId is not None:
            conditions.append(f'h.garage_id = {api_req.gId}')
        if api_req.status is not None:
            conditions.append(f'h.status = {api_req.status}')

        if api_req.startValidDateFrom is not None:
            conditions.append(f'h.valid_time_start >= "{api_req.startValidDateFrom}"')

        if api_req.startValidDateEnd is not None:
            conditions.append(f'h.valid_time_start <= "{api_req.startValidDateEnd}"')

        if api_req.endValidDateFrom is not None:
            conditions.append(f'h.valid_time_end >= "{api_req.endValidDateFrom}"')

        if api_req.endValidDateEnd is not None:
            conditions.append(f'h.valid_time_end <= "{api_req.endValidDateEnd}"')

        if len(conditions) != 0:
            str_conditions = ' and '.join(conditions)
            sql_select = sql_select + f" WHERE ({str_conditions})"

        return sql_select

    def sql_cmd_get_vp_history_by_id(self, history_id):
        sql_select = f"SELECT *" \
                     f" FROM history_virtual_parking h"

        conditions = []
        conditions.append(f'h.id = "{history_id}"')

        if len(conditions) != 0:
            str_conditions = ' and '.join(conditions)
            sql_select = sql_select + f" WHERE ({str_conditions})"

        return sql_select


    def sql_cmd_list_vp_detail_history(self, api_req: HistoryDetailVpQueryApiReq):
        sql_select = f"SELECT *" \
                     f" FROM history_detail_virtual_parking h"

        conditions = []
        conditions.append(f'h.history_id = "{api_req.hId}"')

        if len(conditions) != 0:
            str_conditions = ' and '.join(conditions)
            sql_select = sql_select + f" WHERE ({str_conditions})"

        sql_select += f" ORDER BY `id` DESC"
        return sql_select






