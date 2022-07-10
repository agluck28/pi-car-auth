from py_mqtt.request.PyMqttRequest import BaseReply
from py_mqtt.serializers.AvroHelper import AvroHelper
from py_mqtt.MqttComm import Message
from typing import Callable
from replies.client.Types import AuthorizeUserMessage, StandardResponse
import pathlib
from auth.jwt_helper import JwtCreator

path = pathlib.Path(__file__).parent.resolve()
serialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/pi_car_robot_common.standardResponse.avsc')
deSerialSchemaPath = pathlib.Path.joinpath(
    path, './schemas/src/auth/pi_car_robot.auth.authorizeUser.avsc')

serializer = AvroHelper(serialSchemaPath)
deserializer = AvroHelper(deSerialSchemaPath)


class AuthorizeUser(BaseReply):

    def __init__(self, project: str, service: str, qos: int,
                 publisher: Callable[[Message], None], jwt: JwtCreator) -> None:
        super().__init__(project, service, 'authorize_user',
                         qos, deserializer, serializer, publisher)
        self.jwt = jwt

    def handle_message(self, data: AuthorizeUserMessage) -> StandardResponse:
        check = self.jwt.decode_token(data['token'])
        if check[0]:
            #token was valid, check access level
            if data['access'] in check[1]['access']:
                return StandardResponse(success=True)
            else:
                return StandardResponse(success=False, msg='Invalid access level')
        else:
            return StandardResponse(success=False, msg='Invalid Token')