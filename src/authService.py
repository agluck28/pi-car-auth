from py_mqtt.MqttComm import MqttComm, Subscriber
from py_mqtt.request.PyMqttRequest import BaseReply
from replies.AddUser import AddUser
from replies.GetAllUsers import GetAllUsers
from replies.AuthenticateUser import AuthenticateUser
from replies.AuthorizeUser import AuthorizeUser
from replies.UpdateAccess import UpdateAccess
from replies.DeleteUser import DeleteUser
from auth.PiRobotCarAuth import PiRobotCarAuth
from auth.jwt_helper import JwtCreator
import time

def create_mqtt_server(server: str, port: int = 1883,
                       user_name: str = None, password: str = None,
                       client_id: str = None) -> MqttComm:
    return MqttComm(server, port, client_id=client_id,
                    user_name=user_name, password=password)


def create_db_helper(database: str, db_url: str,
                     user_name: str = '', password: str = ''):
    return PiRobotCarAuth(database, db_url, user_name, password)


def create_jwt_helper(secret):
    return JwtCreator(secret)


def create_replies(comm: MqttComm, db: PiRobotCarAuth,
                   jwt: JwtCreator, qos: int = 2,
                   project: str = 'pi_car_robot',
                   service: str = 'auth', ) -> set[BaseReply]:
    replies: set[Subscriber] = {
        AddUser(project, service, qos, db, comm.send_data).subscriber,
        GetAllUsers(project, service, qos, comm.send_data, db).subscriber,
        AuthenticateUser(project, service, qos, comm.send_data, db, jwt).subscriber,
        AuthorizeUser(project, service, qos, comm.send_data, jwt).subscriber,
        UpdateAccess(project, service, qos, comm.send_data, db).subscriber,
        DeleteUser(project, service, qos, comm.send_data, db).subscriber
    }
    return replies


if __name__ == '__main__':
    DATABASE_NAME = 'pi-car-auth'
    DATABASE_URL = '192.168.1.29'
    DATABASE_USER_NAME = 'pi_robot_auth'
    DATABASE_PASSWORD = 'GUAaNkKAxXmXqT6'
    SECRET = 'sdajhsfdkjsdhfr8ASFVs9m9-8VM'
    MQTT_SERVER = 'localhost'

    comm = create_mqtt_server(MQTT_SERVER)
    db = create_db_helper(DATABASE_NAME, DATABASE_URL, DATABASE_USER_NAME, DATABASE_PASSWORD)
    jwt = create_jwt_helper(SECRET)
    replies = create_replies(comm, db, jwt)
    comm.subscriptions = replies
    try:
        comm.start()
        while True:
            time.sleep(0.1)
    except (KeyboardInterrupt, Exception) as e:
        print(e)
        comm.stop()
