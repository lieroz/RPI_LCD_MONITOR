from __future__ import print_function
from collections import OrderedDict, namedtuple
from multiprocessing import Process
from gpio_listener import GPIO_listener
import pprint
import os
import glob
import re


class OS_poller(Process):
    def __init__(self, chan_out, chan_in):
        super().__init__()
        self.chan_out = chan_out
        self.chan_in = chan_in

    def run(self):
        while True:
            pin = self.chan_out.get()

            if pin == GPIO_listener.BUTTON_NEXT_GPIO:
                self.cpuinfo()
            elif pin == GPIO_listener.BUTTON_PREV_GPIO:
                self.meminfo()
            else:
                self.chan_in.put("Not registered input source, plz contact a developer!!!")

    def cpuinfo(self):
        cpuinfo = OrderedDict()
        procinfo = OrderedDict()
        nprocs = 0

        with open("/proc/cpuinfo") as f:
            for line in f:
                if not line.strip():
                    cpuinfo["proc%s" % nprocs] = procinfo
                    nprocs += 1
                    procinfo = OrderedDict()
                else:
                    if len(line.split(":")) == 2:
                        procinfo[line.split(":")[0].strip()] = line.split(":")[1].strip()
                    else:
                        procinfo[line.split(":")[0].strip()] = ""
 
        for processor in cpuinfo.keys():
            self.chan_in.put(cpuinfo[processor]["model name"])
            break

    def meminfo(self):
        meminfo = OrderedDict()

        with open("/proc/meminfo") as f:
            for line in f:
                meminfo[line.split(":")[0]] = line.split(":")[1].strip()
        
        self.chan_in.put("Total memory: {0}".format(meminfo["MemTotal"]))
        print("Total memory: {0}".format(meminfo["MemTotal"]))
        print("Free memory: {0}".format(meminfo["MemFree"]))

    def netdevs(self):
        with open("/proc/net/dev") as f:
            net_dump = f.readlines()
        
        device_data = {}
        data = namedtuple("data", ["rx", "tx"])

        for line in net_dump[2:]:
            line = line.split(":")
            if line[0].strip() != "lo":
                device_data[line[0].strip()] = data(
                        float(line[1].split()[0]) / (1024.0 * 1024.0), 
                        float(line[1].split()[8]) / (1024.0 * 1024.0))
        
        for dev in device_data.keys():
            print("{0}: {1} MiB {2} MiB".format(dev, round(device_data[dev].rx, 2), round(device_data[dev].tx, 2)))

    def process_list(self):
        pids = []

        for subdir in os.listdir("/proc"):
            if subdir.isdigit():
                pids.append(subdir)

        print("Total number of running processes: {0}".format(len(pids)))


    def size(self, device):
        nr_sectors = open(device + "/size").read().rstrip("\n")
        sect_size = open(device + "/queue/hw_sector_size").read().rstrip("\n")
        return (float(nr_sectors) * float(sect_size)) / (1024.0 * 1024.0 * 1024.0)

    def detect_devs(self):
        dev_pattern = ["sd.*","mmcblk*"]

        for device in glob.glob("/sys/block/*"):
            for pattern in dev_pattern:
                if re.compile(pattern).match(os.path.basename(device)):
                    print("Device:: {0}, Size:: {1} GiB".format(device, self.size(device)))

