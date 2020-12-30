from app.util.str_helper import StringHelper
from app.config.models import Account
import json
import enum
import datetime
from typing import List
import abc


class HistoryVpTblRow:
    """ virtual parking history table的資料 """

    def __init__(self, row_data):
        self.id = row_data.id
        self.customerId = row_data.customer_id
        self.garageId = row_data.garage_id
        self.pointType = row_data.point_type
        self.points = row_data.points
        self.pointsCompensation = row_data.points_compensation
        self.validTimeStart = row_data.valid_time_start
        self.validTimeEnd = row_data.valid_time_end
        self.status = row_data.status
        self.updateAccountId = row_data.update_account_id
        self.updateTime = row_data.update_time
        self._parsing(row_data)

    def _parsing(self, row_data):
        pass

class HistoryVpApiReqBase(abc.ABC):
    @abc.abstractmethod
    def gen_vp_history_tbl_data(self):
        return NotImplemented

    def gen_resp(self, row_data: HistoryVpTblRow):
        """ 產生 Api 要回复資料 """
        resp = {}
        resp['id'] = row_data.id
        resp['customer_id'] = row_data.customerId
        resp['garage_id'] = row_data.garageId
        resp['points'] = row_data.points
        resp['point_type'] = row_data.pointType
        resp['points_compensation'] = row_data.pointsCompensation
        resp['valid_time_start'] = row_data.validTimeStart
        resp['valid_time_end'] = row_data.validTimeEnd
        resp['status'] = row_data.status
        resp['update_account_id'] = row_data.updateAccountId
        resp['update_time'] = row_data.updateTime

        return resp


class HistoryAddVpApiReq(HistoryVpApiReqBase):
    """ add virtual parking history request 格式的 parser跟轉換成  table 的資料 """

    def __init__(self, json_data, account: Account):
        self.cId = json_data.get('customer_id')
        self.gId = json_data.get('garage_id', None)
        self.pointType = json_data.get('point_type')
        self.points = json_data.get('points')
        self.pointsCompensation = json_data.get('points_compensation')
        self.validTimeStart = json_data.get('valid_time_start')
        self.validTimeEnd = json_data.get('valid_time_end')
        self.remark = json_data.get('remark', '')
        self.accountId = account.account_id

        if self.pointType == 2 and self.gId is None:
            raise Exception('新增VP點數為場站類型，但沒有場站ID')


    def gen_vp_history_tbl_data(self):
        """ 產生可以直接寫入history_virtual_parking table的資料 """
        row_data = {}

        row_data['status'] = 0
        row_data['customer_id'] = self.cId
        row_data['garage_id'] = self.gId
        row_data['point_type'] = self.pointType
        row_data['points'] = self.points
        row_data['points_compensation'] = self.pointsCompensation
        row_data['valid_time_start'] = self.validTimeStart
        row_data['valid_time_end'] = self.validTimeEnd
        row_data['update_account_id'] = self.accountId
        row_data['update_time'] = datetime.datetime.utcnow()

        return row_data

    def gen_vp_history_detail_tbl_data(self, id):
        """ 產生可以直接寫入history_detail_virtual_parking table的資料 """
        row_data = self.gen_vp_history_tbl_data()
        del row_data['customer_id']
        del row_data['garage_id']
        del row_data['point_type']
        row_data['history_id'] = id
        row_data['remark'] = self.remark
        return row_data


class HistoryUpdateVpApiReq(HistoryVpApiReqBase):
    """ add virtual parking history request 格式的 parser跟轉換成  table 的資料 """

    def __init__(self, json_data, account: Account):
        self.id = int(json_data.get('id'))
        self.points = json_data.get('points')
        self.pointsCompensation = json_data.get('points_compensation')
        self.validTimeStart = json_data.get('valid_time_start')
        self.validTimeEnd = json_data.get('valid_time_end')
        self.status = json_data.get('status')
        self.remark = json_data.get('remark', '')
        self.accountId = account.account_id

    def gen_vp_history_tbl_data(self):
        """ 產生可以直接寫入history_virtual_parking table的資料 """
        row_data = {}

        row_data['status'] = self.status
        row_data['points'] = self.points
        row_data['points_compensation'] = self.pointsCompensation
        row_data['valid_time_start'] = self.validTimeStart
        row_data['valid_time_end'] = self.validTimeEnd
        row_data['update_account_id'] = self.accountId
        row_data['update_time'] = datetime.datetime.utcnow()

        return row_data

    def gen_vp_history_detail_tbl_data(self):
        """ 產生可以直接寫入history_detail_virtual_parking table的資料 """
        row_data = self.gen_vp_history_tbl_data()
        row_data['history_id'] = self.id
        row_data['remark'] = self.remark
        return row_data


class HistoryVpQueryApiReq:
    """ get virtual parking history request 格式的 parser跟轉換成  table 的資料 """

    def __init__(self, json_data, account: Account):
        self.cId = json_data.get('customer_id', None)
        if self.cId == 'undefined':
            self.cId = None
        if self.cId is not None:
            self.cId = int(self.cId)

        self.gId = json_data.get('garage_id', None)
        if self.gId == 'undefined':
            self.gId = None
        if self.gId is not None:
            self.gId = int(self.gId)

        self.startValidDateFrom = f"{json_data.get('start_valid_date_from', None)} 00:00:00" \
            if json_data.get('start_valid_date_from', None) is not None else None

        self.startValidDateEnd = f"{json_data.get('start_valid_date_end', None)} 23:59:59" \
            if json_data.get('start_valid_date_end', None) is not None else None

        self.endValidDateFrom = f"{json_data.get('end_valid_date_from', None)} 00:00:00" \
            if json_data.get('end_valid_date_from', None) is not None else None

        self.endValidDateEnd = f"{json_data.get('end_valid_date_end', None)} 23:59:59" \
            if json_data.get('end_valid_date_end', None) is not None else None

        self.status = json_data.get('status', None)
        self.accountId = account.account_id


class HistoryDetailVpQueryApiReq:
    """ get virtual parking detail history request 格式的 parser跟轉換成  table 的資料 """

    def __init__(self, json_data, account: Account):
        self.cId = int(json_data.get('customer_id'))
        self.hId = int(json_data.get('vp_history_id'))
        self.account = account




