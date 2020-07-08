#!/usr/bin/python
#This script simply checks that the "/tmp/hdd_status" file updated during the last hour since the cron job runs hourly and overwrite this script.
#Then the script reads the "/tmp/hdd_status" file and simply prints the status of each HDD, print action can be replaced with anything as per the requirement, can send mail, submit ticket, or whatever.

#import sys

import os
import time

file_mod_time = os.stat("/tmp/hdd_status").st_mtime
last_time = (time.time() - file_mod_time) / 60
if last_time > 60:
    print ("hdd_status file was not updated for the last 60 mins please check the cron job updating the hdd_status file [Login to the destination server and run "crontab -l" command)
else:
    with open( "/tmp/hdd_status", 'r' ) as f:
        read_data = f.read()
        f.close()

for word in read_data.split():
    if 'CRITICAL' in word:
        print('CRITICAL: %s' %(word))
    elif 'WARNING' in word:
        print('WARNING: %s' %(word))
    elif 'OK' in word:
        print('OK: %s' %(word))
    else:
        print('UNKNOWN: %s' %(word))