from py_mqtt.request.PyMqttRequest import BaseRequest
from py_mqtt.serializers.AvroHelper import AvroHelper
from queue import Queue
import pathlib
from replies.client.Types import StandardRequest, GetAllUsersMessage

path = pathlib.Path(__file__).parent.resolve().parent

serialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/pi_car_robot_common.standardRequest.avsc')

deSerialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/auth/pi_car_robot.auth.getAllUsers.avsc')

serializer = AvroHelper(serialSchemaPath)
deserializer = AvroHelper(deSerialSchemaPath)


class GetAllUsersRequest(BaseRequest):

    def __init__(self, project: str, service: str,
                 qos: int, request_queue: Queue,
                 timeout: int = 2) -> None:
        super().__init__(project, service, 'get_all_users', qos,
                         serializer, deserializer, request_queue, timeout)

    def send_request(self, **kwargs) -> GetAllUsersMessage:
        self._request = StandardRequest(request=True)
        rsp: GetAllUsersMessage = super().send_request(**kwargs)
        return rsp
