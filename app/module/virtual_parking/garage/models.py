from app.util.str_helper import StringHelper
from app.config.models import Account
import json
import enum
import datetime
from typing import List
import abc


class GarageVpTblRow:
    """ garage virtual parking table的資料 """

    def __init__(self, row_data):
        self.id = row_data.id
        self.customerId = row_data.customer_id
        self.garageId = row_data.garage_id
        self.vpEnabled = row_data.vp_enable
        self.vpDeductRule = row_data.vp_deduct_rule
        self.vpDeductFrom = row_data.vp_deduct_from
        self.updateAccountId = row_data.update_account_id
        self.updateTime = row_data.update_time
        self._parsing(row_data)

    def _parsing(self, row_data):
        pass

    def is_enabled(self):
        if self.vpEnabled == 1:
            return True
        else:
            return False


class GarageVpApiReqBase(abc.ABC):

    @abc.abstractmethod
    def gen_vp_garage_tbl_data(self, account: Account):
        return NotImplemented

    def gen_resp(self, row_data: GarageVpTblRow):
        """ 產生 Api 要回复資料 """
        resp = {}
        resp['id'] = row_data.id
        resp['customer_id'] = row_data.customerId
        resp['garage_id'] = row_data.garageId
        resp['vp_enable'] = row_data.vpEnabled
        resp['vp_deduct_rule'] = row_data.vpDeductRule
        resp['vp_deduct_from'] = row_data.vpDeductFrom
        resp['update_account_id'] = row_data.updateAccountId
        resp['update_time'] = row_data.updateTime

        return resp


class GarageVpApiReq(GarageVpApiReqBase):
    """ virtual parking garage API config request 格式的parser跟轉換成  garage_virtual_parking_args 的資料 """

    def __init__(self, json_data, account: Account, is_update_data=False):
        self.cId = int(json_data['customer_id']) if is_update_data is False else None
        self.accountId = int(account.account_id)
        self.gId = int(json_data['garage_id'])
        self.vpEnable = json_data['vp_enable']
        self.vpDeductRule = json_data.get('vp_deduct_rule', None)
        self.vpDeductFrom = json_data['vp_deduct_from']

    def gen_vp_garage_tbl_data(self, is_update_data=False):
        """ 產生可以直接寫入 garage_virtual_parking_args table的資料 """
        row_data = {}
        if is_update_data is False:
            row_data['customer_id'] = self.cId
        row_data['garage_id'] = self.gId
        row_data['vp_enable'] = self.vpEnable
        row_data['vp_deduct_rule'] = self.vpDeductRule
        row_data['vp_deduct_from'] = self.vpDeductFrom
        row_data['update_account_id'] = self.accountId
        row_data['update_time'] = datetime.datetime.utcnow()

        return row_data


class GarageVpGetApiReq(GarageVpApiReqBase):
    """ virtual parking garage API config request 格式的parser跟轉換成  garage_virtual_parking_args 的資料 """

    def __init__(self, json_data, account: Account):
        self.accountId = int(account.account_id)
        self.gId = int(json_data['garage_id'])

    def gen_vp_garage_tbl_data(self):
        """ 產生可以直接寫入 garage_virtual_parking_args table的資料 """
        pass


