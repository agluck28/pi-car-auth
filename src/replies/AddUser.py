from py_mqtt.request.PyMqttRequest import BaseReply
from py_mqtt.serializers.AvroHelper import AvroHelper
from py_mqtt.MqttComm import Message
from typing import Callable
from auth.PiRobotCarAuth import PiRobotCarAuth
from replies.client.Types import AddUserMessage, StandardResponse
import pathlib

path = pathlib.Path(__file__).parent.resolve()
serialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/pi_car_robot_common.standardResponse.avsc')
deSerialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/auth/pi_car_robot.auth.userRequest.avsc')


class AddUser(BaseReply):
    '''
    Adds the given user
    '''

    def __init__(self, project: str, service: str,
                 qos: int, db_helper: PiRobotCarAuth,
                 publisher: Callable[[Message], None],
                 json: bool = False) -> None:
        super().__init__(project, service, 'add_user',
                         qos, AvroHelper(deSerialSchemaPath, json),
                         AvroHelper(serialSchemaPath, json), publisher)
        self.db = db_helper

    def handle_message(self, data: AddUserMessage) -> StandardResponse:
        try:
            self.db.add_user(data['userName'],
                             data['password'], [data['access']])
            return StandardResponse(success=True)
        except (RuntimeWarning, KeyError) as e:
            return StandardResponse(success=False,
                                    msg=f'Error: {type(e).__name__}: {e}')
