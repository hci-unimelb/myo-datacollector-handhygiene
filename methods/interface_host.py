import methods.interface_sub as interface
import methods.project_library as project_library
import socket
from threading import Thread
from multiprocessing import Pipe
import json
import datetime
import time
import sched


def connection_mac(pipe):
    s = socket.socket()

    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    port = 10001

    print('Host IP:', ip, 'Port:', port)
    s.bind((host, port))
    s.listen(1)

    c, addr = s.accept()
    print('Connection Address:', addr)

    while True:
        response = c.recv(1024).decode()
        if response is None or response == '':
            break
        print(response)
        response = json.loads(response)

        if response['status'] == 'start':
            time_offset = project_library.get_time_offset()[1]

            now = datetime.datetime.timestamp(datetime.datetime.now())
            sleep = response['time'] - (now + time_offset)
            time.sleep(sleep)

            pipe.send(response['message'])

        elif response['status'] == 'end':
            pipe.send({'status': 'end'})


def main():
    pipe1, pipe2 = Pipe()

    thread = Thread(target=connection_mac, args=(pipe2,))
    thread.start()

    interface.plot_emg(pipe1, True)


if __name__ == '__main__':
    main()
