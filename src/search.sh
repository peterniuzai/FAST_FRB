#!/bin/bash

if [ ! -d "/data26/home/nch/FAST_Miner/Logfile/$1/" ]; then

	mkdir -p "/data26/home/nch/FAST_Miner/Logfile/$1/"

fi

MaxDM=5000


python /data26/home/nch/FAST_Miner/src/start_huntting_even.py $1 $2 $MaxDM>>/data26/home/nch/FAST_Miner/Logfile/$1/$HOSTNAME.log 2>>/data26/home/nch/FAST_Miner/Logfile/$1/$HOSTNAME_error.log &
python /data26/home/nch/FAST_Miner/src/start_huntting_odd.py $1 $2 $MaxDM>>/data26/home/nch/FAST_Miner/Logfile/$1/$HOSTNAME.log 2>>/data26/home/nch/FAST_Miner/Logfile/$1/$HOSTNAME_error.log 

echo Huntting Complete!
#python /data26/home/nch/FAST_Miner/second_huntting_even.py $1 $2 $MaxDM>> /data26/home/nch/FAST_Miner/Logfile/$1/$HOSTNAME.log &
#python /data26/home/nch/FAST_Miner/second_huntting_odd.py $1 $2 $MaxDM>> /data26/home/nch/FAST_Miner/Logfile/$1/$HOSTNAME.log 
###Even and Odd is in order to maximum use the Ability of 2GPUs in a server.
