#!/bin/bash
DATABASE=lockbox
DATEF=$(date +'%m%d%Y')
DATENOW=$(date +'%d%b%Y')
LOGTIME=$(date +'%d%b%Y %T%z')
FILETIME=$(date +'%m%d%y')
LOG=/var/log/lockbox/$DATENOW-$DATABASE.log
i=0
RETRY_ATTEMPTS=5
timestamp (){
	LOGTIME=$(date +'%d%b%Y %T%z')
}
getFiles (){
			timestamp
			#send \"get /$DATEF*.zip /datadrive_01/lockbox/input/tmp/\r\"
			printf "[$LOGTIME] Start SFTP download from 'BANCFIRST'\n ----" >> $LOG
			/usr/bin/expect -c "
			spawn sshpass -f "/usr/local/sbin/assets/bancfirst.txt" sftp MidwestHose@as2.bancfirst.com
			expect \"sftp>\" 
		    
			send \"get /$DATEF*.zip /datadrive_01/lockbox/input/tmp/\r\"
			expect \"sftp>\"
			send \"ls\r\"
			expect \"sftp>\"
			send \"exit\r\"" >> $LOG

			timestamp
			printf "[$LOGTIME] END SFTP download from 'BANCFIRST'\n ----" >> $LOG
			sleep 5

}

if ! ls "/datadrive_01/lockbox/output/old/$FILETIME"*;
then
	getFiles
	sleep 10
else
	echo "[$LOGTIME] Today's Lockbox processed..."
fi

while [ $i -le $RETRY_ATTEMPTS ] 
do
	if ls "/datadrive_01/lockbox/input/tmp/$DATEF"*.zip 1> /dev/null 2>&1;
	#if ls "/datadrive_01/lockbox/input/tmp/Midwest.zip" 1> /dev/null 2>&1;
	then
		#bash /usr/local/sbin/WatchLockbox.sh
		unzip -j -o "/datadrive_01/lockbox/input/tmp/$DATEF*.zip" -d "/datadrive_01/lockbox/input/" 
		sleep 10s
		bash /usr/local/sbin/WatchLockbox.sh
		#unzip -j -o "/datadrive_01/lockbox/input/tmp/Midwest.zip" -d "/datadrive_01/lockbox/input/" | bash /usr/local/sbin/WatchLockbox.sh
		timestamp
		echo "[$LOGTIME] Starting Lockbox Processing..." >> $LOG
		
		i=5
	elif [[ $i -eq RETRY_ATTEMPTS ]]; then
		echo "Max Attempts ($i)" >> $LOG
		exit 1
	else
		echo "Reattempting (attempt $i)" >> $LOG
		i=$((i+1))
		sleep 5
		if ! ls "/datadrive_01/lockbox/output/old/$FILETIME"*;
		then
			getFiles
		else
			echo "[$LOGTIME] Today's Lockbox processed..."
		fi

		#getFiles
	fi

done

# elif [ $i -eq 5 ]
# 	then
# 		


				