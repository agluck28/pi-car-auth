from py_mqtt.request.PyMqttRequest import BaseRequest
from py_mqtt.serializers.AvroHelper import AvroHelper
from queue import Queue
import pathlib
from replies.client.Types import StandardResponse, AddUserMessage


path = pathlib.Path(__file__).parent.resolve().parent

serialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/auth/pi_car_robot.auth.userRequest.avsc')

deSerialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/pi_car_robot_common.standardResponse.avsc')

serializer = AvroHelper(serialSchemaPath)
deserializer = AvroHelper(deSerialSchemaPath)


class AuthenticateUserRequest(BaseRequest):

    def __init__(self, project: str, service: str,
                 qos: int, request_queue: Queue, timeout: int = 2) -> None:
        super().__init__(project, service, 'authenticate_user',
                         qos, serializer, deserializer, request_queue, timeout)

    def send_request(self, userName: str, password: str,
                     access: str, **kwargs) -> StandardResponse:
        self._request = AddUserMessage(userName=userName,
                                       password=password, access=access)
        rsp: StandardResponse = super().send_request(**kwargs)
        return rsp
