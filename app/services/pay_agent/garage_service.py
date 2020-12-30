from app.services.pay_agent.service_base import *

logger = LogConfig.get_logger()


class PayAgentGarageService(PayAgentServiceBase):
    """ every thing about tablat transaction data"""

    def __init__(self, db, user: Account):
        super().__init__(db, user)

    async def get_pa_garage(self, by_pmsp_garage_id, by_table_id) -> Union[GaragePaTblRow, ErrorMsgBase]:
        """ 讀取支付平台的場站資訊 """
        tb = GaragePaTblHandler(self._db)
        res = await tb.get(by_pmsp_garage_id, by_table_id)
        if isinstance(res, Exception):
            return ApiErrorGeneric.UnexpectedError(f'{res}')
        return res

    async def add_or_update_pa_garage(self, pa_type: PAType, garage_conf_req: PaGarageConfApiReq)-> Union[GaragePaTblRow, ErrorMsgBase]:
        """ reqeust 中的 garage id不存在則新增, 存在則 update """

        get_res = await self.get_pa_garage(garage_conf_req.gId, None)
        if isinstance(get_res, ErrorMsgBase):
            return get_res
        if get_res is None:
            return await self.add_pa_garage(pa_type, garage_conf_req)
        else:
            return await self.update_pa_garage(pa_type, garage_conf_req)


    async def add_pa_garage(self, pa_type: PAType, garage_conf_req: PaGarageConfApiReq) -> Union[GaragePaTblRow, ErrorMsgBase]:
        """ 寫入支付平台的場站資訊 """

        if pa_type != PAType.PKLOT:
            logger.error(f"Not support pa type {pa_type}")
            return ApiErrorPaymentAgent.NotSupportPlatform(f"Not support pa type {pa_type}")

        garage_conf_req.set_pklot_launch(1)

        # 新增一個場站在大聲公伺服器上
        pklot_http = PKLotHttp()
        pklot_add_garage_resp = await pklot_http.add_garage(PKLotHttpReq.GarageConf(garage_conf_req))
        if isinstance(pklot_add_garage_resp, Exception):
            return ApiErrorGeneric.UnexpectedError(f'{pklot_add_garage_resp}')
        if pklot_add_garage_resp.error is not None:
            return ApiErrorPKL.RespDataError(pklot_add_garage_resp.error.title)

        # 產生要寫入 pa garage table 的資料，並寫入table
        row_data = garage_conf_req.gen_pa_garage_tbl_data(self._user, pklot_add_garage_resp)
        tb = GaragePaTblHandler(self._db)
        res = await tb.add(row_data)
        if isinstance(res, Exception):
            return ApiErrorGeneric.UnexpectedError(f'{res}')

        # 讀取剛寫進的 garage_pa_args table 的資料並且回傳
        check_res = await self.get_pa_garage(None, res.lastrowid)
        if isinstance(check_res, ErrorMsgBase):
            return check_res

        if check_res is None:
            logger.error(f"Can not found the garage pa data we added: last row id: {res.lastrowid}")
            apiError = ApiErrorGeneric.UnexpectedError(f"找不到剛新增的PA場站資料, last row id: {res.lastrowid}")
            return apiError

        return check_res


    async def update_pa_garage(self, pa_type: PAType, garage_conf_req: PaGarageApiReqBase, pklot_garage_id=None) -> Union[GaragePaTblRow, ErrorMsgBase]:
        """ 更新支付平台的場站資訊 """
        if pa_type != PAType.PKLOT:
            logger.error(f"Not support pa type {pa_type}")
            return ApiErrorPaymentAgent.NotSupportPlatform(f"Not support pa type {pa_type}")

        if pklot_garage_id is None:
            # 由pmsp garage id 找到 pklot garage id
            get_res = await self.get_pa_garage(garage_conf_req.gId, None)
            if isinstance(get_res, ErrorMsgBase):
                return get_res
            if get_res is None:
                logger.error(f"Failed to find the pa garage conf by pmsp garage id: {garage_conf_req.gId}")
                error = ApiErrorPaymentAgent.NotFoundGaragePA(f"Failed to find the pa garage conf by pmsp garage id: {garage_conf_req.gId}")
                return error

            pklot_garage_id = get_res.pklotId

        pklot_http = PKLotHttp()
        if isinstance(garage_conf_req, PaGarageConfApiReq):
            # 更新大聲公伺服器上的場站
            http_resp = await pklot_http.update_garage(PKLotHttpReq.GarageConf(garage_conf_req), pklot_garage_id)
        elif isinstance(garage_conf_req, PaGarageLaunchApiReq):
            # 上架大聲公的場站
            http_resp = await pklot_http.launch_garage(PKLotHttpReq.GarageLaunch(garage_conf_req), pklot_garage_id)

        if isinstance(http_resp, Exception):
            return ApiErrorGeneric.UnexpectedError(f'{http_resp}')
        if http_resp.error is not None:
            return ApiErrorPKL.RespDataError(http_resp.error.title)

        tbl = GaragePaTblHandler(self._db)

        row_data = garage_conf_req.gen_pa_garage_tbl_data(self._user)
        res = await tbl.update(row_data)
        if isinstance(res, Exception):
            return ApiErrorGeneric.UnexpectedError(f'{res}')

        # 讀取剛更新的 garage_pa_args table 的資料並且回傳
        check_res = await self.get_pa_garage(garage_conf_req.gId, None)
        if isinstance(check_res, ErrorMsgBase):
            return check_res

        if check_res is None:
            logger.error(f"Can not found the garage pa data we updated: pmsp garage id: {garage_conf_req.gId}")
            apiError = ApiErrorGeneric.UnexpectedError(f"找不到剛更新的場站資料, pmsp garage id: {garage_conf_req.gId}")
            return apiError

        return check_res

    async def delete_pa_garage_by_id(self, garage_id, conn):
        """ 刪除支付平台的場站設定 """
        account_id = self._user.account_id
        tbl = GaragePaTblHandler(self._db)
        res = await tbl.delete_row(conn, garage_id)
        if not isinstance(res, Exception):
            logger.info(f'Delete pay_agent garage id: {garage_id} by account id: {account_id}')
            self._syslog['create_account_id'] = account_id
            self._syslog['event_id'] = SystemEventType.DELETE_INFO.value
            self._syslog['event_message'] = f'Delete pay_agent garage id: {garage_id} by account id: {account_id}'
            await self._log_service.addlog(self._syslog)
            return True
        else:
            logger.error('Failed to delete pay_agent garage id: {garage_id} by account id: {account_id}')
            return False


