#!/bin/bash

file=${1}
export_path=${2}
if [ -z "${file}" ] || [ -z "${export_path}" ]
then
    echo "Please insert path of download data and export_path"
else
    echo "Unzip Start"
    data=$file
    unzip -O cp949 $data -d $GEO_DATA_HOME/${export_path}
fi
