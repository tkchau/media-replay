import logging
import socket
import time
import thread
import json


def addr_to_msg(addr):
    return '{}:{}'.format(addr[0], str(addr[1])).encode('utf-8')


TARGET_USER1 = "relaya"
TARGET_USER2 = "relayb"
# TARGET_HOST = "35.247.162.147"
TARGET_HOST = "192.168.1.109"
TARGET_PORT = 10010

# udp socket
udp_sock1 = None


# convert dict data structure to json string
def conver_dict_to_json(dict_cmd):
    json_string = json.dumps(dict_cmd)
    return json_string


def main_query_server(channel=None, host=TARGET_HOST, port=TARGET_PORT):
    if channel is None:
        logging.error("Channel socket is None, come back...")
        return

    # update socket channel
    udp_sock = channel

    while True:
        host_str = "query"
        logging.info("====================Thread main_query_server....")
        udp_sock.sendto(host_str, (host, port))
        data, addr = udp_sock.recvfrom(1024)  # buffer size is 1024 bytes
        logging.info("====================connection from: %s --> %s", addr, data)
        time.sleep(1)


def main_send(channel=None, host=TARGET_HOST, port=TARGET_PORT):
    if channel is None:
        logging.error("Channel socket is None, come back...")
        return

    # update socket channel
    udp_sock = channel

    msg_counter = 0
    while True:
        msg_counter = msg_counter + 1
        host_str = "host-relay-" + str(msg_counter)
        # logging.info("Thread main sending....")
        udp_sock.sendto(host_str, (host, port))
        time.sleep(0.1)


def main_recv(channel=None, host=TARGET_HOST, port=TARGET_PORT):
    if channel is None:
        logging.error("Channel socket is None, come back...")
        return

    # update socket channel
    udp_sock = channel

    logging.info("Target host is " + host + ":" + str(port))
    while True:
        try:
            # logging.info("Thread main receiving....")
            data, addr = udp_sock.recvfrom(1024)  # buffer size is 1024 bytes
            logging.info("Relay connection from: %s --> %s", addr, data)
            # logging.info("data is > " + data)
            time.sleep(0.1)
        except Exception as expt:
            logging.error(str(expt))
            time.sleep(0.1)


def main_1(host=TARGET_HOST, port=TARGET_PORT):
    logging.info("I'm media-relay1")
    logging.info("Host is " + host + ":" + str(port))

    # Step 1: Create udp socket
    global udp_sock1
    udp_sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    # udp_sock.bind(("192.168.1.109", 6666))

    # Step 2: Send message to server
    dict_cmd = {}
    dict_cmd['command'] = 'register'
    dict_cmd['data'] = TARGET_USER
    json_string = conver_dict_to_json(dict_cmd)
    logging.info(json_string)
    udp_sock1.sendto(json_string, (host, port))
    data, addr = udp_sock1.recvfrom(1024)
    logging.info("relay received: %s --> %s", addr, data)

    # clear dict
    dict_cmd.clear()

    data2 = None
    dict_cmd['command'] = 'query2'
    dict_cmd['data'] = 'a'
    json_string = json.dumps(dict_cmd)
    logging.info(json_string)
    while True:
        udp_sock1.sendto(json_string, (host, port))

        try:
            data2, addr = udp_sock1.recvfrom(1024)
            logging.info(data2)
            loaded_json = json.loads(str(data2))
            status = None
            for x in loaded_json:
                if x == "status":
                    status = loaded_json[x]
                    break

            # stopping point
            logging.info("Dump status is " + status)
            if (status != 'unknown') and ("host" not in data2):
                break
            else:
                time.sleep(0.2)
        except Exception as expt2:
            logging.error(str(expt2))

    # Step 4: We have valid address for p2p
    logging.info("Relay received: %s", data2)
    loaded_json = json.loads(str(data2))
    hostp = None
    portp = None
    for x in loaded_json:
        if x == "ip":
            hostp = loaded_json[x]
        elif x == "port":
            portp = int(loaded_json[x])
    logging.info("Found rtp session to send/recv " + hostp + ":" + str(portp))

    try:
        thread.start_new_thread(main_send, (udp_sock1, hostp, portp,))
        thread.start_new_thread(main_recv, (udp_sock1, hostp, portp,))
    except Exception as expt3:
        logging.error(str(expt3))

    # Finally, run forever
    while True:
        time.sleep(0.1)



def main_2(host=TARGET_HOST, port=TARGET_PORT):
    logging.info("I'm media-relay2")
    logging.info("Host is " + host + ":" + str(port))

    # Step 1: Create udp socket
    global udp_sock1
    udp_sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    # udp_sock.bind(("192.168.1.109", 6666))

    # Step 2: Send message to server
    dict_cmd = {}
    dict_cmd['command'] = 'register'
    dict_cmd['data'] = TARGET_USER
    json_string = conver_dict_to_json(dict_cmd)
    logging.info(json_string)
    udp_sock1.sendto(json_string, (host, port))
    data, addr = udp_sock1.recvfrom(1024)
    logging.info("relay received: %s --> %s", addr, data)

    # clear dict
    dict_cmd.clear()

    data2 = None
    dict_cmd['command'] = 'query2'
    dict_cmd['data'] = 'a'
    json_string = json.dumps(dict_cmd)
    logging.info(json_string)
    while True:
        udp_sock1.sendto(json_string, (host, port))

        try:
            data2, addr = udp_sock1.recvfrom(1024)
            logging.info(data2)
            loaded_json = json.loads(str(data2))
            status = None
            for x in loaded_json:
                if x == "status":
                    status = loaded_json[x]
                    break

            # stopping point
            logging.info("Dump status is " + status)
            if (status != 'unknown') and ("host" not in data2):
                break
            else:
                time.sleep(0.2)
        except Exception as expt2:
            logging.error(str(expt2))

    # Step 4: We have valid address for p2p
    logging.info("Relay received: %s", data2)
    loaded_json = json.loads(str(data2))
    hostp = None
    portp = None
    for x in loaded_json:
        if x == "ip":
            hostp = loaded_json[x]
        elif x == "port":
            portp = int(loaded_json[x])
    logging.info("Found rtp session to send/recv " + hostp + ":" + str(portp))

    try:
        thread.start_new_thread(main_send, (udp_sock1, hostp, portp,))
        thread.start_new_thread(main_recv, (udp_sock1, hostp, portp,))
    except Exception as expt3:
        logging.error(str(expt3))

    # Finally, run forever
    while True:
        time.sleep(0.1)


def main():
    main_1()


if __name__ == '__main__':
    # '%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - - %(name)s:%(lineno)d- %(message)s')
    main()
    logging.info("============= quit game!!!")
