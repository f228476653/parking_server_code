
from aiohttp import web
from app.config.models import Account
from app.services.user_service import UserService 
from app.services.exceptions import UserNotExistError,AuthenticationError
from app.controllers.controller import Controller

from .api_response import ApiResponse

class LoginController(Controller):
    
    async def login(self,request):
        #region
        """
        Description login
        ---
        tags:
        - Login
        summary: Login
        description: user login.
        operationId: app.controllers.login_controller.login
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: login and get token
          required: true
          schema:
            type: object
            properties:
              account:
                type: string
                description: account
                example: account
              passwd:
                type: string
                description: password
                example: password
              rem:
                type: boolean
                default: fasle
                description: remember me
            required:
                - account
                - passwd
        responses:
          "200":
            description: 伺服器收到請求並回應
            schema:
              type: object
              properties:
                data:
                  type: object
                  description: 有error發生，data為{}
                  properties:
                    token:
                      type: string
                      description: 呼叫API需要的oken
                      example: "eyJ0eXA....."
                error:
                  type: object
                  description: 沒有發生錯誤，error為null
                  properties:
                    code:
                      type: string
                      description: 錯誤代碼<br>\
                        00999:未知錯誤
                      example: "00999"
                    title:
                      type: string
                      description: 錯誤訊息
                      example: "意外錯誤"
                    detail:
                      type: string
                      description: 詳細的錯誤訊息<br>\
                        User does not exist:帳號錯誤<br>\
                        Wrong credentials:密碼錯誤
                      example: "User does not exist"

        """
        #endregion
        post_data = await request.json()
        account = post_data.get('account')
        password = post_data.get('passwd')
        rem = post_data.get('rem')
        if rem :
            jwt_exp_delta_seconds = request.app['jwt_exp_delta_seconds_remember_me']
        else:
            jwt_exp_delta_seconds = request.app['jwt_exp_delta_seconds']
        jwt_secret = request.app['jwt_secret']
        jwt_algorithm = request.app['jwt_algorithm']

        try:
            user_service = UserService(request.app['pmsdb'],None)
            result = await user_service.login(account,password,jwt_exp_delta_seconds,jwt_secret,jwt_algorithm)
            data={'is_customer_root':result['is_customer_root'], 'role_id':result['role_id'],'customer_id':result['customer_id'],'is_superuser':result['is_superuser'],'token':result['token'].decode('utf-8'),'user_name':result['user_name'],'account':result['account'],'account_id':result['account_id']}
            api_response=ApiResponse(data)
            return self.json_response(api_response.asdict())
        except UserNotExistError:
            api_response=ApiResponse({},True,"User does not exist")
            return self.json_response(api_response.asdict())
        except AuthenticationError:
            api_response=ApiResponse({},True,"Wrong credentials")
            return self.json_response(api_response.asdict())

    async def forget_passward_query_reset(self,request):
        """ forget password """
        print('save')
        user_service = UserService(request.app['pmsdb'],None)
        post_data = await request.json()
        email = post_data.get('email')
        jwt_secret = request.app['jwt_secret']
        jwt_algorithm = request.app['jwt_algorithm']
        jwt_exp_delta_seconds = 36000000
        result = await user_service.forget_passward_query_reset(email,jwt_secret,jwt_algorithm,jwt_exp_delta_seconds)
        api_response=ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_reset_password_account(self,request):
        token=request.match_info['token']
        service = UserService(request.app['pmsdb'],None)
        data = await service.get_reset_password_account(token)
        result = ApiResponse(data)
        return self.json_response(result.asdict())
