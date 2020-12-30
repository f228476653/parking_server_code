import json
from datetime import datetime
from app.controllers.controller import Controller
from app.config.models import Account
from app.util.console_helper import ConsoleHelper
from app.util.encrypt_helper import EncryptHelper
from app.decorators.authorize import authorize
from app.decorators.check_customer_authorization import check_customer_authorization
from app.services.user_service import UserService
from app.controllers.api_response import ApiResponse

class UserController(Controller):
    
    
    async def get_users(self,request):
        #region doc
        """
        Description get all users according to a logged on user
        ---
        tags:
        - Users
        summary: get user list
        description: get user list.
        operationId: app.controllers.user_controller.get_users
        produces:
        - application/json
        parameters:
        - in: header
          name: Authorization
          schema:
            type: string
          required: true
        responses:
          "200":
             class::api_response
        """
        #endregion
        user_service = UserService(request.app['pmsdb'],request['login'])
        accounts = await user_service.get_users()
        api_response=ApiResponse(accounts)
        return self.json_response(api_response.asdict())

    async def is_account_exist(self,request):
        account=request.match_info['account']
        user_service = UserService(request.app['pmsdb'],request['login'])
        result = await user_service.is_account_exist(account)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())
        
    async def get_users_by_customer_id(self,request):
        customer_id=request.match_info['customer_id']
        db_service = UserService(request.app['pmsdb'],request['login'])
        data = await db_service.get_users_by_customer_id(customer_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())
    
    async def get_users_by_customer_id_with_system_account(self,request):
        customer_id=request.match_info['customer_id']
        db_service = UserService(request.app['pmsdb'],request['login'])
        data = await db_service.get_users_by_customer_id_with_system_account(customer_id)
        api_response=ApiResponse(data)
        return self.json_response(api_response.asdict())

    async def get_user_by_id(self,request):
        """ get account by account_id """
        id=request.match_info['id']
        user_service = UserService(request.app['pmsdb'],request['login'])
        accounts = await user_service.get_user_by_account_id(id)
        return self.json_response(accounts)

    async def get_user_by_account(self,request):
        account = request.match_info['account']
        user_service = UserService(request.app['pmsdb'],request['login'])
        accounts = await user_service.get_user_by_account(account)
        return self.json_response(accounts)

    async def get_users_by_garage_id_xor_customer_id(self,request):
        """ get account by account_id """
        garage_id=request.match_info['garage_id']
        user_service = UserService(request.app['pmsdb'],request['login'])
        accounts = await user_service.get_users_by_garage_id_xor_customer_id(garage_id)
        api_response=ApiResponse(accounts)
        return self.json_response(api_response.asdict())

    async def get_first_user_by_account_id(self,request):
        """ get first user by account_id """
        id=request.match_info['id']
        user_service = UserService(request.app['pmsdb'],request['login'])
        one = await user_service.get_first_by_account_id(id)
        if one is None:
            return self.json_response([])
        else:
            return self.json_response([dict(one)])

    async def add_user(self,request):
        db_service = UserService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        new_user = post_data.get('user')
        map_garage_to_account = post_data.get('map_garage_to_account')
        map_garage_group_to_account = post_data.get('map_garage_group_to_account')
        new_user['create_account_id']=request['login']['account_id']
        new_user['password'] = EncryptHelper().encrypt(post_data.get('new_password'))
        one = await db_service.add_user(new_user, map_garage_to_account, map_garage_group_to_account)
        api_response=ApiResponse(one)
        return self.json_response(api_response.asdict())

    
    async def update_user(self,request):
        db_service = UserService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        
        account = post_data.get('user')
        map_garage_to_account = post_data.get('map_garage_to_account')
        map_garage_group_to_account = post_data.get('map_garage_group_to_account')
        new_password = post_data.get('new_password')
        if new_password:
            account['password'] = EncryptHelper().encrypt(new_password)

        account['modified_account_id']=request['login']['account_id']
        account['modified_date'] = datetime.now()

        one = await db_service.update_user(account, map_garage_to_account, map_garage_group_to_account)
        api_response=ApiResponse(one)
        return self.json_response(api_response.asdict())

    async def update_password(self,request):
        db_service = UserService(request.app['pmsdb'],None)
        post_data = await request.json()
        account = post_data.get('user')
        account['password'] = EncryptHelper().encrypt(account['password'])
        one = await db_service.update_password(account)
        api_response=ApiResponse(one)
        return self.json_response(api_response.asdict())

    async def get_permissions(self,request):
        """ get all permission """
        user_service = UserService(request.app['pmsdb'],request['login'])
        d= await user_service.get_permissions()
        api_response=ApiResponse(d)
        return self.json_response(api_response.asdict())
        
    async def get_permission_by_id(self,request):
        """ get permission by id """
        id=request.match_info['id']
        user_service = UserService(request.app['pmsdb'],request['login'])
        permission = await user_service.get_permission_by_id(id)
        if permission is None:
            return self.json_response([])
        else:
            return self.json_response([dict(permission)])

    async def get_permission_by_rold_id(self,request):
        id=request.match_info['id']
        user_service = UserService(request.app['pmsdb'],request['login'])
        permission = await user_service.get_permissions_by_role_id(id)
        api_response = ApiResponse(permission)
        return self.json_response(api_response.asdict())

    async def get_roles(self,request):
        """ get all role """
        user_service = UserService(request.app['pmsdb'],request['login'])
        d= await user_service.get_roles()
        api_response=ApiResponse(d)
        return self.json_response(api_response.asdict())

    async def get_role_by_id(self,request):
        user_service = UserService(request.app['pmsdb'],request['login'])
        id=request.match_info['id']
        one= await user_service.get_role_by_id(id)
        if one is None:
            return self.json_response([])
        else:
            api_response = ApiResponse(one)
            return self.json_response(api_response.asdict())

    async def get_roles_by_customer_id(self,request):
        user_service = UserService(request.app['pmsdb'], request['login'])
        customer_id = request.match_info['customer_id']
        result = await user_service.get_roles_by_customer_id(customer_id)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_maximun_permission(self,request):
        user_service = UserService(request.app['pmsdb'], request['login'])
        result = await user_service.get_maximun_permission()
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_customer_maximun_permission(self,request):
        user_service = UserService(request.app['pmsdb'], request['login'])
        result = await user_service.get_customer_maximun_permission()
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def delete_role(self,request):
        user_service = UserService(request.app['pmsdb'], request['login'])
        role_id = request.match_info['role_id']
        account_id = request['login']['account_id']
        result = await user_service.delete_role(role_id,account_id)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def is_role_name_exist_by_customer_id(self,request):
        role_name=request.match_info['role_name']
        user_service = UserService(request.app['pmsdb'],request['login'])
        result = await user_service.is_role_name_exist_by_customer_id(role_name)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())
    
    async def get_role_by_customer_id(self, request):
        user_service = UserService(request.app['pmsdb'],request['login'])
        customer_id=request.match_info['customer_id']
        d= await user_service.get_role_by_customer_id(customer_id)
        api_response=ApiResponse(d)
        return self.json_response(api_response.asdict())

    async def add_role(self,request):
        db_service = UserService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        role = post_data.get('role')
        role['create_account_id']=request['login']['account_id']
        if 'customer_id' not in role :
            role['customer_id'] = request['login']['customer_id']
        permission = post_data.get('permission')

        one = await db_service.add_role(role,permission)

        if one is None:
            return self.json_response([])
        else:
            api_response=ApiResponse(one)
            return self.json_response(api_response.asdict())

    async def update_role(self,request):
        db_service = UserService(request.app['pmsdb'],request['login'])
        post_data = await request.json()
        
        role = post_data.get('role')
        role['create_account_id']=request['login']['account_id']
        permission = post_data.get('permission')

        one = await db_service.update_role(role,permission)

        if one is None:
            return self.json_response([])
        else:
            api_response=ApiResponse(one)
            return self.json_response(api_response.asdict())
    
    
    async def delete_user_by_id(self,request):
        user_service = UserService(request.app['pmsdb'],request['login'])
        account_id=request.match_info['id']
        login_id=request['login']['account_id']
        result = await user_service.delete_user_by_id(account_id,login_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_map_garage_to_account_by_account_id(self,request):
        user_service = UserService(request.app['pmsdb'],request['login'])
        account_id=request.match_info['account_id']
        result = await user_service.get_map_garage_to_account_by_account_id(account_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_map_garage_group_to_account_by_account_id(self,request):
        user_service = UserService(request.app['pmsdb'],request['login'])
        account_id=request.match_info['account_id']
        result = await user_service.get_map_garage_group_to_account_by_account_id(account_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())
    
    async def get_map_garage_to_account_list_by_acocunt_id(self,request):
        """ 取得可配置的場站清單 """
        user_service = UserService(request.app['pmsdb'],request['login'])
        account_id=request.match_info['account_id']
        result = await user_service.get_map_garage_to_account_list_by_acocunt_id(account_id)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    
