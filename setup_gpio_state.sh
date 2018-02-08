#!/bin/bash
for pin in 17 27 22 10 9 11 5 6 13
do
echo $pin > /sys/class/gpio/export
done
exit 0
