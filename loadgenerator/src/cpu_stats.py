from subprocess import check_output
from threading import Lock
import re

def fetch_proc_stats(pid):
    filename = '/proc/{}/stat'.format(pid)
    with open(filename) as stat_file:
        line = stat_file.readline()
        data = line.split(' ')
        cpu_time = int(data[14]) + int(data[15])
        memory = float(data[23])
        return (cpu_time, memory)
    raise ValueError('Pid not found or couldn\'t open the {} file'.format(filename))

mutex = Lock()
def fetch_docker_disk_usuage(volume):
    regex = re.compile(r'(\d+(?:\.\d+)?)\s*([kmgtp]?[Bb])', re.IGNORECASE)
    order = ['b', 'kb', 'mb', 'gb', 'tb']
    with mutex:
        size = check_output("docker system df -v | grep {} | awk '{{ print $3 }}'".format(volume), shell=True)
        value, unit = regex.findall(size)[0]
        return float(value) * (1024**order.index(unit.lower()))
