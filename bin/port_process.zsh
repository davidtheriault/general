#!/bin/zsh
# Written by David Theriault
# ./port_proess.zsh [port]
# if given port, get process
# information for given port.
# otherwise, get info for all
# TCP listening ports.

if [ $# -eq 0 ];
    then
    lsof -P -i TCP -sTCP:LISTEN
else
    lsof -i:$1 -P -sTCP:LISTEN
fi
