#!/bin/bash
set -e

/hbase/bin/start-hbase.sh
/hbase/bin/hbase thrift start-foreground
