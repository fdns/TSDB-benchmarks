import matplotlib.pyplot as plt
from loader import load
import logging

def graph_query_time(data):
    data = data['query']
    fig = plt.figure()
    plt.figure(fig.number)
    plt.plot(data, range(len(data)))

def graph_cpu_usuage(data, label, fig=None):
    if fig is None:
        fig = plt.figure()
    data = data['stats']
    plt.figure(fig.number)
    plt.title('Tiempo de CPU utilizado Vs Tiempo')
    plt.xlabel('Tiempo desde inicio de mediciones [segundos]')
    plt.ylabel('Tiempo de CPU utilizado desde inicio de las mediciones [jiffies]')
    baset = data[0]['timestamp']
    base_cpu = data[0]['cpu']
    plot, = plt.plot([(x['timestamp'] - baset) for x in data], [(x['cpu'] - base_cpu) for x in data], label=label)
    plt.legend()
    #plt.legend(handles=[plot])
    return fig


def graph_disk_usuage(data):
    data = data['stats']
    fig = plt.figure()
    plt.figure(fig.number)
    plt.title('Espacio utilizado en memoria disco Vs Tiempo')
    plt.xlabel('Tiempo desde inicio de mediciones [segundos]')
    plt.ylabel('Espacio utilizado en disco [megabytes]')
    base = data[0]['timestamp']
    plt.plot([(x['timestamp'] - base) for x in data], [(x['disk'])/1024/1024 for x in data])

def graph_memory_usuage(data):
    data = data['stats']
    fig = plt.figure()
    plt.figure(fig.number)
    plt.title('Espacio utilizado en memoria primaria Vs Tiempo')
    plt.xlabel('Tiempo desde inicio de mediciones [segundos]')
    plt.ylabel('Espacio utilizado en memoria primaria [megabytes]')
    base = data[0]['timestamp']
    plt.plot([(x['timestamp'] - base) for x in data], [(x['memory'])/1024/1024 for x in data])

def main():
    tests = ['domain']
    databases = [('clickhouse', 'ClickHouse'),
                 ('druid', 'Druid'),
                 ('elasticsearch', 'ElasticSearch'),
                 ('influxdb', 'InfluxDB'),
                 ('prometheus', 'Prometheus'),
                 ('opentsdb', 'OpenTSDB')]
    for test in tests:
        fig = None
        for db in databases:
            data = load('../../out/{}_{}_1.out'.format(db[0], test))
            fig = graph_cpu_usuage(data, db[1], fig)
    #graph_disk_usuage(data)
    #graph_memory_usuage(data)
    #print data
    plt.show()

if __name__ == '__main__':
    logging.basicConfig()
    main()
