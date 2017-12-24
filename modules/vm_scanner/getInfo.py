from modules.helpers import convert_size_storage


def getVmInfo(vm, content, vchtime, interval, perf_dict, ):
    result = {"guest_os": vm.config.guestFullName,
              "ram": str(vm.config.hardware.memoryMB / 1024) + "GB",
              "cpus": vm.config.hardware.numCPU,
              "coresOnSocket": vm.config.hardware.numCoresPerSocket,
              "disks": [],
              "vm_name": vm.name,
              "hostName": vm.guest.hostName,
              "nicInfo": []}
    disks = vm.guest.disk
    for i in disks:
        result['disks'].append({"path": i.diskPath,
                                "capacity": convert_size_storage(i.capacity),
                                "freeSpace": convert_size_storage(i.freeSpace)})
    net = vm.guest.net
    for i in net:
        result['nicInfo'].append({"ip": i.ipAddress,
                                  "mac": i.macAddress})
    return result


def getHostInfo(vm, content, vchtime, interval, perf_dict, ):
    host = vm.summary.runtime.host
    result = {"hostname": host.name,
              "hostOS": host.config.product.fullName,
              "managementIp": host.summary.managementServerIp,
              "mbVendor": host.hardware.systemInfo.vendor,
              "mbModel": host.hardware.systemInfo.model,
              "cpu": host.summary.hardware.cpuModel,
              "cpuFrequency": int(host.hardware.cpuInfo.hz / (pow(10, 6))),
              "cpuCores": host.hardware.cpuInfo.numCpuCores,
              "cpuPackages": host.hardware.cpuInfo.numCpuPackages,
              "cpuThreads": host.hardware.cpuInfo.numCpuThreads,
              "ramSize": convert_size_storage(host.hardware.memorySize)}

    return result
