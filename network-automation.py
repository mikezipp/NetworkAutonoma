
"""
This module is a base for single-thread scripts.
based on https://github.com/admiralspark/NetSpark-Scripts
sudo python -m pip install netmiko <- TO INSTALL NETMIKO
"""

from datetime import datetime
import csv
from netmiko import ConnectHandler



TARGETDEVICES = []
hostname = []
device_type = []
ipaddr = []
username = []
password = []
secret = []
device = {}


COMMANDLIST = []

#INITIALIZE LISTS#
ipaddr_list = []
device_type_list = []
def initlists():
   with open("company.csv", mode='r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
         ipaddr = row['IP_Address']
         ipaddr_list.append(ipaddr)
         device_type = row['device_type']
         if device_type not in device_type_list:
            device_type_list.append(device_type)
initlists()


#ADD COMMANDS#
def commandlist():
   command = raw_input("Input one command per line, end with an extra newline: ")
   while command is not "":
      COMMANDLIST.append(command)
      command = raw_input("Input one command per line, end with an extra newline: ")
   print COMMANDLIST


#APPLY CONFIG TO A SINGLE DEVICE#
def userselect1():
   with open("company.csv", mode='r') as csvfile:
      reader = csv.DictReader(csvfile)
#      count = 0
      for x in ipaddr_list:
         print "%s" % (x)
      SELECT_DEVICE = raw_input("enter ip of device you would like to configure\n>")
      commandlist()
      for row in reader:
         if SELECT_DEVICE == row['IP_Address']:
            print "Found device %s. Gathering details..." % (SELECT_DEVICE)
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
            COMMIT_CONFIRM = raw_input("\n\n###\nHOSTNAME: %s\nCOMMAND(S):%s\n###\nType YES to confirm, NO to abort\n>>>" % (hostname, COMMANDLIST))
            if COMMIT_CONFIRM == "YES":
               print "\nsending configuration to hostname: %s" % hostname
               start_time = datetime.now()
               net_connect = ConnectHandler(**device)

               #BASELINE TEST
               base_commands = net_connect.send_command('show ver')
               print base_commands

               #ENTER ENABLE MODE
               net_connect.enable()

               #EXECUTE CHANGES (IN CONFIG MODE)
               config_commands = net_connect.send_config_set(COMMANDLIST)
               print config_commands
               print "\n>>>>>>>>> End <<<<<<<<<"
               net_connect.disconnect()
               end_time = datetime.now()
               total_time = end_time - start_time
               print "Time elapsed: %s" % str(total_time)

            if COMMIT_CONFIRM == "NO":
               print "\naborting configuration"
            else:
               print "\nInvalid Selection, exiting program"






#APPLY CONFIG TO A GROUP OF DEVICES # IN PROGRESS#
def userselect2():
   with open("company.csv", mode='r') as csvfile:
      reader = csv.DictReader(csvfile)
      for x in device_type_list:
         print "%s" % (x)
      SELECT_DEVICE_TYPE = raw_input("enter type of device you would like to configure\n>")
      commandlist()

      for row in reader:
         if SELECT_DEVICE_TYPE == row['device_type']:
            print "Found device %s. Gathering details..." % (SELECT_DEVICE_TYPE)

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

            COMMIT_CONFIRM = raw_input("\n\n###\nHOSTNAME: %s\nCOMMAND(S):%s\n###\nType YES to confirm, NO to abort\n>>>" % (hostname, COMMANDLIST))
            if COMMIT_CONFIRM == "YES":
               print "\nsending configuration to hostname: %s" % hostname
               start_time = datetime.now()
               net_connect = ConnectHandler(**device)
               
               #BASELINE TEST
               base_commands = net_connect.send_command('show ver')
               print base_commands

               #ENTER ENABLE MODE
               net_connect.enable()

               #EXECUTE CHANGES (IN CONFIG MODE)
               config_commands = net_connect.send_config_set(COMMANDLIST)
               print config_commands
               print "\n>>>>>>>>> End <<<<<<<<<"
               net_connect.disconnect()
               end_time = datetime.now()
               total_time = end_time - start_time
               print "Time elapsed: %s" % str(total_time)

            if COMMIT_CONFIRM == "NO":
               print "\naborting configuration"
            else:
               print "\nInvalid Selection, exiting program"






#USER SELECTION MENU#
def usermenu():
   userselect = raw_input ("\n\nWhat would you like to do?\n1 - Run command(s) to a single host\n2 - Run command(s) to a type of hosts\n4 - Exit program\n\n>")

   if userselect == "1":
      print "Running command(s) against a single host"
      userselect1()

   if userselect == "2":
      print "Running command(s) against a type of hosts"
      userselect2()

   if userselect == "4":
      print "exiting program"

usermenu()








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
