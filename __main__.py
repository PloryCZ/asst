#!/usr/bin/env python3

import alpn
import ripe
import httplib
import resolver
import plaintext
from sys import exit
from sys import argv
from colorama import Fore, Style


def eval_args():
    args = argv[1:]
    flags = []
    targets = []
    for arg in args:
        if arg[:2] == "--":
            flags.append(arg[2:])
        else:
            targets.append(arg)
    return targets[0], tuple(flags)

if __name__ == "__main__":
    print()
    try:
        target, flags = eval_args()
        resolved = resolver.resolve_ip(target)
        if len(resolved) > 2:
            target_ip = resolved[1]
        else:
            target_ip = resolved[0]
    except:
        print(Fore.RED + "fatal error: domain name resolution" + Style.RESET_ALL)
        print()
        exit()
    try:
        if "all" in flags: allswitch = True
        else: allswitch = False
        if "alpn" in flags or allswitch:
            alpn_protocols = alpn.list(target_ip)
        if "prot" in flags or allswitch:
            plaintext_protocols = plaintext.list(target_ip)
        if "ripe" in flags or allswitch:
            ripe_response = ripe.get(target_ip)
        if "info" in flags or allswitch:
            info = httplib.get_info(target_ip)
    except:
        print(Fore.RED + "fatal error: property resolution" + Style.RESET_ALL)
        print()
        exit()
    if "resolve" in flags or allswitch:
        print("--RESOLUTION--")
        if len(resolved) > 2:
            print("domain: " + Fore.GREEN + resolved[0] + Style.RESET_ALL)
            print("www: " + Fore.GREEN + resolved[1] + Style.RESET_ALL)
        else:
            print("host: " + Fore.GREEN + resolved[0] + Style.RESET_ALL)
            print("www: " + Fore.RED + "assuming same addr" + Style.RESET_ALL)
        print()
    if "alpn" in flags or allswitch:
        print("--ALPN--")
        if "http/1.1" in alpn_protocols:
            print("http/1.1: " + Fore.GREEN + "ok" + Style.RESET_ALL)
        else:
            print("http/1.1: " + Fore.RED + "no" + Style.RESET_ALL)
        if "http/2" in alpn_protocols:
            print("http/2: " + Fore.GREEN + "ok" + Style.RESET_ALL)
        else:
            print("http/2: " + Fore.RED + "no" + Style.RESET_ALL)
        print()
    if "prot" in flags or allswitch:
        print("--PROTOCOLS--")
        if "http/1.0" in plaintext_protocols:
            print("http/1.0: " + Fore.GREEN + "ok" + Style.RESET_ALL)
        else:
            print("http/1.0: " + Fore.RED + "no" + Style.RESET_ALL)
        if "http/1.1" in plaintext_protocols:
            print("http/1.1: " + Fore.GREEN + "ok" + Style.RESET_ALL)
        else:
            print("http/1.1: " + Fore.RED + "no" + Style.RESET_ALL)
        print()
    if "info" in flags or allswitch:
        print("--HTTPINFO--")
        for key in info:
            if key == "server":
                if "apache/" in info[key]:
                    print("server: " + Fore.RED + info[key] + Style.RESET_ALL + " - exposed Apache version")
                else:
                    print("server: " + Fore.GREEN + info[key] + Style.RESET_ALL)
            elif key == "tls/ssl":
                if info[key] == "no":
                    print("tls/ssl: " + Fore.RED + "no" + Style.RESET_ALL)
                else:
                    print("tls/ssl: " + Fore.GREEN + info[key] + Style.RESET_ALL)
            else:
                print(key + ": " + Fore.GREEN + info[key] + Style.RESET_ALL)
        print()
    if "ripe" in flags or allswitch:
        print("--RIPE--")
        print(Fore.YELLOW + ripe_response + Style.RESET_ALL)
        print()

