import matplotlib.pyplot as plt
from loader import load
import logging

def graph_query_time(data):
    data = data['query']
    fig = plt.figure()
    plt.figure(fig.number)
    plt.plot(data, range(len(data)))

def graph_cpu_usuage(data, label, testname, fig=None):
    if fig is None:
        fig = plt.figure()
    data = data['stats']
    plt.figure(fig.number)
    plt.title('{}: Tiempo de CPU utilizado Vs Tiempo'.format(testname))
    plt.xlabel('Tiempo desde inicio de mediciones [segundos]')
    plt.ylabel('Tiempo de CPU utilizado desde inicio de las mediciones [jiffies]')
    baset = data[0]['timestamp']
    base_cpu = data[0]['cpu']
    plt.plot([(x['timestamp'] - baset) for x in data], [(x['cpu'] - base_cpu) for x in data], label=label)
    plt.legend()
    return fig


def graph_disk_usuage(data, label, testname, fig=None):
    if fig is None:
        fig = plt.figure()
    data = data['stats']
    plt.figure(fig.number)
    plt.title('{}: Espacio utilizado en memoria secundaria Vs Tiempo'.format(testname))
    plt.xlabel('Tiempo desde inicio de mediciones [segundos]')
    plt.ylabel('Espacio utilizado en memoria secundaria [megabytes]')
    base = data[0]['timestamp']
    plt.plot([(x['timestamp'] - base) for x in data], [(x['disk'])/1024/1024 for x in data], label=label)
    plt.legend()
    return fig

def graph_memory_usuage(data, label, testname, fig=None):
    if fig is None:
        fig = plt.figure()
    data = data['stats']
    plt.figure(fig.number)
    plt.title('{}: Espacio utilizado en memoria primaria Vs Tiempo'.format(testname))
    plt.xlabel('Tiempo desde inicio de mediciones [segundos]')
    plt.ylabel('Espacio utilizado en memoria primaria [megabytes]')
    base = data[0]['timestamp']
    plt.plot([(x['timestamp'] - base) for x in data], [(x['memory'])/1024/1024 for x in data], label=label)
    plt.legend()
    return fig

def graph_query_time(data, label, testname, fig=None):
    if fig is None:
        fig = plt.figure()
    data = data['query']
    plt.figure(fig.number)
    plt.title('{}: Tiempo de consulta Vs Tiempo'.format(testname))
    plt.xlabel('Tiempo desde inicio de mediciones [segundos]')
    plt.ylabel('Tiempo utilizado en obtener los datos [segundos]')
    base = data[0][0]
    plt.plot([x[0]-base for x in data], [x[1] for x in data], label=label)
    plt.legend()
    return fig

def main():
    graphs = (graph_cpu_usuage, graph_disk_usuage, graph_memory_usuage, graph_query_time)
    tests = [('domain', 'Dominio'), ('mask', 'Mascara de Red'), ('length', 'Largode paquetes')]
    databases = [#('clickhouse', 'ClickHouse'), # Require SSE4.2
                 ('druid', 'Druid'),
                 ('elasticsearch', 'ElasticSearch'),
                 ('influxdb', 'InfluxDB'),
                 ('prometheus', 'Prometheus'),
                 ('opentsdb', 'OpenTSDB')
    ]
    for test in tests:
        fig = [None for _ in range(len(graphs))]
        for db in databases:
            data = load('../../out/{}_{}_1.out'.format(db[0], test[0]))
            if data:
                for i in range(len(graphs)):
                    fig[i] = graphs[i](data, db[1], test[1], fig[i])
    plt.show()

if __name__ == '__main__':
    logging.basicConfig()
    main()
