import pathlib
from py_mqtt.request.PyMqttRequest import BaseReply
from py_mqtt.serializers.AvroHelper import AvroHelper
from py_mqtt.MqttComm import Message
from typing import Callable
from auth.PiRobotCarAuth import PiRobotCarAuth
from replies.client.Types import GetAllUsersMessage, StandardRequest


path = pathlib.Path(__file__).parent.resolve()
serialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/auth/pi_car_robot.auth.getAllUsers.avsc')
deSerialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/pi_car_robot_common.standardRequest.avsc')


class GetAllUsers(BaseReply):

    def __init__(self, project: str, service: str,
                 qos: int, publisher: Callable[[Message], None],
                 db_helper: PiRobotCarAuth, json: bool = False) -> None:
        super().__init__(project, service, 'get_all_users', qos,
                         AvroHelper(deSerialSchemaPath, json),
                         AvroHelper(serialSchemaPath, json), publisher)
        self.db = db_helper

    def handle_message(self, data: StandardRequest) -> dict:
        try:
            rsp = self.db.get_all_users()
            users = [user[0] for user in rsp if True]
            return GetAllUsersMessage(users=users)
        except RuntimeWarning:
            return GetAllUsersMessage(users=['Bad Request'])
