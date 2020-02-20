import logging
import socket
import time
import json


def addr_to_msg(addr):
    return '{}:{}'.format(addr[0], str(addr[1])).encode('utf-8')


class RtpSession:
    def __init__(self, name, ip, port):
        self._name = name
        self._ip = ip
        self._port = port

    @property
    def name(self):
        return self._name

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @name.setter
    def name(self, value):
        self._name = value

    @ip.setter
    def ip(self, value):
        self._ip = value

    @port.setter
    def port(self, value):
        self._port = value

    def __str__(self):
        return self.name + ":" + self.ip + ":" + str(self.port)


LISTENING_PORT = 10010

list_ip_from_clients = []


def main(host='0.0.0.0', port=LISTENING_PORT):
    logging.info("I'm server")
    logging.info("Host is " + host + ":" + str(port))
    # Step 1: create udp socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    udp_sock.bind((host, port))
    logging.info("Server is listening at " + host + ":" + str(port))

    # Step 2: receive message from clients
    while True:
        try:
            data, addr = udp_sock.recvfrom(1024)  # buffer size is 1024 bytes
            logging.info("connection from: %s --> %s", addr, data)

            string_cmd = None
            user_name = None
            loaded_json = json.loads(str(data))
            for x in loaded_json:
                if x == "command":
                    string_cmd = loaded_json[x]
                elif x == "data":
                    user_name = loaded_json[x]

            if string_cmd == 'register':
                logging.info("server - send client info to: %s", addr)

                udp_sock.sendto(addr_to_msg(addr), addr)

                new_peer = RtpSession(user_name, addr[0], int(addr[1]))
                logging.info(str(new_peer))

                list_ip_from_clients.append(new_peer)

                # dump content of list
                logging.info("Length of list is " + str(len(list_ip_from_clients)))

            elif string_cmd == 'query':
                logging.info("server - send client info to: %s", addr)
                is_found = False
                found_element = None
                for element in list_ip_from_clients:
                    if element.name != user_name:
                        is_found = True
                        found_element = element
                        break

                dict_cmd = {}
                if is_found is False:
                    udp_sock.sendto('unknown', addr)
                    dict_cmd['status'] = 'unknown'
                else:
                    dict_cmd['command'] = 'query'
                    dict_cmd['status'] = 'found'
                    dict_cmd['ip'] = found_element.ip
                    dict_cmd['port'] = found_element.port

                # dump content
                json_string = json.dumps(dict_cmd)
                logging.info(json_string)
                udp_sock.sendto(json_string, addr)

            elif string_cmd == 'query2':
                logging.info("data2 is " + user_name)
                logging.info("server2 - send client info to: %s", addr)
                is_found = False
                found_element = None
                for element in list_ip_from_clients:
                    if element.name == user_name:
                        is_found = True
                        found_element = element
                        break

                dict_cmd = {}
                if is_found is False:
                    udp_sock.sendto('unknown', addr)
                    dict_cmd['status'] = 'unknown'
                else:
                    dict_cmd['command'] = 'query'
                    dict_cmd['status'] = 'found'
                    dict_cmd['ip'] = found_element.ip
                    dict_cmd['port'] = found_element.port

                # dump content
                json_string = json.dumps(dict_cmd)
                logging.info(json_string)
                udp_sock.sendto(json_string, addr)

            elif string_cmd == 'update':
                logging.info("data3 is " + user_name)
                logging.info("server2 - send client info to: %s", addr)
                is_found = False
                found_element = None
                for element in list_ip_from_clients:
                    if element.name == user_name:
                        is_found = True
                        found_element = element
                        break

                dict_cmd = {}
                if is_found is False:
                    udp_sock.sendto('unknown', addr)
                    dict_cmd['status'] = 'unknown'
                else:
                    dict_cmd['command'] = 'query'
                    dict_cmd['status'] = 'found'
                    dict_cmd['ip'] = found_element.ip
                    dict_cmd['port'] = found_element.port

                # dump content
                json_string = json.dumps(dict_cmd)
                logging.info(json_string)
                udp_sock.sendto(json_string, addr)

            time.sleep(0.1)
        except Exception as expt2:
            logging.error(str(expt2))
            time.sleep(0.1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - - %(name)s:%(lineno)d- %(message)s')
    main()
    logging.info("============= quit game!!!")