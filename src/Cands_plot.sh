#!/bin/bash


Codes_dir=/data26/home/nch/FAST_Miner/

file_dir=/data26/zhuww/psr_19beam_1bit/


Coin_dir=$Codes_dir/Coin_Result/
Gold_dir=$Codes_dir/Gold_Mine/


project=$1
Serverlist=$2

#echo =====================
#echo Thanks Chenhui Niu~
#echo The FRB Hunter~
#echo =====================
#sleep 1
#echo "Let's Go~"
#sleep 2

date_pic='10'
All_plot=1
 
for date_obs in $Gold_dir/$project/*/
do 
	if [ -d $date_obs ]
	then
		date_obs=`echo $date_obs | awk -F $project/ {'print $2'}`
            if [[ $date_obs =~ $date_pic ]] || [[ $All_plot == 1 ]]
		then  
		rm -f $Gold_dir/$project/$date_obs/*.txt
		for gold_can in $Gold_dir/$project/$date_obs/*.gold
	
		do 
	       		if [ -s $gold_can ]
		  	then

		           	#echo ========START============
				#echo Golden Cands: $gold_can
				f_stamp=`echo ${gold_can##*/} | awk -F . {'print $1'}`
		        	file_dir=$Coin_dir/$project/$date_obs
				#echo $file_dir
				#echo $f_stamp 
		        	if [ -d $file_dir ]

		           	then
		           	fil_line=`ls $file_dir -l | grep  -n $f_stamp | awk -F : {'print $1'}`
		           	fil_line=$(($fil_line -1)) # Be caution of first line of 'ls' cmd, 'Total xxx'
			#	echo $fil_line th Fiterbank File of Date: $date_obs
				python /data26/home/nch/FAST_Miner/src/bursts_plot.py $project $date_obs $fil_line $gold_can $Serverlist
			#	echo ---------END-------------
#				echo
				fi
		        fi
		done
	    fi
       fi
done
