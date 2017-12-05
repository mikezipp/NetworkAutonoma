"""
This module is a base for single-thread scripts.
based on https://github.com/admiralspark/NetSpark-Scripts
sudo python -m pip install netmiko <- TO INSTALL NETMIKO
"""

from datetime import datetime
import csv
from netmiko import ConnectHandler


# Begin timing the script
STARTTIME = datetime.now()
ENDTIME = datetime.now()
TOTALTIME = ENDTIME - STARTTIME

COMMANDLIST = []
TARGETDEVICES = []
hostname = []
device_type = []
ipaddr = []
username = []
password = []
secret = []
device = {}




# Iterates through a CSV, forms a dict, runs the command and logics it.


def userselect1():
   with open("company.csv", mode='r') as csvfile:
      reader = csv.DictReader(csvfile)
#      rows = [r for r in reader]
      count = 1

      for count, row in enumerate(reader):
         hostname = row['SysName']
         device_type = row['device_type']
         ipaddr = row['IP_Address']
         username = row['username']
         password = row['password']
         secret = row['secret']
         count = count + 1
         device = {
            'device_type': device_type,
            'ip': ipaddr,
            'username': username,
            'password': password,
            'secret': secret,
            'verbose': False,
      }
         print count, device

#ADD FUNCTION TO ALLOW USER TO APPLY CONFIG ONLY TO SPECIFIED DEVICE




def userselect2():
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

         COMMAND = raw_input ("enter command would you like to run\n>")
         print "You entered \n\n%s\n\nIf this looks correct, enter YES. enter NO to abort" % COMMAND
         COMMANDCONFIRM = raw_input ("\n>")
         if COMMANDCONFIRM == "YES":
            print "Sending config:\n\n%s\n\non %s with the following credentials:\nusername: %s\npassword: %s" % (COMMAND, ipaddr, username, password)
#           net_connect = ConnectHandler(**device)
#           showcommand = net_connect.send_command_expect("show system uptime")
#           print("\n\n>>>>>>>>> Device {0} <<<<<<<<<\n".format(row['SysName']))
#           configcommand = "do show system uptime "
#           exitcommand = "exit"
            break
         elif COMMANDCONFIRM == "NO":
            print "you selected NO. Exiting program"
            break

#         if iphost == "":
#            net_connect.config_mode()
#            net_connect.send_command_expect(showcommand)
#            print "Sent command %s to %s " % (showcommand, ipaddr)
#            net_connect.send_command_expect(configcommand)
#            print "Sent command %s to %s " % (configcommand, ipaddr)
#            print "Memory Saved."
#            print "\n>>>>>>>>> End <<<<<<<<<"
#            net_connect.disconnect()





def usermenu():
   userselect = raw_input ("\n\nWhat would you like to do?\n1 - Run a single command against a single host\n2 - Run a single command against a list of hosts\n4 - Exit program\n\n>")

   if userselect == "1":
      print "you selected run a single command against a single host"
      userselect1()

   if userselect == "2":
      print "you selected run a single command against a list of hosts"
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
