import ssl
import socket
from time import sleep
from _thread import start_new_thread

runtime, success = {}, {}

def checkFor(ip, target, i):
    global runtime, success
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.set_alpn_protocols([target])
        ssock = context.wrap_socket(sock)
        ssock.connect((ip, 443))
        protocol = ssock.selected_alpn_protocol()
        ssock.close()
        del ssock, context, sock
        if protocol is not None:
            if protocol == target:
                success[str(i)] = True
        runtime[str(i)] = False
        return
    except:
        runtime[str(i)] = False


def list(ip):
    global runtime, success
    runtime = {"1":True, "2":True, "3":True}
    success = {"1":False, "2":False, "3":False}
    start_new_thread(checkFor, (ip, "http/1.1", 1))
    start_new_thread(checkFor, (ip, "h2", 2))
    start_new_thread(checkFor, (ip, "http/1", 3))
    while runtime["1"] or runtime["2"] or runtime["3"]:
        sleep(0.2)
    supported = []
    if success["1"]:
        supported.append("http/1.1")
    if success["2"]:
        supported.append("http/2")
    return supported

