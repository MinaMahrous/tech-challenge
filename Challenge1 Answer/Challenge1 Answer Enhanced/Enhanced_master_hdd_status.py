#!/usr/bin/python

import paramiko
import datetime


def timestamp():
    t = datetime.datetime.now()
    s = t.strftime('%m-%d-%Y %H:%M:%S')
    return s


def LOG(message):
    localtime = timestamp()
    f1.write(localtime +" - "+ message + "\n")


def conf_read(ConfFilePath):
    LOG("INFO - Configuration file read - Started")
    try:
        with open (ConfFilePath, 'r') as f:
            ServerSplittedList = f.read().splitlines()
        f.close()
        return ServerSplittedList
        LOG("INFO - Configuration file read - Finished")
    except:
        LOG("ERROR: Configuration file read - Failed - Please check that file (Servers.list) exists and accessible with read permission")

#This function to transfer the check_hdd_status.py script to the remote server in case it is not there already.
#The script will be transfered under monuser (Monitoring User) home directory.
def transfer_script(host, uname, passwd):
    try:
        LOG("INFO - transfer_script() - Started")
        transport = paramiko.Transport((host, 22))
        transport.connect(username=uname, password=passwd)
        sftp = paramiko.SFTPClient.from_transport(transport)
        LOG("INFO - SFTP session opened with remote server" + host + " successfully to transfer the script")
        sftp.put("/home/mtalaat/check_hdd_status.py", "./check_hdd_status.py")
        LOG("INFO - Script transfer completed successfully")
        sftp.close()
        transport.close()
        LOG("INFO - SFTP session closed successfully on server " + host + " after transferring the script")
    except:
        LOG("ERROR - transfer_script() - Failed")


#This function to check if the check_hdd_status.py script already exist on the remote server under monuser (Monitoring user) home directory.
def script_exist(host,uname,passwd):
    try:
        LOG("INFO - script_exist() - Started")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host,username=uname,password=passwd)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls ./check_hdd_status.py')
        return ssh_stdout.read()
        LOG("INFO - script_exist() - Finished")
    except:
        LOG("ERROR - script_exist() - Failed")


#This function to run check_hdd_status.py script on the remote server and append the error message (if any) in Error.log file and append the the status of HDD in consalidated Report.log
def run_script(host, uname, passwd):
    try:
        LOG("INFO - run_script() - Started")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=uname, password=passwd)
        LOG("INFO - Connection to server: " + host + " established successfully")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('python ./check_hdd_status.py')
        LOG("INFO - check_hdd_status.py script is running on server: " + host)
        localtime = timestamp()
        error = ssh_stderr.read()
        if error:
            LOG("ERROR - Error occurred during running script on server: " + host + " Please check Error.log")
            err = open("Error.log", "a")
            err.write('\n' + localtime + '\nOutput from Server: %s \n%s' %(host,error))
            err.close()
        text = ssh_stdout.read()
        out = open("Report.log", "a")
        out.write ('\n' + localtime + '\nOutput from Server: %s \n%s' %(host,text))
        out.close()
        LOG("INFO - Script completed successfully on server: " + host + " and Report.log updated successfully")
    except:
        LOG("ERROR - run_script() - Failed")

def main():

    ServerList = conf_read("./Servers.list")
    for line in ServerList:
        hname = line.split(":")[0].strip()
        uname = line.split(":")[1].strip()
        upass = line.split(":")[2].strip()
        LOG("INFO - Processing  on server: " + hname + "....")
        #Check if monitoring script exist on remote server
        file_exist = script_exist(hname, uname, upass)
        LOG("INFO - Checking if script exists on server: " + hname + "...")
        #If monitoring script exist on remote server then run it else, transfer it first then run it.
        if file_exist:
            LOG("INFO - Script found on server: " + hname + "...")
            run_script(hname, uname, upass)
        else:
            LOG("INFO - Script NOT found on server: " + hname + "...")
            transfer_script(hname, uname, upass)
            run_script(hname, uname, upass)


f1 = open('./Master.log', 'a')
main()
f1.close()