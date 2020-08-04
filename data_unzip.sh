#!/bin/bash

arg=${1}
if [ -z "$arg" ]
then
    echo "Please insert path of download data file"
else
    echo "Unzip Start"
    data=$arg
    unzip -O cp949 $data -d $GEO_DATA_HOME/data/address_cp949/
fi
