from app.util.str_helper import StringHelper
from app.config.models import Account
import json
import enum
import datetime
from typing import Union
import abc

class PAType(enum.IntEnum):
    PKLOT = 1


class GaragePaTblRow:
    """ payment agent garage tb的資料 """

    def __init__(self, row_data):
        self.id = row_data.id
        self.pklotId = row_data.pklot_id
        self.pmspId = row_data.pmsp_id
        self.pklotName = row_data.pklot_name
        self.pklotAddress = row_data.pklot_address
        self.pklotLat = row_data.pklot_lat
        self.pklotLng = row_data.pklot_lng
        self.pklotCarLots = row_data.pklot_car_lots
        self.pklotMotoLots = row_data.pklot_moto_lots
        self.pklotDisabilityLots = row_data.pklot_disability_lots
        self.pklotGarageDesc = row_data.pklot_garage_desc
        self.pklotCarHeightLimit = row_data.pklot_car_height_limit
        self.pklotPayRule = row_data.pklot_pay_rule
        self.pklotLaunch = row_data.pklot_launch
        self.updateTime = row_data.update_time
        self.updateAccountId = row_data.update_account_id

        self._parsing(row_data)

    def _parsing(self, row_data):
        pay_rule = json.loads(row_data.pklot_pay_rule)[0]
        self.pklotServiceHoursBegin = pay_rule['start_at']
        self.pklotServiceHoursEnd = pay_rule['end_at']
        self.pklotMaxPrice = (float(pay_rule['max_price_cents']))/100 if pay_rule['max_price_cents'] is not None else None

        first_rule = pay_rule['price_units'][0]
        self.pklotMinutesUnit = first_rule['minutes']
        self.pklotPriceUnit = (float(first_rule['price_cents']))/100

    def is_pklot_launch(self) -> bool:
        return True if self.pklotLaunch == 1 else False

class PaGarageApiReqBase(abc.ABC):
    gId = None

    @abc.abstractmethod
    def gen_pa_garage_tbl_data(self, account: Account, pklot_resp=None):
        return NotImplemented

    def gen_resp(self, row_data: GaragePaTblRow):
        """ 產生 Api 要回复資料 """
        resp = {}
        pklot_resp = {}
        pklot_resp['name'] = row_data.pklotName
        pklot_resp['address'] = row_data.pklotAddress
        pklot_resp['lat'] = row_data.pklotLat
        pklot_resp['lng'] = row_data.pklotLng
        pklot_resp['car_lots'] = row_data.pklotCarLots
        pklot_resp['moto_lots'] = row_data.pklotMotoLots
        pklot_resp['disability_lots'] = row_data.pklotDisabilityLots
        pklot_resp['service_hours_begin'] = row_data.pklotServiceHoursBegin
        pklot_resp['serviceHoursEnd'] = row_data.pklotServiceHoursEnd
        pklot_resp['minutes_unit'] = row_data.pklotMinutesUnit
        pklot_resp['price_unit'] = row_data.pklotPriceUnit
        pklot_resp['max_price'] = row_data.pklotMaxPrice
        pklot_resp['car_height_limit'] = row_data.pklotCarHeightLimit
        pklot_resp['garage_desc'] = row_data.pklotGarageDesc
        pklot_resp['launch'] = True if row_data.pklotLaunch == 1 else False

        resp['garage_id'] = row_data.pmspId
        resp['pklot'] = pklot_resp

        return resp


class PaGarageGetApiReq(PaGarageApiReqBase):
    """ pa_garage get API request 格式的parser """

    def __init__(self, customer_id, garage_id):
        self.gId = int(garage_id)

    def gen_pa_garage_tbl_data(self, account: Account, pklot_resp = None):
        """ 產生可以直接寫入garage_pa_args table的資料 """
        row_data = {}
        row_data['pmsp_id'] = self.gId

        return row_data


