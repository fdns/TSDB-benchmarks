FROM yandex/clickhouse-server:1.1

RUN sed -i 's,<listen_host>::1</listen_host>,<listen_host>0.0.0.0</listen_host>,' /etc/clickhouse-server/config.xml && \
    sed -i 's,<listen_host>::</listen_host>,,' /etc/clickhouse-server/config.xml &&\
    sed -i 's,<level>trace</level>,<level>information</level>,' /etc/clickhouse-server/config.xml

