from subprocess import check_output
from threading import Lock
import re
import os

import logging
logger = logging.getLogger(__name__)


def fetch_proc_stats(pids):
    memory = 0
    for pid in pids.split('\n'):
        try:
            result = check_output("ps --no-headers -o rss {}".format(pid), shell=True)
            memory += int(result.strip()) * 1024
        except Exception as e:
            logger.exception(e)
            logger.error('Error fetching resident memory of {}'.format(pid))
            os._exit(1)
    return (fetch_cpu_stats(pids), memory)

def fetch_cpu_stats(pids):
    cpu = 0
    for pid in pids.split('\n'):
        try:
            with open('/proc/{}/stat'.format(pid)) as stat_file:
                line = stat_file.readline()
                data = line.split(' ')
                cpu += int(data[13]) + int(data[14])
        except Exception as e:
            logger.exception(e)
            logger.error('Error analysing pids {}'.format(pids))
            os._exit(1)
    return cpu

mutex = Lock()
def fetch_docker_disk_usuage(volume):
    regex = re.compile(r'(\d+(?:\.\d+)?)\s*([kmgtp]?[Bb])', re.IGNORECASE)
    order = ['b', 'kb', 'mb', 'gb', 'tb']
    with mutex:
        size = check_output("docker system df -v | grep {} | awk '{{ print $3$4 }}'".format(volume), shell=True)
        value, unit = regex.findall(size)[0]
        return int(float(value) * (1024**order.index(unit.lower())))
