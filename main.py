from __future__ import print_function
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vmodl, vim
from colored import fore, back, style
import time
import sys

import atexit
import ssl

import modules.strings as strs
import modules.config as cfg
from modules.vm_scanner.getProperties import GetProperties
from modules.vm_scanner.getPerf import getVMPerf


def scanVM():
    interval = cfg.vspehre['interval']
    try:
        while True:
            si = None
            try:
                if cfg.vspehre['skipSSL']:
                    context = ssl._create_unverified_context()
                    si = SmartConnect(host=cfg.vspehre['host'],
                                      user=cfg.vspehre['user'],
                                      pwd=cfg.vspehre['password'],
                                      port=int("443"),
                                      sslContext=context)
                else:
                    si = SmartConnect(host=cfg.vspehre['host'],
                                      user=cfg.vspehre['user'],
                                      pwd=cfg.vspehre['password'],
                                      port=int("443"))
            except IOError as e:
                pass
            if not si:
                print(strs.connError)
                return -1

            atexit.register(Disconnect, si)
            content = si.RetrieveContent()
            # Get vCenter date and time for use as baseline when querying
            vchtime = si.CurrentTime()

            # Get all the performance counters
            perf_dict = {}
            perfList = content.perfManager.perfCounter
            for counter in perfList:
                counter_full = "{}.{}.{}".format(counter.groupInfo.key,
                                                 counter.nameInfo.key,
                                                 counter.rollupType)
                perf_dict[counter_full] = counter.key

            retProps = GetProperties(content,
                                     [vim.VirtualMachine],
                                     ['name',
                                      'runtime.powerState',
                                      'runtime.connectionState'],
                                     vim.VirtualMachine)

            for vm in retProps:
                if (vm['runtime.powerState'] == "poweredOn") \
                    and \
                   (vm['runtime.connectionState'] != "disconnected"):

                    print('*' * 20)
                    print('[x] ' + vm['name'])
                    getVMPerf(vm['moref'], content, vchtime,
                              int(interval), perf_dict)
                else:
                    print(strs.vmError.format(fore.LIGHT_BLUE, back.RED,
                                              style.BOLD, vm['name'],
                                              style.RESET))
                # time.sleep(2)

    except vmodl.MethodFault as e:
        print('Caught vmodl fault : ' + e.msg)
        return -1
    except Exception as e:
        print('Caught exception : ' + str(e))
        # return -1

    return 0


if __name__ == '__main__':
    try:
        scanVM()
    except KeyboardInterrupt:
        time.sleep(1)
        sys.exit()
