# vCenter Perfomance Getter
#### Getting performance metrics from VMware vCenter

##### Setup
Required [vmware/pyvmomi](https://github.com/vmware/pyvmomi) and [dslackw/colored](https://github.com/dslackw/colored)

Basically installing using pip:
```sh
pip install pyvmomi colored
```

#### Config
./modules/config.py

If using rabbitMQ, add to config:
```python
rMQ = {"host": "YOU_VSPHERE_ADDR",
       "user": "USER",
       "password": "PASS"
       }

```

##### Storing in MySQL
Storing VM Data:
```sql
CREATE TABLE `vms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vm_name` text,
  `guest_os` text,
  `nicInfo` longtext,
  `disks` longtext,
  `cpus` varchar(45) DEFAULT NULL,
  `coresOnSocket` varchar(45) DEFAULT NULL,
  `ram` varchar(45) DEFAULT NULL,
  `hostName` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=287 DEFAULT CHARSET=utf8;
```
Storing Host Data:
```sql
CREATE TABLE `vms_hosts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cpu` varchar(255) DEFAULT NULL,
  `ramSize` varchar(255) DEFAULT NULL,
  `hostname` varchar(45) DEFAULT NULL,
  `mbVendor` varchar(45) DEFAULT NULL,
  `cpuFrequency` varchar(45) DEFAULT NULL,
  `mbModel` varchar(45) DEFAULT NULL,
  `hostOS` varchar(45) DEFAULT NULL,
  `cpuPackages` varchar(45) DEFAULT NULL,
  `cpuCores` varchar(45) DEFAULT NULL,
  `managementIp` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8;
```
Perf Data:
```sql
CREATE TABLE `vms_perf_counters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vm_id` int(11) DEFAULT NULL,
  `host_id` int(11) DEFAULT NULL,
  `vm_cpu_percent` varchar(255) DEFAULT NULL,
  `vm_mem_act` varchar(255) DEFAULT NULL,
  `vm_mem_usage` varchar(255) DEFAULT NULL,
  `vm_datastore_av_io` varchar(255) DEFAULT NULL,
  `vm_datastore_av_latency` varchar(255) DEFAULT NULL,
  `vm_av_netusage` varchar(255) DEFAULT NULL,
  `datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idvms_perf_counters_UNIQUE` (`id`),
  KEY `datetime` (`datetime`)
) ENGINE=InnoDB AUTO_INCREMENT=5451 DEFAULT CHARSET=utf8;
```
