# tech-challenge
## The Challenge
  
  Situation:
  
	This Nagios check plugin is a POC, checking the text file /tmp/hdd_status.
    The file /tmp/hdd_status should be existing on all servers, and should be
    kept up to date by a script executed hourly by cron.
  
  Goal:
  
    Please make the plugin Production ready to be rolled out on to all our servers.
  There are some typical problems with this type of monitoring that have to be
  addressed in the code.
  
  This implies:
  
    - Catch common problems before they happen in Production.
    - Proof read the existing lines of code.
    - Improve/rewrite the code where you think it is necessary.
      (You do not have to use Python, feel free to use the scripting language of your choice)
    - Add comments where useful, in order to explain:
	
        - Your reasoning.
        - Foreseeable risks with your approach.
        - Suggestions of how something should be done ideally.
		
hdd_status file contains:

+++++++++++++++++++++++++++++++++++++++++++++++++++

hdd1:OK hdd2:OK hdd3:WARNING hdd4:OK hdd5:CRITICAL

+++++++++++++++++++++++++++++++++++++++++++++++++++

Script "check_hdd_status.py" contains:


#!/usr/bin/python

import sys

with open( './hdd_status', 'r' ) as f:
    read_data = f.read()
f.close()

if 'WARNING' in read_data:
    print('WARNING: %s' %(read_data))
    sys.exit(1)
elif 'CRITICAL' in read_data:
    print('CRITICAL: %s' %(read_data))
    sys.exit(2)
elif 'OK' in read_data:
    print('OK: %s' %(read_data))
    sys.exit(0)


print('UNKNOWN - %s' %(read_data))
sys.exit(0)

## My Answer

After updating check_hdd_status.py to fix couple of issues, I developed Enhanced_master_hdd_status.py which works a central distribution system for the ease of deploying the hdd monitoring into any new servers, by simply adding the new servers in the Servers.list configuration file.
I more possible enhancement that can be implemented, is to use SSH keys between the monitoring server and the monitored nodes instead of providing the monitoring user name and password.
 
Challenge 1 Answer including:
 
1- Enhanced_master_hdd_status.py

2- check_hdd_status.py

3- Servers.list (Configuration file).

4- Master.log (Log file for all functions in Enhanced_master_hdd_status.py script).

5- Report.log (Log file contains a Consolidated report for output of check_hdd_status.py collected from all servers included in Servers.list configuration file).