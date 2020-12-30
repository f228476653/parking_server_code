"""Controller base.

TODO: check if there is any usage for a base controller.
"""
import json
from aiohttp.web import json_response,Response
from aiohttp import web

from app.util.custom_json_encoder import custom_json_handler,serialize_instance,keystore_json_handler,utc_json_handler

from app.controllers.api_response import ApiResponse

class Controller:
    """Controller base class."""

    @staticmethod
    def blob_response(data, status=200, content_type="application/octet-stream", message="", reason=""):
        return Response(content_type=content_type, status=200, body=data, reason="")
    
    @staticmethod
    def normal_json_response(data, *args, **kwargs):
        """Response json wrapper, to do self.json_response."""
        return json_response(data, *args, **kwargs)

    @staticmethod
    def json_response(data,status=200,message="",reason=""):
        
        if data is None:
            return json_response([])
        else:
            
            result = json.dumps(data,default=custom_json_handler)
            return Response(content_type="application/json",charset="utf-8",status=status,text=result,reason=reason)
    
    @staticmethod
    def error_json_response(message,status=500,reason=""):
            api_response=ApiResponse(f'Error : {message}',True,f'Error : {message}')
            result = json.dumps(api_response.asdict(),default=custom_json_handler)
            return Response(content_type="application/json",charset="utf-8",status=status,text=result,reason=reason)

    @staticmethod
    def utc_json_handler(data,status=200,message="",reason=""):
        if data is None:
            return json_response([])
        else:
            result = json.dumps(data,default=utc_json_handler)
            return Response(content_type="application/json",charset="utf-8",status=status,text=result,reason=reason)
    

    @staticmethod
    def keystoreenum_response(data,status=200,message="",reason=""):
        if data is None:
            return json_response([])
        else:
            result = json.dumps(KeystoreStatusEnum.__members__.values(),default=keystore_json_handler)
            return Response(content_type="application/json",charset="utf-8",status=status,text=result,reason=reason)

    @staticmethod
    async def write(req, response):
        """Send response.
        Usefull if you need to process something after response.
        """
        await response.prepare(req)
        await response.write_eof()
