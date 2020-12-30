from app.util.str_helper import StringHelper
from app.config.models import Account
import json
import enum
import datetime
from typing import List
import abc


class HistoryDetailVpTblRow:
    """ virtual parking history table的資料 """

    def __init__(self, row_data):
        self.id = row_data.id
        self.historyId = row_data.history_id
        self.customerId = row_data.customer_id
        self.garageId = row_data.garage_id
        self.pointType = row_data.point_type
        self.points = row_data.points
        self.pointsCompensation = row_data.points_compensation
        self.validTimeStart = row_data.valid_time_start
        self.validTimeEnd = row_data.valid_time_end
        self.status = row_data.status
        self.updateAccountId = row_data.update_account_id
        self.remark = row_data.remark
        self.updateTime = row_data.update_time
        self._parsing(row_data)

    def _parsing(self, row_data):
        pass



