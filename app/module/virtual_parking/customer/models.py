from app.util.str_helper import StringHelper
from app.config.models import Account
import json
import enum
import datetime
from typing import List
import abc


class CustomerVpTblRow:
    """ customer virtual parking table的資料 """

    def __init__(self, row_data):
        self.id = row_data.id
        self.customerId = row_data.customer_id
        self.vpEnabled = row_data.vp_enable
        self.vpDeductRule = row_data.vp_deduct_rule
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


class CustomerVpApiReqBase(abc.ABC):

    @abc.abstractmethod
    def gen_vp_customer_tbl_data(self, account: Account):
        return NotImplemented

    def gen_resp(self, row_data: CustomerVpTblRow):
        """ 產生 Api 要回复資料 """
        resp = {}
        resp['id'] = row_data.id
        resp['customer_id'] = row_data.customerId
        resp['vp_enable'] = row_data.vpEnabled
        resp['vp_deduct_rule'] = row_data.vpDeductRule
        resp['update_account_id'] = row_data.updateAccountId
        resp['update_time'] = row_data.updateTime

        return resp


class CustomerVpApiReq(CustomerVpApiReqBase):
    """ virtual parking customer API config request 格式的parser跟轉換成  customer_virtual_parking_args 的資料 """

    def __init__(self, json_data, account: Account):
        self.cId = int(json_data['customer_id'])
        self.accountId = int(account.account_id)
        self.vpEnable = json_data['vp_enable']
        self.vpDeductRule = json_data['vp_deduct_rule']

    def gen_vp_customer_tbl_data(self):
        """ 產生可以直接寫入 garage_virtual_parking_args table的資料 """
        row_data = {}

        row_data['customer_id'] = self.cId
        row_data['vp_enable'] = self.vpEnable
        row_data['vp_deduct_rule'] = self.vpDeductRule
        row_data['update_account_id'] = self.accountId
        row_data['update_time'] = datetime.datetime.utcnow()

        return row_data


class CustomerVpGetApiReq(CustomerVpApiReqBase):
    """ virtual parking customer API config request 格式的parser跟轉換成  customer_virtual_parking_args 的資料 """

    def __init__(self, json_data, account: Account):
        self.cId = int(json_data['customer_id'])
        self.accountId = int(account.account_id)

    def gen_vp_customer_tbl_data(self):
        pass

