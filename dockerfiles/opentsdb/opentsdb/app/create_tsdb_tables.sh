
#!/bin/bash

export COMPRESSION="gz"
export HBASE_HOME=/opt/hbase

cd /usr/share/opentsdb
./tools/create_table.sh
touch /opt/opentsdb_tables_created.txt
