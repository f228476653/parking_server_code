from app.util.str_helper import StringHelper
from app.config.models import Account
import json
import enum
import datetime
from typing import List
import abc


class RegularDailyReportVpApiReq:

    def __init__(self, json_data, account: Account):
        start_date = json_data.get('start_date', None)
        self.paid_time_start = f"{json_data['start_date']} 00:00:00" if start_date is not None else None
        end_date = json_data.get('end_date', None)
        self.paid_time_end = f"{json_data['end_date']} 23:59:59" if end_date is not None else None
        self.gIdList = json_data['garage_id_list']
        if len(self.gIdList) == 0:
            raise Exception('There is no garage id in the request data')



