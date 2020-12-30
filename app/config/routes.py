
""" utes module."""
from app.controllers.user_controller import UserController
from app.controllers.login_controller import LoginController
from app.controllers.systemlog_controller import SystemlogController
from app.controllers.system_configuration_controller import SystemConfigurationController
import aiohttp_cors

prefix_v1 = "/api/v1"

def map_routes(app):
    """Map routes to app object."""
    cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })

    
    # kafka_controller = KafkaController()
    # cors.add(app.router.add_route("POST", prefix_v1+r'/kafka/producer', kafka_controller.kafka_producer))
    # cors.add(app.router.add_route("POST", prefix_v1+r'/kafka/consumer', kafka_controller.kafka_consumer))

    system_configuration_controller = SystemConfigurationController()
    cors.add(app.router.add_route("GET", prefix_v1+r'/system/configuration/{key}', system_configuration_controller.get_system_configuration_by_key))
    cors.add(app.router.add_route("GET", prefix_v1+r'/system/configuration', system_configuration_controller.get_all_system_configuration))
    cors.add(app.router.add_route("POST", prefix_v1+r'/system/configuration', system_configuration_controller.create_system_configuration))
    cors.add(app.router.add_route("PUT", prefix_v1+r'/system/configuration/update', system_configuration_controller.update_system_configuration_by_key))
    cors.add(app.router.add_route("PUT", prefix_v1+r'/system/configuration/delete', system_configuration_controller.delete_system_configuration_by_key))

    
    login_controller=LoginController()
    cors.add(app.router.add_route("POST", prefix_v1+r'/login', login_controller.login))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/login/au/forget_password',login_controller.forget_passward_query_reset))
    cors.add(app.router.add_route("GET", prefix_v1+r'/login/au/get_reset_password_account/{token}', login_controller.get_reset_password_account))

    
    user_controller = UserController()
    cors.add(app.router.add_route("PUT", prefix_v1+r'/account/au/update_password',user_controller.update_password))
    cors.add(app.router.add_route("GET",prefix_v1+r'/accounts',user_controller.get_users))
    
   
    syslog_controller=SystemlogController()
    cors.add(app.router.add_route("POST",prefix_v1+r'/system_log',syslog_controller.add_log))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/system_log',syslog_controller.delall_log))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/system_log',syslog_controller.query_by_message))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/system_log/date',syslog_controller.query_by_date))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/system_log/event/',syslog_controller.query_by_event))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/system_log/type',syslog_controller.query_SystemEventType))


