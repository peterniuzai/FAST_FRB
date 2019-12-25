#!/bin/bash

#Serverlist=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
#Serverlist=[2,3,4,6,7,8,10,12,13,14,15,16,17,18,19,20,21]
Serverlist=[7,9,10,13,14,15,16,17,18,19,20,21]
echo We Gonna Echo the status of X-serise GPU Server: $Serverlist
#pdsh -w x$Serverlist "date"
#pdsh -w x$Serverlist "top > grep 'nch'"
pdsh -w x$Serverlist "nvidia-smi | grep 'heimdall'"


