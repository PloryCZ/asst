import ssl
import socket


def get_info(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, 80))
    sock.sendall(b'GET / HTTP/1.0\r\nHost: ' + addr.encode("utf-8") + b'\r\n\r\n')
    received = sock.recv(4096).decode("utf-8", "ignore")
    info = {}
    received = received.lower()
    if "server: " in received:
        info["server"] = received.split("server: ")[1].split("\r\n")[0]
    if "date: " in received:
        info["date"] = received.split("date: ")[1].split("\r\n")[0]

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssock = context.wrap_socket(sock)
        ssock.connect((addr, 443))
        info["tls/ssl"] = "HTTPS (TLS v1.2)"
    except:
        info["tls/ssl"] = "no"
    return info

