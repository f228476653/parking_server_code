import app.controllers.api_response as ar

class ErrorMsgBase:
    """將 error main-code 跟 error sub-code 組成 Api response error所需要的格式"""
    _mainCode = ""
    _subCode = ""
    _msg = ""
    _detail = ""

    def __init__(self, detail=""):
        self._detail = detail if detail != "" else self._msg

    def api_error(self) -> ar.ApiResponse.Error:
        return ar.ApiResponse.Error(f'{self._mainCode}{self._subCode}', self._msg, self._detail)


class ErrorMainCode:
    generic = "00"
    paymentAgent = "01"
    parkingSpeaker = "11"


class ApiErrorGeneric:
    """一般錯誤的error code"""

    class WrongParams(ErrorMsgBase):
        _mainCode = ErrorMainCode.generic
        _subCode = '001'
        _msg = "輸入參數錯誤"

    class DatabaseError(ErrorMsgBase):
        _mainCode = ErrorMainCode.generic
        _subCode = '002'
        _msg = "資料庫處理錯誤"

    class CustomerIdError(ErrorMsgBase):
        _mainCode = ErrorMainCode.generic
        _subCode = '003'
        _msg = "帳號權限不可對此客戶id資料進行操作"

    class NotFoundOrder(ErrorMsgBase):
        _mainCode = ErrorMainCode.generic
        _subCode = '004'
        _msg = "該場站無此訂單id"

    class UnexpectedError(ErrorMsgBase):
        _mainCode = ErrorMainCode.generic
        _subCode = '999'
        _msg = "意外錯誤"

    class DataNoneTypeError(ErrorMsgBase):
        _mainCode = ErrorMainCode.generic
        _subCode = '005'
        _msg = "NoneType Data"

class RealTimeDataError:
    """付費平台的error code"""

    class RealTimeDataParserFail(ErrorMsgBase):
        _mainCode = ErrorMainCode.paymentAgent
        _subCode = '001'
        _msg = "即時交易資料錯誤"


class ApiErrorPaymentAgent:
    """付費平台的error code"""

    class NotSupportPlatform(ErrorMsgBase):
        _mainCode = ErrorMainCode.paymentAgent
        _subCode = '001'
        _msg = "不支援的特約平台"

    class NotPlatformMember(ErrorMsgBase):
        _mainCode = ErrorMainCode.paymentAgent
        _subCode = '002'
        _msg = "無法請款，車主不是該特約平台的會員"

    class PayFailure(ErrorMsgBase):
        _mainCode = ErrorMainCode.paymentAgent
        _subCode = '003'
        _msg = "請款失敗"

    class OrderIsPaid(ErrorMsgBase):
        _mainCode = ErrorMainCode.paymentAgent
        _subCode = '004'
        _msg = "此訂單已經付過款"

    class NotPayAgentMember(ErrorMsgBase):
        _mainCode = ErrorMainCode.paymentAgent
        _subCode = '005'
        _msg = "非特約平台會員無法請款非零金額"

    class NotFoundGaragePA(ErrorMsgBase):
        _mainCode = ErrorMainCode.paymentAgent
        _subCode = '006'
        _msg = "特約平台上找不到此場站的設定"

    class ChargeParamsWrong(ErrorMsgBase):
        _mainCode = ErrorMainCode.paymentAgent
        _subCode = '007'
        _msg = "已收金額跟請款金額必須擇一，不可同時不為零"

    class DeviceCodeWrong(ErrorMsgBase):
        _mainCode = ErrorMainCode.paymentAgent
        _subCode = '008'
        _msg = "找不到設備代碼對應的設備"

    class LeaveTimeWrong(ErrorMsgBase):
        _mainCode = ErrorMainCode.paymentAgent
        _subCode = '009'
        _msg = "出場時間小於入場時間"


class ApiErrorPKL:
    """大聲公的error code"""

    class CanNotConnect(ErrorMsgBase):
        _mainCode = ErrorMainCode.parkingSpeaker
        _subCode = '001'
        _msg = "無法連線大聲公"

    class RespDataError(ErrorMsgBase):
        _mainCode = ErrorMainCode.parkingSpeaker
        _subCode = '002'
        _msg = "大聲公回應錯誤"


