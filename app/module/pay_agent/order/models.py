from app.util.str_helper import StringHelper
from app.config.models import Account
import json
import enum
import datetime
from typing import Union
import abc
from app.module.virtual_parking.garage.models import *
from app.module.virtual_parking.customer.models import *
from app.custom_errors.api_error_data import *

class ParkingTblRow:
    def __init__(self, row_data):
        self.pklotOrderId = row_data.pklot_order_id
        self.pklotMember = row_data.pklot_member
        self.enterTime: datetime = row_data.enter_time
        self.plateNum = row_data.vehicle_identification_number
        self.paidTime = row_data.paid_time
        self.record_status = row_data.record_status

    def is_pklot_member(self) -> Union[bool, None]:
        if self.pklotMember == 1:
            return True
        elif self.pklotMember == 0:
            return False
        else:
            return None

    def already_succ_paid(self):
        if (self.paidTime != '0000-00-00 00:00:00' and self.paidTime != None) and self.record_status == 1:
            return True
        else:
            return False

class PaEntryApiReq:
    """ pa_entry API request 格式的Parser跟轉換成transaction table 的資料 """

    def __init__(self, json_data, account: Account):
        self.accountId = int(account.account_id)
        self.gId = int(json_data['garage_id'])
        self.strDatetime = json_data['entry_datetime']
        self.intDateTime = StringHelper.date_str_to_timestamp(self.strDatetime)
        self.plateNumber = json_data['plate_number']
        self.deviceType = json_data.get('device_type', 30)
        self.supportPKLot = json_data.get('support_pklot', True)
        if self.supportPKLot is None:
            self.supportPKLot = True

    def gen_transac_tbl_data(self, account: Account, pklot_resp):
        """ 產生可以直接寫入real_time_transaction table的資料 """
        entry_data = {}
        transaction_data = {}

        entry_data["in_or_out_datetime"] = self.strDatetime
        entry_data["garage_id"] = str(self.gId)
        entry_data["customer_id"] = str(self.cId)
        entry_data["create_account_id"] = str(self.accountId)
        entry_data["vehicle_identification_number"] = self.plateNumber
        entry_data["device_type"] = self.deviceType

        if pklot_resp is not None:
            entry_data["pklot_order_id"] = pklot_resp.orderId
            entry_data["pklot_member"] = pklot_resp.isMember

        entry_data["in_or_out"] = "0"
        entry_data["parking_type"] = "0"
        entry_data["card_id_16"] = 0

        entry_data["pay_datetime"] = "0000-00-00 00:00:00"
        entry_data["card_type"] = "0"
        entry_data["receivable"] = "0"
        entry_data["real_fees"] = "0"
        entry_data["before_pay_balance"] = "0"
        entry_data["is_disability"] = "0"
        entry_data["device_ip"] = ""

        entry_data["discount_type"] = "0"
        entry_data["discount_amount"] = "0"
        entry_data["status_number"] = "0"
        entry_data["vehicle_type"] = "1"
        entry_data["card_id_appearance"] = ""
        entry_data["is_autoload"] = "0"
        entry_data["autoload_amout"] = "0"
        entry_data["parking_id"] = ""

        entry_data["exit_type_config_detail_id"] = "0"
        entry_data["exit_type_config_detail_remarks"] = ""
        entry_data["record_status"] = "1"

        transaction_data["transaction"] = entry_data

        return transaction_data

    def set_garage_customer_id(self, c_id):
        self.cId = c_id

