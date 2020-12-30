import json
from collections import OrderedDict
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.decorators.authorize import authorize
from app.services.keystore_service import KeystoreService
from keystore.keystore_status_enum import KeystoreStatusEnum
from app.controllers.api_response import ApiResponse
from pprint import pprint
from app.services.exceptions import UserNotExistError,AuthenticationError


class KeystoreController(Controller):
    
    async def new_keystore(self,request):
        db_service = KeystoreService(request.app['pmsdb'])
        post_data = await request.json()
        key = post_data.get('keystore')
        key['create_account_id']=request['login']['account_id']
        result = await db_service.generate_and_save_keystore(key)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def update_keystore(self,request):
        db_service = KeystoreService(request.app['pmsdb'])
        post_data = await request.json()
        key = post_data.get('keystore')
        key['create_account_id']=request['login']['account_id']
        result = await db_service.generate_and_udpate_keystore(key)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())


    async def get_keystores(self,request):
        db_service = KeystoreService(request.app['pmsdb'])
        data = await db_service.get_keystores()
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_keystores_by_customer_id(self,request):
        db_service = KeystoreService(request.app['pmsdb'])
        customer_id=request.match_info['customer_id']
        data = await db_service.get_keystores_by_customer_id(customer_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_keystores_by_id(self,request):
        db_service = KeystoreService(request.app['pmsdb'])
        id=request.match_info['id']
        data = await db_service.get_keystores_by_id(id)
        result = ApiResponse([dict(data)][0])
        return self.json_response(result.asdict())

    async def get_keystore_status(self,request):
        api_response=ApiResponse(KeystoreStatusEnum.asdict())
        return self.json_response(api_response.asdict())

    async def delete_keystore_by_id(self,request):
        db_service = KeystoreService(request.app['pmsdb'])
        id=request.match_info['id']
        result = await db_service.delete_keystore_by_id(id,request['login']['account_id'])
        if result is None:
            return self.json_handler([])
        else:
            return self.json_response(result)

    async def get_pad_config_by_key(self,request):
        """
        Description Key
        ---
        tags:
        - Key
        summary: 使用啟動碼，取得場站設定
        description: 使用啟動碼，取得場站設定
        operationId: app.controllers.keystore_controller.get_pad_config_by_key
        produces:
        - application/json
        parameters:
        - in: path
          name: key
          description: 啟動碼
          required: true
          schema:
            type: string      
        """
        db_service = KeystoreService(request.app['pmsdb'])
        inital_key = request.match_info['key']
        result = await db_service.get_pad_config_by_key(inital_key)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def encrypt_key_for_pad_config(self,request):
        """
        Description Key
        ---
        tags:
        - Key
        summary: 產生啟動碼
        description: 產生啟動碼
        operationId: app.controllers.keystore_controller.encrypt_key_for_pad_config
        produces:
        - application/json
        parameters:
        - in: header
          description: login Token
          name: Authorization
          schema:
            type: string
          required: true
        - in: path
          name: garage_id
          description: ID of garage
          required: true
          schema:
            type: string
        - in: path
          name: device_key
          description: key of device
          required: true
          schema:
            type: string         
        """
        db_service = KeystoreService(request.app['pmsdb'])
        garage_id = request.match_info['garage_id']
        device_key = request.match_info['device_key']
        print(garage_id)
        print(device_key)
        result = await db_service.encrypt_key_for_pad_config(garage_id,device_key,request['login']['account_id'])
        api_response=ApiResponse(result)   
        return self.json_response(api_response.asdict())



    

    
