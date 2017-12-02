'''
This module is a base for single-thread scripts.
based on https://github.com/admiralspark/NetSpark-Scripts
'''

from datetime import datetime
import csv
from netmiko import ConnectHandler
import credentials


# Begin timing the script
STARTTIME = datetime.now()



# Iterates through a CSV, forms a dict, runs the command and logics it.

def netcon(username, password, secret, CUSTOMER, COMMANDLIST):
    with open(CUSTOMER, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            hostname = row['SysName']
            device_type = row['device_type']
            ipaddr = row['IP_Address']
            switch = {
                'device_type': device_type,
                'ip': ipaddr,
                'username': username,
                'password': password,
                'secret': secret,
                'verbose': False,
            }

            net_connect = ConnectHandler(**switch)
            net_connect.enable()
            net_connect.send_config_set(COMMANDLIST)
            connect_return = net_connect.send_config_set(COMMANDLIST)

            print("\n\n>>>>>>>>> Device {0} {1} <<<<<<<<<".format(hostname, ipaddr))
            print(connect_return)
            print("\n>>>>>>>>> End <<<<<<<<<")
            net_connect.disconnect()


COMMANDLIST = []

def main():
   COMMANDSTRING = input('Enter command to run: ')
   while COMMANDSTRING is not "":
      COMMANDLIST.append(command)
      print "you entered %s" % COMMANDLIST
      COMMANDTARGET = input('Enter target device ip : ')
      print "you selected %s" % COMMANDTARGET
      with open(CUSTOMER, mode='r') as csvfile:
         reader = csv.DictReader(csvfile)
         if COMMANDTARGET in reader:
            print "found device, applying config"
            netcon(username, password, secret, CUSTOMER, COMMANDLIST)
            ENDTIME = datetime.now()
            print("\nTotal time for script: \n" + str(TOTALTIME))



TOTALTIME = ENDTIME - STARTTIME




"""
pip install netmiko tinydb pyperclip getpass

"""





"""
MZ TEST

def show_version():
   net_connect = ConnectHandler(**router)
   output = net_connect.send_command('show version')
   output = output.split('\n')
   print output

show_version()

"""
