from py_mqtt.request.PyMqttRequest import BaseRequest
from py_mqtt.serializers.AvroHelper import AvroHelper
from queue import Queue
import pathlib
from replies.client.Types import UpdateAccessMessage, StandardResponse

path = pathlib.Path(__file__).parent.resolve().parent

serialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/auth/pi_car_robot.auth.updateAccess.avsc')

deSerialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/pi_car_robot_common.standardResponse.avsc')

serializer = AvroHelper(serialSchemaPath)
deserializer = AvroHelper(deSerialSchemaPath)


class UpdateAccessRequest(BaseRequest):

    def __init__(self, project: str, service: str,
                 qos: int, request_queue: Queue, timeout: int = 2) -> None:
        super().__init__(project, service, 'update_access', qos,
                         serializer, deserializer, request_queue, timeout)

    def send_request(self,username: str, access: str, **kwargs) -> StandardResponse:
        self._request = UpdateAccessMessage(userName=username, access=access)
        return super().send_request(**kwargs)
