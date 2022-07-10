from py_mqtt.request.PyMqttRequest import BaseReply
from py_mqtt.serializers.AvroHelper import AvroHelper
from py_mqtt.MqttComm import Message
from typing import Callable
from replies.client.Types import DeleteUserMessage, StandardResponse
import pathlib
from auth.PiRobotCarAuth import PiRobotCarAuth

path = pathlib.Path(__file__).parent.resolve()
serialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/pi_car_robot_common.standardResponse.avsc')
deSerialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/auth/pi_car_robot.auth.deleteUser.avsc')

serializer = AvroHelper(serialSchemaPath)
deserializer = AvroHelper(deSerialSchemaPath)


class DeleteUser(BaseReply):

    def __init__(self, project: str, service: str,
                 qos: int, publisher: Callable[[Message], None],
                 db_helper: PiRobotCarAuth) -> None:
        super().__init__(project, service, 'delete_user',
                         qos, deserializer, serializer, publisher)
        self.db = db_helper

    def handle_message(self, data: DeleteUserMessage) -> StandardResponse:
        try:
            self.db.delete_user(data['userName'])
            return StandardResponse(success=True)
        except RuntimeWarning as e:
            return StandardResponse(success=False, msg=f'{type(e).__name__}: {e}')
