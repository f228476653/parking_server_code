import json
from app.controllers.controller import Controller
from app.config.models import SystemLog,Event
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.systemlog_service import SystemlogService
from app.controllers.api_response import ApiResponse
import time

class SystemlogController(Controller):
    
    async def add_log(self,request):
        db_service = SystemlogService(request.app['pmsdb'])
        post_data = await request.json()
        syslog = post_data.get('system_log')
        syslog['create_account_id']=request['login']['account_id']
        syslog['create_account_id']=0
        result = await db_service.addlog(syslog)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def delall_log(self,request):
        db_service = SystemlogService(request.app['pmsdb'])
        post_data = await request.json()
        syslog = post_data.get('system_log')
        syslog['create_account_id']=request['login']['account_id']
        result = await db_service.delete_alllog(syslog)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())


    async def query_by_message(self,request):
        db_service = SystemlogService(request.app['pmsdb'])
        post_data = await request.json()
        syslog = post_data.get('system_log')
        syslog['create_account_id']=request['login']['account_id']
        result = await db_service.query_by_msg(syslog)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())


    async def query_by_date(self,request):
        db_service = SystemlogService(request.app['pmsdb'])
        post_data = await request.json()
        syslog = post_data.get('system_log')
        syslog['create_account_id']=request['login']['account_id']
        result = await db_service.query_by_date(syslog)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def query_by_event(self,request):
        db_service = SystemlogService(request.app['pmsdb'])
        post_data = await request.json()
        syslog = post_data.get('system_log')
        syslog['create_account_id']=request['login']['account_id']
        result = await db_service.query_by_event(syslog)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def query_SystemEventType(self,request):
        db_service = SystemlogService(request.app['pmsdb'])
        post_data = await request.json()
        syslog = post_data.get('system_log')
        syslog['create_account_id']=request['login']['account_id']
        result = await db_service.query_SystemEventType(syslog)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

