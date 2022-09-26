# -*- coding: utf-8 -*-
import re


# letters only string
def is_alpha(data):
    if data:
        try:
            if data.isalpha():
                return True
        except:
            pass
    return False


# alphanumberc string
def is_alphanum(data):
    if data:
        try:
            if data.isalnum():
                return True
        except:
            pass
    return False


# digits only string
def is_digit(data):
    if data:
        try:
            if str(data).isdigit():
                return True
        except:
            pass
    return False


# positive or negative numbers
def is_number(data):
    if data:
        try:
            if re.search('^[0-9-]+$', data):
                return True
        except:
            pass
    return False


# positive or negative decimals
def is_decimal(data):
    if data:
        try:
            if re.search('^[0-9-]+(.[0-9]+)?$', data):
                return True
        except:
            pass
    return False


# TCP IPv4 address
def is_tcp_ipv4(data):
    if data:
        try:
            parts = [(0 <= int(k) <= 255) for k in str(data).split('.')]
            if len(parts) == 4 and all(parts):
                return True
        except:
            pass
    return False


# TCP port
def is_tcp_port(data):
    if data:
        try:
            port = int(data)
            if 1 <= port <= 65535:
                return True
        except:
            pass
    return False
