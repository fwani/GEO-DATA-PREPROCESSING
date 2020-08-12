#!/usr/bin/env bash

export GEO_DATA_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Thirdparty library
export PYTHONPATH=$GEO_DATA_HOME:$PYTHONPATH

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
