from subprocess import check_output
from threading import Lock
import re

import logging
logger = logging.getLogger(__name__)


def fetch_proc_stats(pids):
    memory = 0
    for pid in pids.split('\n'):
        try:
            result = check_output("ps --no-headers -o rss {}".format(pid), shell=True)
        except Exception as e:
            logger.exception(e)
            import os
            os._exit(0)
        memory += int(result.strip())
    return (fetch_cpu_stats(pids), memory)

def fetch_cpu_stats(pids):
    cpu = 0
    for pid in pids.split('\n'):
        with open('/proc/{}/stat'.format(pid)) as stat_file:
            line = stat_file.readline()
            data = line.split(' ')
            cpu += int(data[13]) + int(data[14])
    return cpu

mutex = Lock()
def fetch_docker_disk_usuage(volume):
    regex = re.compile(r'(\d+(?:\.\d+)?)\s*([kmgtp]?[Bb])', re.IGNORECASE)
    order = ['b', 'kb', 'mb', 'gb', 'tb']
    with mutex:
        size = check_output("docker system df -v | grep {} | awk '{{ print $3 }}'".format(volume), shell=True)
        value, unit = regex.findall(size)[0]
        return float(value) * (1024**order.index(unit.lower()))
