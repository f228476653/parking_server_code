from app.module.pay_agent.device.db_handler import *
from app.services.systemlog_service import SystemlogService
from app.services.pay_agent.service_base import *


class PayAgentDeviceService(PayAgentServiceBase):

    def __init__(self, db, user):
        super().__init__(db, user)
    
    async def add_pa_device(self, dev_conf_req: PaDeviceConfApiReq):
        """ 寫入支付平台的設備資訊 """

        # 產生要寫入 pa device table 的資料，並寫入table
        row_data = dev_conf_req.gen_pa_device_tbl_data()
        tbl_handler = DevicePaTblHandler(self._db)
        res = await tbl_handler.add(row_data)
        if isinstance(res, Exception):
            return ApiErrorGeneric.UnexpectedError(f'{res}')
        return res.lastrowid

    async def update_pa_device(self, dev_conf_req: PaDeviceConfApiReq):
        """ 寫入支付平台的設備資訊 """

        # 產生要寫入 pa device table 的資料，並更新table
        row_data = dev_conf_req.gen_pa_device_tbl_data()
        tbl_handler = DevicePaTblHandler(self._db)
        res = await tbl_handler.update(dev_conf_req.id, row_data)
        if isinstance(res, Exception):
            return ApiErrorGeneric.UnexpectedError(f'{res}')
        return res.lastrowid

    async def get_devices_by_dev_type(self, g_id, dev_type):
        """ 讀取跟device type相符的支付平台的設備資訊 """

        tbl_handler = DevicePaTblHandler(self._db)
        res = await tbl_handler.get_by_dev_type(g_id, dev_type)
        if isinstance(res, Exception):
            return ApiErrorGeneric.UnexpectedError(f'{res}')
        return res

    async def get_device_by_dev_id(self, dev_id):
        """ 讀取跟table Id相符的支付平台的設備資訊 """

        tbl_handler = DevicePaTblHandler(self._db)
        res = await tbl_handler.get_by_id(dev_id)
        if isinstance(res, Exception):
            return ApiErrorGeneric.UnexpectedError(f'{res}')
        return res

    async def get_devices_by_dev_code(self, g_id, dev_code):
        """ 讀取跟使用者代碼相符的支付平台的設備資訊 """

        tbl_handler = DevicePaTblHandler(self._db)
        res = await tbl_handler.get_by_dev_code(g_id, dev_code)
        if isinstance(res, Exception):
            return ApiErrorGeneric.UnexpectedError(f'{res}')
        return res

    async def delete_device_by_device_id(self, device_id: int):
        tbl_handler = DevicePaTblHandler(self._db)
        res = await tbl_handler.delete(device_id)

        if not isinstance(res, Exception):
            logger.info(f'Delete pay_agent device id: {device_id} by account id: {self._user.account_id}')
            self._syslog['create_account_id'] = self._user.account_id
            self._syslog['event_id'] = SystemEventType.DELETE_INFO.value
            self._syslog['event_message'] = f'Delete pay_agent garage id: {device_id} by account id: {self._user.account_id}'
            await self._log_service.addlog(self._syslog)
            return True
        else:
            logger.error('Failed to delete pay_agent device id: {device_id} by account id: {self._user.account_id}')
            return False
