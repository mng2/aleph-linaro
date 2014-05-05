#!/bin/bash

echo "Setting txenable low..."
./uiopoke -d /dev/uio4 -a 0 -w 0
echo "Done."
