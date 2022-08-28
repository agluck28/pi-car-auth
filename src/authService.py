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
from dotenv import dotenv_values


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
        AuthenticateUser(project, service, qos,
                         comm.send_data, db, jwt).subscriber,
        AuthorizeUser(project, service, qos, comm.send_data, jwt).subscriber,
        UpdateAccess(project, service, qos, comm.send_data, db).subscriber,
        DeleteUser(project, service, qos, comm.send_data, db).subscriber,
        AddUser(project, f'{service}_json', qos, db,
                comm.send_data, True).subscriber,
        GetAllUsers(project, f'{service}_json', qos,
                    comm.send_data, db, True).subscriber,
        AuthenticateUser(project, f'{service}_json', qos,
                         comm.send_data, db, jwt, json=True).subscriber,
        AuthorizeUser(project, f'{service}_json', qos,
                      comm.send_data, jwt, True).subscriber,
        UpdateAccess(project, f'{service}_json', qos,
                     comm.send_data, db, True).subscriber,
        DeleteUser(project, f'{service}_json', qos,
                   comm.send_data, db, True).subscriber
    }
    return replies


if __name__ == '__main__':
    config = dotenv_values('.env')

    comm = create_mqtt_server(config['MQTT_SERVER'],
                              user_name=config['MQTT_USER_NAME'],
                              password=config['MQTT_PASSWORD'],
                              client_id=config['MQTT_CLIENT_ID'])
    db = create_db_helper(config['DATABASE_NAME'],
                          config['DATABASE_URL'],
                          config['DATABASE_USER_NAME'],
                          config['DATABASE_PASSWORD'])
    jwt = create_jwt_helper(config['JWT_SECRET'])
    replies = create_replies(comm, db, jwt)
    comm.subscriptions = replies
    try:
        comm.start()
        while True:
            time.sleep(0.1)
    except (KeyboardInterrupt, Exception) as e:
        print(e)
        comm.stop()
