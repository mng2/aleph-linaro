#!/bin/bash

echo "Asserting txenable..."
./uiopoke -d /dev/uio4 -a 0 -w 16

