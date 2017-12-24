from json import dumps

from modules.helpers import vmIdGetter, hostIdGetter
from modules.vm_scanner.getInfo import getVmInfo, getHostInfo
from modules.vm_scanner.buildQuery import BuildQuery as bq
import modules.strings as strs
from modules.storing import query_toBase


def statCheck(perf_dict, counter_name):
    counter_key = perf_dict[counter_name]
    return counter_key


def getVMPerf(vm, content, vchtime, interval, perf_dict, ):
    result = {"host": None, "vm": None, "pData": None}
    pData = {"vm_cpu_percent": None,
             "vm_mem_active": None,
             "vm_mem_usage": None,
             "vm_datastore_av_io": None,
             "vm_av_netusage": None}
    si = interval * 3  # There are 3 interval's samples in each minute
    vm_name = vm.name
    host_name = vm.summary.runtime.host.name
    vm_id = vmIdGetter(vm_name)
    host_id = hostIdGetter(host_name)
    if not vm_id:
        result['vm'] = getVmInfo(vm, content, vchtime, interval, perf_dict,)
        q = (strs.vmQuery.format(result['vm']['vm_name'],
                                 result['vm']['hostName'],
                                 result['vm']['guest_os'],
                                 dumps(result['vm']['nicInfo']),
                                 dumps(result['vm']['disks']),
                                 result['vm']['cpus'],
                                 result['vm']['coresOnSocket'],
                                 result['vm']['ram']))
        query_toBase(q)
        vm_id = vmIdGetter(vm_name)
    if not host_id:
        result['host'] = getHostInfo(vm, content, vchtime, interval, perf_dict,)
        q = (strs.hostQuery.format(result['host']['cpu'],
                                   result['host']['ramSize'],
                                   result['host']['hostname'],
                                   result['host']['mbVendor'],
                                   result['host']['cpuFrequency'],
                                   result['host']['mbModel'],
                                   result['host']['hostOS'],
                                   result['host']['cpuPackages'],
                                   result['host']['cpuCores'],
                                   result['host']['managementIp']))
        query_toBase(q)
        host_id = hostIdGetter(host_name)
    # Counters ================================================================
    # CPU Usage Average %
    statCpuUsage = bq(content, vchtime,
                      (statCheck(perf_dict, 'cpu.usage.average')),
                      "", vm, interval)
    cpuUsage = ((float(sum(statCpuUsage[0].value[0].value)) / si) / 100)

    # Mem Active Average MB
    statMemActive = bq(content, vchtime,
                       (statCheck(perf_dict, 'mem.active.average')),
                       "", vm, interval)
    memoryActive = (float(sum(statMemActive[0].value[0].value) / 1024) / si)

    # Mem Active Average %
    statMemUsage = bq(content, vchtime,
                      (statCheck(perf_dict, 'mem.usage.average')),
                      "", vm, interval)
    memoryUsage = ((float(sum(statMemUsage[0].value[0].value)) / si) / 100)

    # Datastore Average IO
    statDatastoreIoRead = bq(content, vchtime,
                             (statCheck(perf_dict,
                                        'datastore.numberReadAveraged.average')),
                             "*", vm, interval)
    DatastoreIoRead = (float(sum(statDatastoreIoRead[0].value[0].value)) / si)
    statDatastoreIoWrite = bq(content, vchtime,
                              (statCheck(perf_dict,
                                         'datastore.numberWriteAveraged.average')),
                              "*", vm, interval)
    DatastoreIoWrite = (float(sum(statDatastoreIoWrite[0].value[0].value)) / si)

    # Datastore Average Latency
    statDatastoreLatRead = bq(content, vchtime,
                              (statCheck(perf_dict,
                                         'datastore.totalReadLatency.average')),
                              "*", vm, interval)
    DatastoreLatRead = (float(sum(statDatastoreLatRead[0].value[0].value)) / si)
    statDatastoreLatWrite = bq(content, vchtime,
                               (statCheck(perf_dict,
                                          'datastore.totalWriteLatency.average')),
                               "*", vm, interval)
    DatastoreLatWrite = (float(sum(statDatastoreLatWrite[0].value[0].value)) / si)

    # Network usage (Tx/Rx)
    statNetworkTx = bq(content, vchtime,
                       (statCheck(perf_dict, 'net.transmitted.average')),
                       "", vm, interval)
    networkTx = (float(sum(statNetworkTx[0].value[0].value) * 8 / 1024) / si)
    statNetworkRx = bq(content, vchtime,
                       (statCheck(perf_dict, 'net.received.average')),
                       "", vm, interval)
    networkRx = (float(sum(statNetworkRx[0].value[0].value) * 8 / 1024) / si)

    pData['vm_id'] = vm_id[0][0]
    pData['host_id'] = host_id[0][0]
    pData['vm_cpu_percent'] = round(cpuUsage, 2)
    pData['vm_mem_active'] = round(memoryActive, 2)
    pData['vm_mem_usage'] = round(memoryUsage, 2)
    pData['vm_datastore_av_io'] = [round(DatastoreIoRead, 2), round(DatastoreIoWrite, 2)]
    pData['vm_datastore_av_lat'] = [round(DatastoreLatRead, 2), round(DatastoreLatWrite, 2)]
    pData['vm_av_netusage'] = [round(networkTx, 2), round(networkRx, 2)]

    result['pData'] = pData

    q = (strs.perfQuery.format(result['pData']['vm_id'],
                               result['pData']['host_id'],
                               result['pData']['vm_cpu_percent'],
                               result['pData']['vm_mem_active'],
                               result['pData']['vm_mem_usage'],
                               result['pData']['vm_datastore_av_io'],
                               result['pData']['vm_datastore_av_lat'],
                               result['pData']['vm_av_netusage']))
    query_toBase(q)
