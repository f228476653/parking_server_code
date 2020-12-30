from app.services.virtual_parking.service_base import *
from app.module.virtual_parking.history.db_handler import *
from app.module.virtual_parking.regular_report.models import *

logger = LogConfig.get_logger()


class RegularReportVpService(VirtualParkingServiceBase):
    """ every thing about tablat transaction data"""

    def __init__(self, db, user: Account):
        super().__init__(db, user)

    async def get_summary_by_monthly(self, api_req: RegularDailyReportVpApiReq) -> Union[List[dict], ErrorMsgBase]:
        try:
            async with self._db.acquire() as conn:
                cmd = self.sql_cmd_summary_day_orders(api_req, True)
                data = [dict(row.items()) async for row in await conn.execute(cmd)]
        except Exception as e:
            logger.error('Failed to get_summary_by_monthly for regular report')
            logger.exception(e)
            return ApiErrorGeneric.DatabaseError('Failed to get summary with monthly orders')

        return data

    async def get_summary_by_daily(self, api_req: RegularDailyReportVpApiReq) -> Union[List[dict], ErrorMsgBase]:
        try:
            async with self._db.acquire() as conn:
                cmd = self.sql_cmd_summary_day_orders(api_req)
                data = [dict(row.items()) async for row in await conn.execute(cmd)]
        except Exception as e:
            logger.error('Failed to get_summary_by_daily for regular report')
            logger.exception(e)
            return ApiErrorGeneric.DatabaseError('Failed to get summary with daily orders')

        return data

    def sql_cmd_summary_day_orders(self, api_req: RegularDailyReportVpApiReq, by_month = False):
        cmd_day_orders = self.sql_cmd_vp_orders_with_date(api_req, by_month)

        sql_select = f"SELECT" \
                     f" day_orders.paid_date AS date"  \
                     f", count(1) AS count" \
                     f", CAST(SEC_TO_TIME(SUM(day_orders.diff_hours)) AS CHAR) AS diff_hours" \
                     f", CAST(SUM(day_orders.fee) AS SIGNED) AS receivable" \
                     f", CAST(SUM(day_orders.real_fee) AS SIGNED) AS received" \
                     f", SUM(day_orders.deduct_point_garage) AS deduct_points_garage" \
                     f", SUM(day_orders.deduct_point_customer) AS deduct_points_customer" \
                     f", SUM(day_orders.deduct_count_garage) AS deduct_count_garage" \
                     f", SUM(day_orders.deduct_count_customer) AS deduct_count_customer" \
                     f" FROM ({cmd_day_orders}) day_orders"\
                     f" GROUP BY day_orders.paid_date"\
                     f" ORDER BY day_orders.paid_date ASC"

        return sql_select

    def sql_cmd_vp_orders_with_date(self, api_req: RegularDailyReportVpApiReq, by_month = False):
        if by_month:
            sub_date_str = 7
        else:
            sub_date_str = 10

        sql_select = f"SELECT" \
                     f" LEFT(p.paid_time, {sub_date_str}) AS paid_date" \
                     f", (UNIX_TIMESTAMP(p.paid_time) - UNIX_TIMESTAMP(p.enter_time)) AS diff_hours" \
                     f", p.garage_id" \
                     f", p.fee" \
                     f", p.real_fee" \
                     f", IF(p.vp_deduct_from = 0, p.vp_deduct_point, 0) as deduct_point_garage" \
                     f", IF(p.vp_deduct_from = 1, p.vp_deduct_point, 0) as deduct_point_customer" \
                     f", IF(p.vp_deduct_from = 0, 1, 0) as deduct_count_garage" \
                     f", IF(p.vp_deduct_from = 1, 1, 0) as deduct_count_customer" \
                     f" FROM parking p"

        conditions = []
        # conditions.append(f'p.garage_id = {api_req.gId}')
        conditions.append('p.out_device_type = 30')
        conditions.append('p.record_status = 1')
        conditions.append('p.paid_type = "81"')
        if api_req.paid_time_start is not None:
            conditions.append(f'p.paid_time >= "{api_req.paid_time_start}"')

        if api_req.paid_time_end is not None:
            conditions.append(f'p.paid_time <= "{api_req.paid_time_end}"')

        if len(conditions) != 0:
            str_conditions = ' and '.join(conditions)
            sql_select = sql_select + f" WHERE ({str_conditions})"

        garage_condition = ''
        for i, garage_id in enumerate(api_req.gIdList):
            if i == 0:
                garage_condition = f'p.garage_id = {garage_id}'
            else:
                garage_condition = f'{garage_condition} OR p.garage_id = {garage_id}'

        sql_select = f'{sql_select} and ({garage_condition})'

        return sql_select








