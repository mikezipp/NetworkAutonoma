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

            # net_connect.send_config_set(username cisco priv 15 pass cisco)
            connect_return = net_connect.send_config_set(COMMANDLIST)

            print("\n\n>>>>>>>>> Device {0} {1} <<<<<<<<<".format(hostname, ipaddr))
            print(connect_return)
            print("\n>>>>>>>>> End <<<<<<<<<")
            net_connect.disconnect()


# Grab the Customer name to search
CUSTOMER = input('Customer name: ') + ".csv"
username, password, secret = credentials.cred_csv()

# Just for testing
#COMMANDSTRING = input('Command string to run: ')
COMMANDLIST = []
command = input("Input one command per line, end with an extra newline: ")
while command is not "":
    COMMANDLIST.append(command)
    command = input("Input one command per line, end with an extra newline: ")


# Run the primary function in this program
netcon(username, password, secret, CUSTOMER, COMMANDLIST)
ENDTIME = datetime.now()

# How long did it run?
TOTALTIME = ENDTIME - STARTTIME
print("\nTotal time for script: \n" + str(TOTALTIME))




"""
pip install netmiko tinydb pyperclip getpass

For database support (WIP):
pip install tinydb

For the email formatter (connectwise):
pip install pyperclip

For secure credential access (req'd soon):
pip install getpass

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
