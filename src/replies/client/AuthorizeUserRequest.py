from py_mqtt.request.PyMqttRequest import BaseRequest
from py_mqtt.serializers.AvroHelper import AvroHelper
from queue import Queue
import pathlib
from replies.client.Types import StandardResponse, AuthorizeUserMessage


path = pathlib.Path(__file__).parent.resolve().parent

serialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/auth/pi_car_robot.auth.authorizeUser.avsc')

deSerialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/pi_car_robot_common.standardResponse.avsc')

serializer = AvroHelper(serialSchemaPath)
deserializer = AvroHelper(deSerialSchemaPath)


class AuthorizeUserRequest(BaseRequest):

    def __init__(self, project: str, service: str,
                 qos: int, request_queue: Queue, timeout: int = 2) -> None:
        super().__init__(project, service, 'authorize_user', qos,
                         serializer, deserializer, request_queue, timeout)

    def send_request(self, token: str, access: str, **kwargs) -> StandardResponse:
        self._request = AuthorizeUserMessage(token=token, access=access)
        rsp: StandardResponse = super().send_request(**kwargs)
        return rsp
