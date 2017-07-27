from subprocess import check_output
from threading import Lock
import re

import logging
logger = logging.getLogger(__name__)


def fetch_proc_stats(pids):
    cpu, memory = 0,0
    for pid in pids.split('\n'):
        try:
            result = check_output("ps --no-headers -o %cpu,rss {}".format(pid), shell=True)
        except Exception as e:
            logger.exception(e)
            import time
            time.sleep(60)
            import os
            os._exit(0)
        result = result.strip().split(' ')
        cpu += float(result[0])
        memory += int(result[1])
    return (fetch_proc_stats_old(pids), memory)

def fetch_proc_stats_old(pids):
    """Deprecated, use the /proc file"""
    cpu, memory = 0,0
    for pid in pids.split('\n'):
        with open('/proc/{}/stat'.format(pid)) as stat_file:
            line = stat_file.readline()
            data = line.split(' ')
            cpu += int(data[13]) + int(data[14])
            #cpu, memory = (cpu + cpu_time, memory + int(data[23]))
    return cpu
    return (cpu, memory)

mutex = Lock()
def fetch_docker_disk_usuage(volume):
    regex = re.compile(r'(\d+(?:\.\d+)?)\s*([kmgtp]?[Bb])', re.IGNORECASE)
    order = ['b', 'kb', 'mb', 'gb', 'tb']
    with mutex:
        size = check_output("docker system df -v | grep {} | awk '{{ print $3 }}'".format(volume), shell=True)
        value, unit = regex.findall(size)[0]
        return float(value) * (1024**order.index(unit.lower()))
