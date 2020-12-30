import jwt,json
from datetime import datetime, timedelta
from sqlalchemy import desc,func,text
from sqlalchemy.orm import Session,sessionmaker
from app.config.models import Account
from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler
from app.services.device_ibox_service import DeviceIboxService
from app.services.device_pv3_service import DevicePv3Service
from app.services.device_event_service import DeviceEventService

class DeviceManager:
    """ management all garage related service """
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None
    device_ibox_service: DeviceIboxService = None
    device_pv3_service: DevicePv3Service = None 
    device_event_service: DeviceEventService = None
    
    def __init__(self, db, user: Account):
        self._db = db
        self._log_service = SystemlogService(self._db)
        self._syslog = {}
        self._user = user
        self.device_ibox_service = DeviceIboxService(self._db, self._user)
        self.device_pv3_service = DevicePv3Service(self._db, self._user)
        self.device_event_service = DeviceEventService(self._db, self._user)

    async def get_device_event(self) -> []:
        return await self.device_event_service.get_device_event()

    async def add_device_event(self, device_event: dict):
        return await self.device_event_service.add_device_event(device_event)

    async def device_export(self, data: dict, device_type: str):
        print("現在觀察匯出")
        if await self.is_args_exist(data, device_type):
            print("資料正確")
            print(data["garage_id"])
            # print(car_type)
            # print(car_type)
            if "iBox" == device_type:
                await self.device_ibox_service.device_export(data)
            if "PV3" == device_type:
                await self.device_pv3_service.device_export(data)
            # !!費率暫時關閉!!
            # await self.fee_service.build_csv(data["garage_id"], car_type)
        else:
            print("有錯")
        return True
    
    async def export_all_device_by_same_device(self, data: dict, device_type: str):
        print(data["garage_id"])
        print(device_type)
        print(data)
        device_id_list = data['device_id_list']
        # 用迴圈 把所有id都執行一次device_export
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@', device_id_list)
        if device_type == "iBox":
            for id in device_id_list:
                data['device_ibox_args_id'] = id
                await self.device_ibox_service.device_export(data)
        elif device_type == "PV3":
            for id in device_id_list:
                data['device_pv3_args_id'] = id
                await self.device_pv3_service.device_export(data)
        return True


    async def is_args_exist(self, data: dict, device_type: str):
        # !!費率暫時關閉!!
        # flag1 = await self.fee_service.get_fee_args(data["garage_id"], car_type)
        # flag1 = flag1["status"]
        # if not flag1:
        #     raise Exception("費率參數尚未設定 請先設定費率")
        if device_type == "iBox":
            flag2 = await self.device_ibox_service.is_ibox_args_exists(data["customer_id"], data["garage_id"], data["device_ibox_args_id"])
            if not flag2:
                raise Exception("iBox參數尚未設定")
        if device_type == "PV3":
            flag2 = await self.device_pv3_service.is_pv3_args_exists(data["customer_id"], data["garage_id"], data["device_pv3_args_id"])
            if not flag2:
                raise Exception("PV3參數尚未設定")
        # TODO PAD CASE
        return True

    async def download_device_parameter(self, data: dict, device_type: str):
        print("現在觀察下載")
        if await self.is_args_exist(data, device_type):
            print("資料正確")
            print(data["garage_id"])
            path = None
            if "iBox" == device_type:
                path = await self.device_ibox_service.download_device_parameter(data)
            if "PV3" == device_type:
                path = await self.device_pv3_service.download_device_parameter(data)
            return path
            # !!費率暫時關閉!!
            # await self.fee_service.build_csv(data["garage_id"], car_type)
        else:
            print("有錯")
        return True

    async def save_customer_map_card_case(self, post_data: dict):
        for i in post_data:
            customer_id = post_data[i]["customer_id"]
            device_type = post_data[i]["device_type"]
            result = True
            if "iBox" == i:
                if "card_case" in post_data[i]:
                    card_case = post_data[i]["card_case"]       
                    result1 = await self.device_ibox_service.save_customer_map_card_case(customer_id, card_case, device_type)
                    result = result & result1
                if "bean" in post_data[i]:
                    bean = post_data[i]["bean"]
                    bean["update_user"] = self._user["account"]
                    bean["update_time"] = datetime.now()
                    result2 = await self.device_ibox_service.save_customer_device_args(customer_id, bean, device_type)
                    result = result & result2
            if "PV3" == i:
                if "card_case" in post_data[i]:
                    card_case = post_data[i]["card_case"]       
                    result3 = await self.device_pv3_service.save_customer_map_card_case(customer_id, card_case, device_type)
                    result = result & result3
                if "bean" in post_data[i]:
                    bean = post_data[i]["bean"]
                    bean["update_user"] = self._user["account"]
                    bean["update_time"] = datetime.now()
                    result4 = await self.device_pv3_service.save_customer_device_args(customer_id, bean, device_type)
                    result = result & result4
        return result
    