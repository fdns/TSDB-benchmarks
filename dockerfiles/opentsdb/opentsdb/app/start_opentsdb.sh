#!/bin/bash
echo "Sleeping for 30 seconds to give HBase time to warm up"
sleep 30 

if [ ! -e /opt/opentsdb_tables_created.txt ]; then
	echo "creating tsdb tables"
	bash /opt/bin/create_tsdb_tables.sh
	echo "created tsdb tables"
	/usr/share/opentsdb/bin/tsdb mkmetric domains
	/usr/share/opentsdb/bin/tsdb mkmetric masks
	/usr/share/opentsdb/bin/tsdb mkmetric length
	echo "domains created"
fi

echo "starting opentsdb"
/usr/share/opentsdb/bin/tsdb tsd
