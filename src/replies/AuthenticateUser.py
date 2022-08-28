from py_mqtt.request.PyMqttRequest import BaseReply
from py_mqtt.serializers.AvroHelper import AvroHelper
from py_mqtt.MqttComm import Message
from typing import Callable
from auth.PiRobotCarAuth import PiRobotCarAuth
from replies.client.Types import AddUserMessage, StandardResponse
import pathlib
from auth.jwt_helper import JwtCreator

path = pathlib.Path(__file__).parent.resolve()
serialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/pi_car_robot_common.standardResponse.avsc')
deSerialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/auth/pi_car_robot.auth.userRequest.avsc')


class AuthenticateUser(BaseReply):

    def __init__(self, project: str, service: str,
                 qos: int, publisher: Callable[[Message], None],
                 db_helper: PiRobotCarAuth, jwt: JwtCreator,
                 life_span: int = 604800, json: bool = False) -> None:
        super().__init__(project, service, 'authenticate_user',
                         qos, AvroHelper(deSerialSchemaPath, json),
                         AvroHelper(serialSchemaPath, json), publisher)
        self.db = db_helper
        self.jwt = jwt
        self.life_span = life_span

    def handle_message(self, data: AddUserMessage) -> StandardResponse:
        try:
            rsp = self.db.authenticate_user(data['userName'], data['password'],
                                            data['access'])
            if rsp['code'] == 200:
                # get the token
                token = self.jwt.create_token(self.life_span,
                                              access=[data['access']])
                return StandardResponse(success=True, msg=token)
        except RuntimeWarning as e:
            return StandardResponse(success=False,
                                    msg=f'{type(e).__name__}: {e}')
