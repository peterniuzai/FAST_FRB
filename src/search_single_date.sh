#!/bin/bash
python /data26/home/nch/FAST_Miner/src/start_huntting_even_single.py >> /data26/home/nch/FAST_Miner/Logfile/Single_$HOSTNAME.log &
python /data26/home/nch/FAST_Miner/src/start_huntting_odd_single.py >> /data26/home/nch/FAST_Miner/Logfile/Single_$HOSTNAME.log 

#python /data26/home/nch/FAST_Miner/second_huntting_even.py >> /data26/home/nch/FAST_Miner/Logfile/$HOSTNAME.log &
#python /data26/home/nch/FAST_Miner/second_huntting_odd.py >> /data26/home/nch/FAST_Miner/Logfile/$HOSTNAME.log 