class PaPayOrderApiReq:
    """ pa_pay_order API request 格式的Parser跟轉換成transaction table 的資料 """

    def __init__(self, json_data, account: Account):
        self.accountId = int(account.account_id)
        self.gId = int(json_data['garage_id'])
        self.strDatetime = json_data['check_out_datetime']
        self.intDateTime = StringHelper.date_str_to_timestamp(self.strDatetime)
        self.parkingId = json_data['parking_id']
        self.deviceType = json_data.get('device_type', 30)
        self.receivable = json_data['receivable_fee'] if json_data['receivable_fee'] is not None else 0
        self.received = json_data['received_fee'] if json_data['received_fee'] is not None else 0
        self.charge = json_data['charge'] if json_data['charge'] is not None else 0
        self.payPlatform = json_data['pay_platform']
        self.deviceCode = json_data['dev_code']
        self.deviceName = ""
        self.deductRule = None
        self.deductPoints = None
        self.deductFrom = None
        self.cardType = None


    def set_device_name(self, dev_name):
        self.deviceName = dev_name

    def set_parking_without_vp(self):
        # 80 為大聲公
        self.cardType = "80"

    def set_parking_with_vp(self, customer_vp: CustomerVpTblRow, garage_vp: GarageVpTblRow, parking_order: ParkingTblRow, paid_succ)\
            -> Union[None, ErrorMsgBase]:
        # 81 為點數扣抵
        self.cardType = "81"
        self.deductFrom = garage_vp.vpDeductFrom
        self.deductRule = garage_vp.vpDeductRule
        if garage_vp.vpDeductFrom == 1:
            self.deductRule = customer_vp.vpDeductRule

        # 不請錢或請款失敗則點數不扣抵
        if self.charge == 0 or paid_succ is False:
            self.deductPoints = 0
        # 金額
        elif self.deductRule == 2:
            self.deductPoints = self.charge
        else:
            utc_enter_time = StringHelper.datetime_to_timestamp(parking_order.enterTime)
            utc_leave_time = self.intDateTime
            diff_time = utc_leave_time - utc_enter_time
            remainder = diff_time % 3600
            quotient = ((diff_time-remainder)//3600)
            deduct_point = quotient

            if remainder != 0:
                deduct_point += 1
                # 每半小時
                if self.deductRule == 0:
                    if remainder <= 1800:
                        deduct_point -= 0.5

            self.deductPoints = deduct_point

        return None

    def gen_transac_tbl_data(self, account: Account, order: ParkingTblRow, paid_succ: bool):
        """ 產生可以直接寫入real_time_transaction table的資料 """
        leave_data = {}
        transaction_data = {}
        only_for_parking = {}

        leave_data["in_or_out_datetime"] = self.strDatetime
        leave_data["garage_id"] = str(self.gId)
        leave_data["customer_id"] = str(self.cId)
        leave_data["create_account_id"] = str(self.accountId)
        leave_data["vehicle_identification_number"] = order.plateNum
        leave_data["device_type"] = self.deviceType

        leave_data["in_or_out"] = "1"
        leave_data["parking_type"] = "0"
        leave_data["card_id_16"] = 0

        leave_data["pay_datetime"] = self.strDatetime

        leave_data["receivable"] = self.receivable
        leave_data["parking_id"] = self.parkingId
        leave_data["device_ip"] = self.deviceCode

        if self.charge != 0:
            leave_data["card_type"] = self.cardType
            if paid_succ:
                leave_data["real_fees"] = self.charge
                leave_data["record_status"] = 1
            else:
                leave_data["real_fees"] = 0
                leave_data["record_status"] = 4
        else:
            leave_data["real_fees"] = self.received
            leave_data["record_status"] = 1
            # 付款方式，99為人工結帳，特約平台上非特約平台的付款方式就先用99
            leave_data["card_type"] = "99"

        leave_data["before_pay_balance"] = "0"
        leave_data["is_disability"] = "0"
        leave_data["discount_type"] = "0"
        leave_data["discount_amount"] = "0"
        leave_data["status_number"] = "0"
        leave_data["vehicle_type"] = "1"
        leave_data["card_id_appearance"] = ""
        leave_data["is_autoload"] = "0"
        leave_data["autoload_amout"] = "0"
        leave_data["exit_type_config_detail_id"] = "0"
        leave_data["exit_type_config_detail_remarks"] = ""

        only_for_parking['device_name'] = self.deviceName
        only_for_parking['vp_deduct_from'] = self.deductFrom
        only_for_parking['vp_deduct_point'] = self.deductPoints
        only_for_parking['vp_deduct_rule'] = self.deductRule

        leave_data["only_for_parking"] = only_for_parking

        transaction_data["transaction"] = leave_data

        return transaction_data

    def set_garage_customer_id(self, c_id):
        self.cId = c_id

