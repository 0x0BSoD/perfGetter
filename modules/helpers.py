from math import pow, floor, log

import modules.strings as strs
from modules.storing import query_toBase


def vmIdGetter(hostname):
    vm_id = query_toBase(strs.vmGetId.format(hostname))
    if vm_id:
        return vm_id
    else:
        return False


def hostIdGetter(hostname):
    vm_id = query_toBase(strs.hostGetId.format(hostname))
    if vm_id:
        return vm_id
    else:
        return False


def convert_size_storage(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(floor(log(size_bytes, 1024)))
    p = pow(1024, i)
    s = round(size_bytes / p, 2)
    return "{} {}".format(floor(s), size_name[i])
