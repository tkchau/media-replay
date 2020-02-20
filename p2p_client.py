import logging
import socket
import time
import thread
import json


def addr_to_msg(addr):
    return '{}:{}'.format(addr[0], str(addr[1])).encode('utf-8')


TARGET_USER = "a"
# TARGET_HOST = "35.247.162.147"
TARGET_HOST = "192.168.1.109"
TARGET_PORT = 10010

udp_sock = None

# dirty code for fast updating
REMOTE_HOST = None
REMOTE_PORT = None


def main_query_server(host=TARGET_HOST, port=TARGET_PORT):
    while True:
        dict_cmd = {}
        dict_cmd['command'] = 'update'
        dict_cmd['data'] = 'relaya'
        json_string = json.dumps(dict_cmd)
        # logging.info(json_string)

        # logging.info("====================> Thread main_query_server....")
        udp_sock.sendto(json_string, (host, port))
        time.sleep(5)


def main_send(host=TARGET_HOST, port=TARGET_PORT):
    msg_counter = 0
    while True:
        msg_counter = msg_counter + 1
        host_str = "host1-" + str(msg_counter)
        # logging.info("Thread main sending....")
        udp_sock.sendto(host_str, (host, port))
        time.sleep(0.1)


def main_recv(host=TARGET_HOST, port=TARGET_PORT):
    logging.info("Target host is " + host + ":" + str(port))
    while True:
        try:
            # logging.info("Thread main receiving....")
            data, addr = udp_sock.recvfrom(1024)    # buffer size is 1024 bytes
            logging.info("connection from: %s:%d --> %s", addr[0], int(addr[1]), data)
            # logging.info("data is > " + data)
            # more update
            remote_ip = addr[0]
            remote_port = int(addr[1])
            if (remote_ip == TARGET_HOST) and (remote_port == TARGET_PORT):
                logging.info("===============> Found response from server.")
                logging.info(data)

                # update port
                hostp = None
                portp = None
                loaded_json = json.loads(str(data))
                for x in loaded_json:
                    if x == "ip":
                        hostp = loaded_json[x]
                    elif x == "port":
                        portp = int(loaded_json[x])

                # Starting threads
                global REMOTE_HOST
                global REMOTE_PORT
                REMOTE_HOST = hostp
                REMOTE_PORT = portp
                logging.info("=============> Updating " + REMOTE_HOST + ":" + str(REMOTE_PORT))

            # sleeping time
            time.sleep(0.1)
        except Exception as expt:
            logging.error(str(expt))
            time.sleep(0.1)


def main(host=TARGET_HOST, port=TARGET_PORT):
    logging.info("I'm client")
    logging.info("Host is " + host + ":" + str(port))

    # Step 1: Create udp socket
    global udp_sock
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

    # Step 2: Send message to server
    dict_cmd = {}
    dict_cmd['command'] = 'register'
    dict_cmd['data'] = TARGET_USER
    json_string = json.dumps(dict_cmd)
    logging.info(json_string)

    udp_sock.sendto(json_string, (host, port))
    data, addr = udp_sock.recvfrom(1024)
    logging.info("client received: %s --> %s", addr, data)
    # clear dict
    dict_cmd.clear()

    # Step 3: query other client information
    data2 = None
    dict_cmd['command'] = 'query'
    dict_cmd['data'] = TARGET_USER
    json_string = json.dumps(dict_cmd)
    logging.info(json_string)
    while True:
        udp_sock.sendto(json_string, (host, port))

        try:
            data2, addr = udp_sock.recvfrom(1024)
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
    logging.info("Client received: %s", data2)
    loaded_json = json.loads(str(data2))
    hostp = None
    portp = None
    for x in loaded_json:
        if x == "ip":
            hostp = loaded_json[x]
        elif x == "port":
            portp = int(loaded_json[x])

    # Starting threads
    global REMOTE_HOST
    global REMOTE_PORT
    REMOTE_HOST = hostp
    REMOTE_PORT = portp

    try:
        thread.start_new_thread(main_send, (hostp, portp,))
        thread.start_new_thread(main_recv, (hostp, portp,))
        thread.start_new_thread(main_query_server, (TARGET_HOST, TARGET_PORT,))
    except Exception as expt3:
        logging.error(str(expt3))

    # Finally, run forever
    while True:
        time.sleep(0.1)


if __name__ == '__main__':
    # '%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - - %(name)s:%(lineno)d- %(message)s')
    main()
    logging.info("============= quit game!!!")