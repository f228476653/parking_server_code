import json
from app.controllers.controller import Controller
from app.decorators.authorize import authorize
from app.controllers.api_response import ApiResponse
from app.services.system_configuration import SystemConfigurationService

class SystemConfigurationController(Controller):

    async def create_system_configuration(self, request):
        system_configuration = SystemConfigurationService(request.app['pmsdb'], request['login'])
        post_data = await request.json()
        result = await system_configuration.create_system_configuration(post_data)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_all_system_configuration(self, request):
        system_configuration = SystemConfigurationService(request.app['pmsdb'], request['login'])
        result = await system_configuration.get_all_system_configuration()
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())

    async def get_system_configuration_by_key(self, request):
        system_configuration = SystemConfigurationService(request.app['pmsdb'], request['login'])
        key = request.match_info['key']
        result = await system_configuration.get_system_configuration_by_key(key)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())
    
    async def update_system_configuration_by_key(self, request):
        system_configuration = SystemConfigurationService(request.app['pmsdb'], request['login'])
        post_data = await request.json()
        result = await system_configuration.update_system_configuration_by_key(post_data)
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())
      
    async def delete_system_configuration_by_key(self, request):
        system_configuration = SystemConfigurationService(request.app['pmsdb'], request['login'])
        post_data = await request.json()
        result = await system_configuration.delete_system_configuration_by_key(post_data['key'])
        api_response = ApiResponse(result)
        return self.json_response(api_response.asdict())
