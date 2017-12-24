connError = 'Could not connect to the specified host using specified username and password'
vmError = '{}{}{}ERROR: Problem connecting to Virtual Machine. {} is likely powered off or suspended {}'
# emptyRes = 'ERROR: Performance results empty. TIP: Check time drift on source and vCenter server'
emptyRes = '{}{}{}ERROR: Performance results empty.\n TIP: Check time drift on source and vCenter server{}'
## Query
vmGetId = "SELECT id FROM `perf`.`vms` WHERE vm_name='{}'"
hostGetId = "SELECT id FROM `perf`.`vms_hosts` WHERE hostname='{}'"

vmQuery = "INSERT INTO `perf`.`vms` (`vm_name`, `hostName`, `guest_os`, `nicInfo`, `disks`, `cpus`, `coresOnSocket`, `ram`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"

hostQuery = "INSERT INTO `perf`.`vms_hosts` (`cpu`, `ramSize`, `hostname`, `mbVendor`, `cpuFrequency`, `mbModel`, `hostOS`, `cpuPackages`, `cpuCores`, `managementIp`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"

perfQuery = "INSERT INTO `perf`.`vms_perf_counters` (`vm_id`, `host_id`, `vm_cpu_percent`, `vm_mem_act`, `vm_mem_usage`, `vm_datastore_av_io`, `vm_datastore_av_latency`, `vm_av_netusage`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"
