#!/bin/bash
#Serverlist=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
#Serverlist=[3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21]
#Serverlist=[6,7,8,9,10,13,14,15,17,18,19,20,21]
#Serverlist=[6,8,11,12,16]
Serverlist=[6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]

echo We Gonna use X-serise GPU Server: $Serverlist
pdsh -w x$Serverlist "python /data26/home/nch/FAST_Miner/src/coincidencer_process.py '201810/' $Serverlist 8 300" 
