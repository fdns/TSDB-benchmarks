FROM java:8u72-jre

RUN useradd opentsdb && \
    apt-get update && \
    apt-get install --no-install-recommends -y gnuplot-nox && \
    apt-get install -y --force-yes \
        rsyslog \
        supervisor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    curl -L https://github.com/OpenTSDB/opentsdb/releases/download/v2.3.0/opentsdb-2.3.0_all.deb > /tmp/opentsdb.deb && \
    dpkg -i /tmp/opentsdb.deb && \
    rm /tmp/opentsdb.deb && \
    curl -sL "https://github.com/tianon/gosu/releases/download/1.7/gosu-amd64" > /usr/sbin/gosu && \
    chmod +x /usr/sbin/gosu

RUN wget -O hbase-1.2.2.bin.tar.gz http://archive.apache.org/dist/hbase/1.2.2/hbase-1.2.2-bin.tar.gz && \
    tar xzvf hbase-1.2.2.bin.tar.gz && \
    mv hbase-1.2.2 /opt/hbase && \
    rm hbase-1.2.2.bin.tar.gz

RUN mkdir -p /data/hbase
 
ADD app/hbase-site.xml /opt/hbase/conf/
ADD app/start_opentsdb.sh /opt/bin/
ADD app/create_tsdb_tables.sh /opt/bin/

COPY ./logback.xml /etc/opentsdb/logback.xml
COPY ./run.sh /run.sh

ADD supervisord.conf /etc/supervisord.conf

VOLUME /data/hbase

expose 4242:4242

CMD ["/run.sh"]