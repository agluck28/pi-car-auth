from py_mqtt.request.PyMqttRequest import BaseReply
from py_mqtt.serializers.AvroHelper import AvroHelper
from py_mqtt.MqttComm import Message
from typing import Callable
from auth.PiRobotCarAuth import PiRobotCarAuth
from replies.client.Types import UpdateAccessMessage, StandardResponse
import pathlib

path = pathlib.Path(__file__).parent.resolve()
serialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/pi_car_robot_common.standardResponse.avsc')
deSerialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/auth/pi_car_robot.auth.updateAccess.avsc')


class UpdateAccess(BaseReply):

    def __init__(self, project: str, service: str,
                 qos: int, publisher: Callable[[Message], None],
                 db_helper: PiRobotCarAuth, json: bool = False) -> None:
        super().__init__(project, service, 'update_access',
                         qos, AvroHelper(deSerialSchemaPath, json),
                         AvroHelper(serialSchemaPath, json), publisher)
        self.db = db_helper

    def handle_message(self, data: UpdateAccessMessage) -> StandardResponse:
        try:
            self.db.update_access(data['userName'], [data['access']])
            return StandardResponse(success=True)
        except RuntimeWarning as e:
            return StandardResponse(success=False,
                                    msg=f'{type(e).__name__}: {e}')
