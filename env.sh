#!/usr/bin/env bash

export GEO_DATA_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

SPARK_VERSION=2.4.4
export SPARK_HOME=$GEO_DATA_HOME/thirdparty/spark-${SPARK_VERSION}-bin-hadoop2.7

# Thirdparty library
export PYTHONPATH=$GEO_DATA_HOME:$PYTHONPATH

# For Spark
export PYSPARK_PYTHON=python3

export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH

export OS="`uname`"
case $OS in
  'Linux')
    OS='Linux'
    export JAVA_HOME=$(readlink -f /usr/bin/javac | sed "s:/bin/javac::")
    ;;
  'Darwin') 
    OS='Mac'
    export JAVA_HOME=$(/usr/libexec/java_home)
    ;;
esac
