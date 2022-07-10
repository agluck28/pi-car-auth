from py_mqtt.request.PyMqttRequest import RequestManager
from py_mqtt.MqttComm import MqttComm
from replies.client.AddUserRequest import AddUserRequest
from replies.client.GetAllUsersRequest import GetAllUsersRequest
from replies.client.AuthenticateUserRequest import AuthenticateUserRequest
from replies.client.AuthorizeUserRequest import AuthorizeUserRequest
from replies.client.UpdateAccessRequest import UpdateAccessRequest
from replies.client.DeleteUserRequest import DeleteUserRequest
from typing import TypedDict


class Replies(TypedDict):
    addUser: AddUserRequest
    getAllUsers: GetAllUsersRequest
    authenticateUser: AuthenticateUserRequest
    authorizeUser: AuthorizeUserRequest
    updateAccess: UpdateAccessRequest
    deleteUser: DeleteUserRequest


def create_mqtt_client(server: str, port: int = 1883,
                       user_name: str = None, password: str = None,
                       client_id: str = None) -> MqttComm:
    return MqttComm(server, port, client_id=client_id,
                    user_name=user_name, password=password)


def create_request_manager(comm: MqttComm) -> RequestManager:

    return RequestManager(comm)


def create_requests(req_manager: RequestManager, project: str = 'pi_car_robot',
                    service: str = 'auth', qos: int = 2) -> Replies:

    return Replies(addUser=AddUserRequest(project, service,
                                          qos, req_manager.queue),
                   getAllUsers=GetAllUsersRequest(project, service,
                                                  qos, req_manager.queue),
                   authenticateUser=AuthenticateUserRequest(project, service,
                                                            qos, req_manager.queue),
                   authorizeUser=AuthorizeUserRequest(project, service,
                                                      qos, req_manager.queue),
                   updateAccess=UpdateAccessRequest(project, service, qos,
                                                    req_manager.queue),
                   deleteUser=DeleteUserRequest(project, service, qos,
                                                req_manager.queue))


if __name__ == '__main__':
    TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NTc0MTQ1ODEuNzU0MzY5MywiZXhwIjoxNjU4MDE5MzgxLjc1NDM2OTMsImFjY2VzcyI6WyJhZG1pbiJdfQ.274r3TBIF0rRjfYwIsJXGrG37jBzD5tDh2riRdOEiUI'
    MQTT_SERVER = 'localhost'
    comm = create_mqtt_client(MQTT_SERVER)
    rm = create_request_manager(comm)
    requests = create_requests(rm)

    comm.start()
    rm.start()
    try:
        while not comm.ready:
            pass
    except:
        pass

    # rsp = requests['authorizeUser'].send_request(token=TOKEN, access='admin')
    # rsp = requests['authenticateUser'].send_request(userName='sherman',
    # password='TheGreatest', access='admin')
    # rsp = requests['updateAccess'].send_request('sherman', 'user')
    rsp = requests['deleteUser'].send_request(userName='sherman')
    print(rsp)
    rm.stop()
    comm.stop()
