import socket
from time import sleep
from _thread import start_new_thread

runtime, success = {}, {}

def tryFor(ip, target, i):
    global runtime, success
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 80))
    sock.sendall(b'GET / ' + target.encode("utf-8") + b'\r\nHost: ' + ip.encode("utf-8") + b'\r\n\r\n')
    received = sock.recv(4096)
    sock.close()
    received = received.decode("utf-8", "ignore")
    if target in received:
        success[str(i)] = True
    runtime[str(i)] = False

def list(ip):
    global runtime, success
    
    runtime = {"1":True, "2":True}
    success = {"1":False, "2":False}

    start_new_thread(tryFor, (ip, "HTTP/1.1", 1))
    start_new_thread(tryFor, (ip, "HTTP/1.0", 2))

    while runtime["1"] or runtime["2"]:
        sleep(0.2)
    protocols = []
    if success["1"]:
        protocols.append("http/1.1")
    if success["2"]:
        protocols.append("http/1.0")
    return protocols

