#!/bin/bash

#Serverlist=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
Serverlist=[6,7,8,9,10,12,13,14,15,17,18,19,20,21]
echo We Gonna Kill the Heimdall and Python on X-serise GPU Server: $Serverlist
#pdsh -w x$Serverlist "date"

pdsh -w x$Serverlist "pkill -9 heimdall"

pdsh -w x$Serverlist "pkill -9 python"
