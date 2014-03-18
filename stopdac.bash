#!/bin/bash

echo "Setting txenable low..."
./uiopoke -d /dev/uio3 -a 0 -w 0
echo "Done."
