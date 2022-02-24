import socket


def resolve_ip(hostname):
    isWebAddr = False
    try:
        if hostname[:4] == "www.":
            hostname = hostname[4:]
    except: pass
    ip_base = socket.gethostbyname(hostname)
    try:
        ip_web = socket.gethostbyname("www." + hostname)
    except: ip_web = ip_base
    if ip_base == ip_web:
        return (ip_base, None)
    else:
        return (ip_base, ip_web, None)

