#!/bin/bash

VENV=venv
SOURCE=${BASH_SOURCE[0]}
DIR=`dirname $SOURCE`
DATE_PREFIX=`date +%Y%m%d`
cd $DIR && mkdir -p log && $VENV/bin/python ./main.py -v 2>&1 | tee -a log/$DATE_PREFIX.log