class PaGarageLaunchApiReq(PaGarageApiReqBase):
    """ pa_garage launch API request 格式的parser跟轉換成 garage_pa_args table 的資料 """

    def __init__(self, json_data, account: Account):
        self.accountId = int(account.account_id)
        self.gId = int(json_data['garage_id'])

        pklot_data = json_data.get('pklot', None)
        self.pklotLaunch = pklot_data['launch'] if pklot_data is not None else None

    def gen_pa_garage_tbl_data(self, account: Account, pklot_resp = None):
        """ 產生可以直接寫入garage_pa_args table的資料 """
        row_data = {}

        if self.pklotLaunch is True:
            row_data['pklot_launch'] = 1
        else:
            row_data['pklot_launch'] = 0

        row_data['pmsp_id'] = self.gId
        row_data['update_time'] = datetime.datetime.utcnow()
        row_data['update_account_id'] = self.accountId

        return row_data

    def gen_resp(self, row_data: GaragePaTblRow):
        """ 產生Api回复資料 """
        resp = {}
        pklot_resp = {}
        pklot_resp['launch'] = True if row_data.pklotLaunch == 1 else False

        resp['garage_id'] = row_data.pmspId
        resp['pklot'] = pklot_resp

        return resp


class PaGarageConfApiReq(PaGarageApiReqBase):
    """ pa_garage API config request 格式的parser跟轉換成 garage_pa_args table 的資料 """

    def __init__(self, json_data, account: Account):
        self.accountId = int(account.account_id)
        self.gId = int(json_data['garage_id'])

        pklot_data = json_data['pklot']
        self.name = pklot_data['name']
        self.address = pklot_data['address']
        self.lat = pklot_data['lat']
        self.lng = pklot_data['lng']
        self.carLots = pklot_data['car_lots']
        self.motoLots = pklot_data['moto_lots']
        self.disabilityLots = pklot_data['disability_lots']
        self.serviceHoursBegin = pklot_data['service_hours_begin']
        self.serviceHoursEnd = pklot_data['service_hours_end']
        self.minutesUnit = pklot_data['minutes_unit']
        self.priceUnit = float(pklot_data['price_unit'])
        max_price = pklot_data.get('max_price', None)
        self.maxPrice = float(max_price) if max_price is not None else None
        self.carHeightLimit = pklot_data.get('car_height_limit', None)
        self.garageDesc = pklot_data.get('garage_desc', None)

    def set_pklot_launch(self, value: int):
        """ 如果是新增場站的話，需要將這個值設為1（因為大聲公新增完場站的預設是上架）"""
        self.pklotLaunch = value

    def gen_pa_garage_tbl_data(self, account: Account, pklot_resp = None):
        """ 產生可以直接寫入garage_pa_args table的資料 """
        row_data = {}

        row_data['pmsp_id'] = self.gId

        if pklot_resp is not None:
            row_data['pklot_id'] = pklot_resp.parkingLotId

        if hasattr(self, 'pklotLaunch'):
            row_data['pklot_launch'] = self.pklotLaunch

        row_data['pklot_name'] = self.name
        row_data['pklot_address'] = self.address
        row_data['pklot_lat'] = self.lat
        row_data['pklot_lng'] = self.lng
        row_data['pklot_car_lots'] = self.carLots
        row_data['pklot_moto_lots'] = self.motoLots
        row_data['pklot_disability_lots'] = self.disabilityLots

        row_data['pklot_garage_desc'] = self.garageDesc
        row_data['pklot_car_height_limit'] = self.carHeightLimit
        row_data['pklot_pay_rule'] = json.dumps(self.gen_pay_rule())

        row_data['update_time'] = datetime.datetime.utcnow()
        row_data['update_account_id'] = self.accountId

        return row_data

    def gen_pay_rule(self) -> list:
        """ 產生寫入garage_pa_args table中pay_rule欄位的資料 """
        max_price_cents = self.maxPrice * 100 if self.maxPrice is not None else None
        return [{"days_of_week": [],
          "for_holiday": False,
          "start_at": self.serviceHoursBegin,
          "end_at": self.serviceHoursEnd,
          "charge_type": "per_unit",
          "price_units": [{"price_cents": self.priceUnit * 100, "minutes": self.minutesUnit}],
          "max_price_cents": max_price_cents,
          "max_price_minutes": 1440,
          "check_in_buffer": 0}]


