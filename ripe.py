import socket


def query_ripe(query):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("whois.ripe.net", 43))
    pre = sock.recv(4096)
    sock.sendall(query.encode("utf-8") + b'\n')
    received = ""
    while True:
        try:
            received += sock.recv(4096).decode("utf-8")
            if "\n\n\n" in received:
                break
        except:
            break
    return received


def get(subject):
    response = query_ripe(subject)
    lines = response.split("\n")
    result = ""
    before_blank = True
    for line in lines:
        if len(line) > 0:
            if not line[0] == "%":
                before_blank = False
                result += line + "\n"
        elif not before_blank:
            before_blank = True
            result += "\n"
    while True:
        if result[-1] == "\n":
            result = result[:-1]
        else:
            break
    return result
    
