#!/bin/bash

echo "Copying starter files into /home/jovyan/work..."
cp -r /starter_files/* /home/jovyan/work/

start.sh jupyter lab

