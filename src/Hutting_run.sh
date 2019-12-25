#!/bin/bash
Serverlist=[6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
#Serverlist=[7,9,10,13,14,15,17,18,19,20,21]
echo We Gonna use X-serise GPU Server: $Serverlist
pdsh -w x$Serverlist "sh /data26/home/nch/FAST_Miner/src/search.sh '201809/' $Serverlist" 
