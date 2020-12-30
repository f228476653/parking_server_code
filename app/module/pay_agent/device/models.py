from app.util.str_helper import StringHelper
from app.config.models import Account
import json
import enum
import datetime
from typing import List
import abc


class DevicePaTblRow:
    """ payment agent garage tb的資料 """

    def __init__(self, row_data):
        self.id = row_data.device_pa_args_id
        self.garageId = row_data.garage_id
        self.deviceType = row_data.device_type
        self.deviceUserCode = row_data.device_user_code
        self.deviceName = row_data.device_name
        self.updateUser = row_data.update_user
        self.updateTime = row_data.update_time
        self._parsing(row_data)

    def _parsing(self, row_data):
        pass


class PaDeviceConfApiReq:
    """ pa_device API config request 格式的parser跟轉換成 garage_pa_args table 的資料 """

    def __init__(self, json_data, account: Account):
        self.accountId = int(account.account_id)
        self.gId = int(json_data['garage_id'])

        self.id = json_data['id'] if (type(json_data.get('id', None)) is int) is True else None

        self.deviceType = int(json_data['order_device_type'])
        self.deviceUserCode = json_data['device_user_code']
        self.deviceName = json_data['device_name']

    def gen_pa_device_tbl_data(self):
        """ 產生可以直接寫入device_pa_args table的資料 """
        row_data = {}

        row_data['garage_id'] = self.gId
        row_data['device_type'] = self.deviceType
        row_data['device_user_code'] = self.deviceUserCode
        row_data['device_name'] = self.deviceName
        row_data['update_time'] = datetime.datetime.utcnow()
        row_data['update_user'] = self.accountId

        return row_data


class PaGetDevByTypeApiReq:
    """ get pay_agent devices by device type request 回复的資料 """

    def gen_resp(self, rows_data: List[DevicePaTblRow]):
        """ 產生Api回复資料 """
        resp_list = []
        for row_data in rows_data:
            row = {}
            row['id'] = row_data.id
            row['device_name'] = row_data.deviceName
            row['device_user_code'] = row_data.deviceUserCode
            row['order_device_type'] = row_data.deviceType
            resp_list.append(row)

        return resp_list





