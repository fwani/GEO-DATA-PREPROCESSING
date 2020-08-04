#!/usr/bin/env bash

declare -a SPARK_VERSIONS=(2.4.4)

if [ ! -d thirdparty ]; then
    mkdir thirdparty
fi

cd thirdparty

for SPARK_VERSION in "${SPARK_VERSIONS[@]}"
do
if [ ! -f spark-$SPARK_VERSION-bin-hadoop2.7.tgz ]; then
    curl -O https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop2.7.tgz
fi
tar xvfz spark-$SPARK_VERSION-bin-hadoop2.7.tgz
done
cd ..

# Set logs off for Spark.
# cp etc/log4j.properties $SPARK_HOME/conf/log4j.properties
