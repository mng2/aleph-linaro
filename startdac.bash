#!/bin/bash

python setupclocks.py
echo "Setting txenable low..."
./uiopoke -d /dev/uio3 -a 0 -w 0
python setupdac.py
echo "Deassert DDS sclr..."
./uiopoke -d /dev/uio2 -a 0 -w 1
./uiopoke -d /dev/uio2 -a 0 -w 17
echo "Loading DDS..."
./uiopoke -d /dev/uio2 -a 0 -w 1
echo "Asserting txenable..."
./uiopoke -d /dev/uio3 -a 0 -w 16

