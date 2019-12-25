#!/bin/bash
#Serverlist=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
#Serverlist=[3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21]
#Serverlist=[7,9,10,13,14,15,17,18,19,20,21]
Serverlist=[6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
#Serverlist=[6,8,11,12,16]

echo We Gonna use X-serise GPU Server: $Serverlist

echo =====================
echo Thanks Chenhui Niu~
echo The FRB Hunter~
echo =====================
sleep 1
echo "Let's Go~"


pdsh -l nch -w x$Serverlist "source /data26/home/nch/.bashrc sh ; /data26/home/nch/FAST_Miner/src/Cands_plot.sh '201810/' $Serverlist" 


#pdsh -l nch -w x$Serverlist "source /data26/home/nch/.bashrc sh ; /data26/home/nch/FAST_Miner/Cands_plot.sh '201901/' $Serverlist" &
#pdsh -l nch -w x$Serverlist "source /data26/home/nch/.bashrc sh ; /data26/home/nch/FAST_Miner/Cands_plot.sh '201903/' $Serverlist" &
#pdsh -l nch -w x$Serverlist "source /data26/home/nch/.bashrc sh ; /data26/home/nch/FAST_Miner/Cands_plot.sh '201904/' $Serverlist" &
#pdsh -l nch -w x$Serverlist "source /data26/home/nch/.bashrc sh ; /data26/home/nch/FAST_Miner/Cands_plot.sh '201905/' $Serverlist" &
#pdsh -l nch -w x$Serverlist "source /data26/home/nch/.bashrc sh ; /data26/home/nch/FAST_Miner/Cands_plot.sh '201906/' $Serverlist" &
#pdsh -l nch -w x$Serverlist "source /data26/home/nch/.bashrc sh ; /data26/home/nch/FAST_Miner/Cands_plot.sh '201907/' $Serverlist" &
#pdsh -l nch -w x$Serverlist "source /data26/home/nch/.bashrc sh ; /data26/home/nch/FAST_Miner/Cands_plot.sh '201908/' $Serverlist" &
#pdsh -l nch -w x$Serverlist "source /data26/home/nch/.bashrc sh ; /data26/home/nch/FAST_Miner/Cands_plot.sh '201909/' $Serverlist" &
#pdsh -l nch -w x$Serverlist "source /data26/home/nch/.bashrc sh ; /data26/home/nch/FAST_Miner/Cands_plot.sh '201811/' $Serverlist" &
#pdsh -l nch -w x$Serverlist "source /data26/home/nch/.bashrc sh ; /data26/home/nch/FAST_Miner/Cands_plot.sh '201812/' $Serverlist" 
#pdsh -w x$Serverlist "sh /data26/home/nch/FAST_Miner/Cands_plot.sh '201901/' $Serverlist" 
