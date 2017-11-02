import matplotlib.pyplot as plt
from loader import load
import logging

def graph_cpu_usage_average(data, label, testname, fig=None, index=0):
    if fig is None:
        fig = plt.figure()
    data = data['stats']
    plt.figure(fig.number)
    plt.title('{}: Tiempo de CPU utilizado promedio Vs Tiempo'.format(testname))
    plt.xlabel('Tiempo desde inicio de mediciones [minutos]')
    plt.ylabel('Tiempo de CPU utilizado promedio [segundos]')

    baset = data[0]['timestamp']
    time = [(x['timestamp'] - baset)/60 for x in data]

    # Translate to a diff array
    diffs = []
    for i in range(1, len(data)):
        diffs.append((data[i]['cpu'] - data[i-1]['cpu'])/100.)
    time = time[1:]

    # Calculating a moving average
    moving = []
    result = []
    for x in diffs:
        moving.append(x)
        if len(moving) > 20:
            moving.pop(0)
        result.append(sum(moving)/len(moving))

    # Calculate the trend
    #import numpy
    #z = numpy.polyfit(time, result, 1)
    #p = numpy.poly1d(z)
    #plt.plot(time, p(time), label=label)
    plt.plot(time, result, label=label)
    plt.legend()
    return fig

def graph_cpu_usuage(data, label, testname, fig=None, index=0):
    if fig is None:
        fig = plt.figure()
    data = data['stats']
    plt.figure(fig.number)
    plt.title('{}: Tiempo de CPU utilizado Vs Tiempo'.format(testname))
    plt.xlabel('Tiempo desde inicio de mediciones [minutos]')
    plt.ylabel('Tiempo de CPU utilizado desde inicio de las mediciones [segundos]')
    baset = data[0]['timestamp']
    base_cpu = data[0]['cpu']
    plt.plot([(x['timestamp'] - baset)/60 for x in data], [(x['cpu'] - base_cpu)/100 for x in data], label=label)
    plt.legend()
    return fig


def graph_disk_usuage(data, label, testname, fig=None, index=0):
    if fig is None:
        fig = plt.figure()
    data = data['stats']
    plt.figure(fig.number)
    plt.title('{}: Espacio utilizado en memoria secundaria Vs Tiempo'.format(testname))
    plt.xlabel('Tiempo desde inicio de mediciones [minutos]')
    plt.ylabel('Espacio utilizado en memoria secundaria [megabytes]')
    base = data[0]['timestamp']
    plt.plot([(x['timestamp'] - base)/60 for x in data], [(x['disk'])/1024/1024 for x in data], label=label)
    plt.legend()
    return fig

def graph_memory_usuage(data, label, testname, fig=None, index=0):
    if fig is None:
        fig = plt.figure()
    data = data['stats']
    plt.figure(fig.number)
    plt.title('{}: Espacio utilizado en memoria primaria Vs Tiempo'.format(testname))
    plt.xlabel('Tiempo desde inicio de mediciones [minutos]')
    plt.ylabel('Espacio utilizado en memoria primaria [megabytes]')
    base = data[0]['timestamp']
    plt.plot([(x['timestamp'] - base)/60 for x in data], [(x['memory'])/1024/1024 for x in data], label=label)
    plt.legend()
    return fig

def graph_query_time(data, label, testname, fig=None, index=0):
    if fig is None:
        fig = plt.figure()
    data = data['query']
    plt.figure(fig.number)
    plt.title('{}: Tiempo de consulta Vs Tiempo'.format(testname))
    plt.xlabel('Tiempo desde inicio de mediciones [minutos]')
    plt.ylabel('Tiempo utilizado en obtener los datos [minutos]')
    base = data[0][0]
    plt.plot([(x[0]-base)/60 for x in data], [x[1] for x in data], label=label)
    plt.legend()
    return fig

LABELS={}
def graph_bar_query_time(data, label, testname, fig=None, index=0):
    global LABELS
    if fig is None:
        fig = plt.figure()
        LABELS[testname] = []

    data = data['query']
    plt.figure(fig.number)
    plt.title('{}: Tiempo de consulta Vs Tiempo'.format(testname))
    plt.xlabel('Tiempo desde inicio de mediciones [minutos]')
    plt.ylabel('Tiempo utilizado en obtener los datos [minutos]')
    base = data[0][0]
    lowcap = base + 4*60*60
    upcap = lowcap + 2*60*60

    values = [x[1] for x in data if lowcap <= x[0] <= upcap]
    if len(values) > 0:
        LABELS[testname].append(label)
        plt.bar(len(LABELS[testname])*0.6, sum(values) / len(values), width=0.4, label=label)
        plt.xticks([(x+1) * 0.6 for x in range(len(LABELS[testname]))], LABELS[testname])
        plt.legend()

    return fig


def main():
    graphs = (
        graph_cpu_usuage,
        graph_disk_usuage,
        graph_memory_usuage,
        graph_query_time,
        graph_cpu_usage_average,graph_bar_query_time)
    tests = [
        ('domain', 'Dominio'),
        ('mask', 'Mascara de Red'),
        ('length', 'Largode paquetes')
    ]
    databases = [('clickhouse', 'ClickHouse'), # Require SSE4.2
                 ('druid', 'Druid'),
                 ('elasticsearch', 'ElasticSearch'),
                 ('influxdb', 'InfluxDB'),
                 ('prometheus', 'Prometheus'),
                 ('opentsdb', 'OpenTSDB')
    ]
    for test in tests:
        fig = [None for _ in range(len(graphs))]
        index = [0 for _ in range(len(graphs))]
        for db in databases:
            data = load('../../out/{}_{}_1.out'.format(db[0], test[0]))
            if data:
                for i in range(len(graphs)):
                    fig[i] = graphs[i](data, db[1], test[1], fig[i], index[i])
                    index[i] += 1
    plt.show()

if __name__ == '__main__':
    logging.basicConfig()
    main()
