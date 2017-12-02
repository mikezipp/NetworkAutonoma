'''
This module is a base for single-thread scripts.
based on https://github.com/admiralspark/NetSpark-Scripts
sudo python -m pip install netmiko <- TO INSTALL NETMIKO
'''

from datetime import datetime
import csv
from netmiko import ConnectHandler


# Begin timing the script
STARTTIME = datetime.now()
ENDTIME = datetime.now()
TOTALTIME = ENDTIME - STARTTIME

COMMANDLIST = []
TARGETDEVICES = []

# Iterates through a CSV, forms a dict, runs the command and logics it.

def initlists():
    with open("company.csv", mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            hostname = row['SysName']
            device_type = row['device_type']
            ipaddr = row['IP_Address']
            username = row['username']
            password = row['password']
            secret = row['secret']
            device = {
                'device_type': device_type,
                'ip': ipaddr,
                'username': username,
                'password': password,
                'secret': secret,
                'verbose': False,
            }


def main():
   initlists()
   COMMANDSTRING = raw_input("\nEnter command to run: \n> ")
   if COMMANDSTRING != "":
      COMMANDLIST.append(COMMANDSTRING)
      print "you entered %s" % COMMANDLIST
      COMMANDTARGET = raw_input("\nEnter target device ip: \n> ")
      TARGETDEVICES.append(COMMANDTARGET)
      print "you selected %s" % TARGETDEVICES
      for device in TARGETDEVICES:
         if device in ipaddr:
            print "found device, starting command push on %s" % device
#           netcon(username, password, COMPANY, COMMANDLIST
            break
         else:
            print "could not find device %s" % device
            break

main()











##################EXTRAS

#            net_connect = ConnectHandler(device)
#            net_connect.enable()
#            net_connect.send_config_set(COMMANDLIST)
#            connect_return = net_connect.send_config_set(COMMANDLIST)
#
#            print("\n\n>>>>>>>>> Device {0} {1} <<<<<<<<<".format(hostname, ipaddr))
#            print(connect_return)
#            print("\n>>>>>>>>> End <<<<<<<<<")
#            net_connect.disconnect()



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
