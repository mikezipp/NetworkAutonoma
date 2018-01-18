
"""
Purpose
This Script allows multiple show commands to be run to multiple devices

Dependancies:
sudo python -m pip install netmiko <- TO INSTALL NETMIKO
#pip install netmiko tinydb pyperclip getpass <- TO INSTALL EVERYTHING ELSE

Author: Mike Zipp (themikezipp @ gmail)
"""

import datetime
import csv
import sys, traceback
import os.path
import os
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException



######################
#DICTIONARIES & LISTS#
######################
   #RAW LISTS OF ALL IP/HOSTNAMES
device_ipaddr_list = []
device_hostname_list = []

device_vendor_list_juniper = []
device_vendor_list_cisco = []

   #CLEANED UP LIST (DUPS and # REMOVED)
target_dest_list = []

   #USER'S SELECTED TARGETS
target_device_list = []

   #USER'S SELECTED SHOW COMMANDS
show_commands_list = []

   #USER SELECTION DICTIONARY
enumeratedictionary = {}

   #TIME FUNCTION
today = datetime.date.today()

##################################
######## MAIN FUNCTIONS ##########
##################################

welcome_screen = """\


\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//
                     __________________________  
            (__)    /                          |
            (oo)   / Welcome to NetAutonoma-v1 |
     /-------\/  --\ Service Owner: Mike Zipp  |
    / |     ||      \__________________________|
   *  ||----||                 
      ~~    ~~    
\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\// 
"""

goodbye_screen = """\
\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//
                     ____________________
            (__)    /                   |
            (oo)   / Exiting program    |
     /-------\/  --\      Goodbye!      |
    / |     ||      \___________________|
   *  ||----||
      ~~    ~~
\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//
"""


##############################################################################
#STEP1 - User choses to search by hostname or IP address
##############################################################################
def USER_SELECT_DESTINATION_TYPE():
   selected_type = "none"
   selected_letter = raw_input("\nEnter letter corresponding to your selection below\n\n(I) - Target device(s) by IP\n(H) - Target device(s) by HOSTNAME\n(V) - Target device(s) by VENDOR(NEW!)\n>")
   if selected_letter == "I":
      selected_type = "IP"
      print "You have selected %s - %s" % (selected_type, "Search by IP")
      return selected_type
   if selected_letter == "H":
      selected_type = "HOSTNAME"
      print "You have selected %s - %s" % (selected_type, "Search by Hostname")
      return selected_type
   if selected_letter == "V":
      selected_vendor = raw_input("\n(J) - All JUNIPER devices\n(C) - All CISCO devices\n>")
      if selected_vendor == "J":
         print "You Selected JUNIPER"
         selected_type = "VENDOR-JUNIPER"
         return selected_type
      if selected_vendor == "C":
         print "You Selected CISCO"
         selected_type = "VENDOR-CISCO"
         return selected_type




##############################################################################
#STEP2 - Python cleans up available selections and executes enumerate function
##############################################################################
def CLEAN_SELECTION(selected_type):
   with open("company.csv", mode='r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
         hostname = row['SysName']
         ipaddr = row['IP_Address']
         device_type = row['device_type']
         if selected_type == "IP":
            if ipaddr != "None" and ipaddr not in device_ipaddr_list:
               device_ipaddr_list.append(ipaddr)
         if selected_type == "HOSTNAME":
            if hostname != "None" and hostname not in device_hostname_list: 
               device_hostname_list.append(hostname)
         if selected_type == "VENDOR-JUNIPER":
            if device_type == "juniper" and hostname not in device_vendor_list_juniper:
               device_vendor_list_juniper.append(hostname)
         if selected_type == "VENDOR-CISCO":
            if device_type == "cisco_ios" and hostname not in device_vendor_list_cisco:
               device_vendor_list_cisco.append(hostname)
   #Need to loop multiple times to remove all # entries
   if selected_type == "IP":
      for host in device_ipaddr_list:
         if "#" in host[0]:
            device_ipaddr_list.remove(host)
      for host in device_ipaddr_list:
         if "#" in host[0]:
            device_ipaddr_list.remove(host)
      for host in device_ipaddr_list:
         if "#" in host[0]:
            device_ipaddr_list.remove(host)
      for host in device_ipaddr_list:
         if "#" in host[0]:
            device_ipaddr_list.remove(host)
      for host in device_ipaddr_list:
         if host not in target_dest_list:
            target_dest_list.append(host)
   if selected_type == "HOSTNAME":
      for host in device_hostname_list:
         if host not in target_dest_list:
            target_dest_list.append(host)
   if selected_type == "VENDOR-CISCO":
      for host in device_vendor_list_cisco:
         if host not in target_dest_list:
            target_dest_list.append(host)
   if selected_type == "VENDOR-JUNIPER":
      for host in device_vendor_list_juniper:
         if host not in target_dest_list:
            target_dest_list.append(host)
   return target_dest_list


##############################################################################
#Step 3 - Python Enumerates list, allows user to add target devices to list
##############################################################################
def ENUMERATELISTS(target_dest_list):
   enumeratedictionary = dict(enumerate(target_dest_list))
   for k, v in enumeratedictionary.iteritems():
      print k, "-", v
   selected_number = raw_input("Input one host # per line, end with an extra newline. ALL to add all hosts: ")
   if selected_number == "ALL":
      for k, v in enumeratedictionary.iteritems():
         target_device_list.append(v)
   while selected_number is not "":
      for k, v in enumeratedictionary.iteritems():
         if selected_number == str(k):
            target_device_list.append(v)
      selected_number = raw_input("Input one host # per line, end with an extra newline: ")
   print "Here are the targeted device(s): %s" % (target_device_list)


##############################################################################
#Step 4 - User selects which commands to send
##############################################################################
def SELECT_SHOW_COMMANDS():
   show_command = raw_input("Input one show command per line, end with an extra newline: ")
   while show_command is not "":
      if "show" in show_command:
         show_commands_list.append(show_command)
      else:
         print "%s is not a valid command, Enter SHOW commands only" % (show_command)
      show_command = raw_input("Input one show command per line, end with an extra newline: ")
   print show_commands_list


##############################################################################
#Step 5 - Confirm Selection & Execute
##############################################################################
def COMMITCONFIRM(selected_type):
   print "\n\n##########\nSending User Commands \n%s \nTo \n%s\n##########\nTYPE YES TO CONTINUE, NO TO EXIT" % (show_commands_list, target_device_list)
   userconfirm = raw_input("\n>")
   if userconfirm == "YES":
      if selected_type == "IP":
         for host in target_device_list:
            print "Connecting to %s" % (host)
            print "Index:",target_device_list.index(host), "of", len(target_device_list)
            COMMITUSINGIP(host)
      if selected_type == "HOSTNAME":
         for host in target_device_list:
            print "Connecting to %s" % (host)
            print "Index:",target_device_list.index(host), "of", len(target_device_list)
            COMMITUSINGHOSTNAME(host)
      if selected_type == "VENDOR-JUNIPER":
         for host in target_device_list:
            print "Connecting to %s" % (host)
            print "Index:",target_device_list.index(host), "of", len(target_device_list)
            COMMITUSINGHOSTNAME(host)
      if selected_type == "VENDOR-CISCO":
         for host in target_device_list:
            print "Connecting to %s" % (host)
            COMMITUSINGHOSTNAME(host)
   elif userconfirm == "NO":
      print goodbye_screen
      sys.exit()


#############################################################
#Step 5 V2 = Confirm Selection & Execute + Allow save to file
#############################################################
def COMMITCONFIRM_SAVE(selected_type):
   global destfilename
   savetofile = "YES"
   print "\n\n##########\nSending User Commands \n%s \nTo \n%s\n##########\nTYPE YES TO CONTINUE, NO TO EXIT" % (show_commands_list, target_device_list)
   userconfirm = raw_input("\n>")
   if userconfirm == "YES":
      if selected_type == "IP":
         print "This feature is not supported yet, Please use Hostname to enable this feature"

      if selected_type == "HOSTNAME":
         for host in target_device_list:
            print "Connecting to %s" % (host)
            destfilename = raw_input("Enter custom filename or hit ENTER to save file as %s-%s.txt\n>" % (host, today))
            if destfilename == "":
               destfilename = "%s-%s.txt" % (host, today)
            TEE_USING_HOSTNAME(host)

      if selected_type == "VENDOR-JUNIPER":
         for host in target_device_list:
            print "Connecting to %s" % (host)
            destfilename = raw_input("Enter custom filename or hit ENTER to save file as %s-%s.txt\n>" % (host, today))
            if destfilename == "":
               destfilename = "%s-%s.txt" % (host, today)
            TEE_USING_HOSTNAME(host)

      if selected_type == "VENDOR-CISCO":
         for host in target_device_list:
            print "Connecting to %s" % (host)
            destfilename = raw_input("Enter custom filename or hit ENTER to save file as %s-%s.txt\n>" % (host, today))
            if destfilename == "":
               destfilename = "%s-%s.txt" % (host, today)
            TEE_USING_HOSTNAME(host)
   else:
      print goodbye_screen


#######################################
#Step 6 V1 - Execute commands (IP ONLY)
#######################################
def COMMITUSINGIP(destination):
   with open("company.csv", mode='r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
         if row['IP_Address'] in destination:
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
            try:
               net_connect = ConnectHandler(**device)
            except NetMikoTimeoutException:
               Msg = 'SSH connection failed'
               print 'SSH connection failed for %s' % (destination)
            except NetMikoAuthenticationException:
               Msg = 'SSH authentication failed'
               print 'SSH authentication failed for %s' % (destination)

            for x in show_commands_list:
               print "sending command %s to %s" % (x, destination)
               user_command = net_connect.send_command(x)
               print user_command
            print "\n>>>>>>>>> Closed connection to %s <<<<<<<<<" % (destination)
            net_connect.disconnect()


############################################
#Step 6 V2 - Execute commands HOSTNAMES ONLY
############################################
def COMMITUSINGHOSTNAME(destination):
   with open("company.csv", mode='r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
         if row['SysName'] in destination:
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
            try:
               net_connect = ConnectHandler(**device)
            except NetMikoTimeoutException:
               Msg = 'SSH connection failed'
               print 'SSH connection failed for %s' % (destination)
            except NetMikoAuthenticationException:
               Msg = 'SSH authentication failed'
               print 'SSH authentication failed for %s' % (destination)

            for x in show_commands_list:
               print "sending command %s to %s" % (x, destination)
               user_command = net_connect.send_command(x)
               print user_command
            print "\n>>>>>>>>> Closed connection to %s <<<<<<<<<" % (destination)
            net_connect.disconnect()


#################################################################
#Step 6 v3 - Execute commands HOSTNAMES ONLY + Allow save to file
#################################################################

def TEE_USING_HOSTNAME(destination):
   with open("company.csv", mode='r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
         if row['SysName'] in destination:
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
            try:
               net_connect = ConnectHandler(**device)
            except NetMikoTimeoutException:
               Msg = 'SSH connection failed'
               print 'SSH connection failed for %s' % (destination)
            except NetMikoAuthenticationException:
               Msg = 'SSH authentication failed'
               print 'SSH authentication failed for %s' % (destination)
            for x in show_commands_list:
               print "sending command %s to %s" % (x, destination)
               user_command = net_connect.send_command(x)
               TEE_TO_SPECIFIED_FILE(destination, x, user_command, device_type)
            print "\n>>>>>>>>> Closed connection to %s <<<<<<<<<" % (destination)
            net_connect.disconnect()




######################################
######MAIN FUNCTIONS#####

def MULTI_SHOW_MULTI_DEST():
   start_time = datetime.datetime.now()
   selected_type = USER_SELECT_DESTINATION_TYPE()
   CLEAN_SELECTION(selected_type)
   ENUMERATELISTS(target_dest_list)
   SELECT_SHOW_COMMANDS()
   COMMITCONFIRM(selected_type)
   end_time = datetime.datetime.now()
   total_time = end_time - start_time
   print "\n\n Total time to complete script was %s" % (total_time)


def MULTI_SAVE_MULTI_DEST():
   start_time = datetime.datetime.now()
   print "PLEASE NOTE IP IS NOT SUPPORTED WITH MULTI SAVE MODE"
   selected_type = USER_SELECT_DESTINATION_TYPE()
   CLEAN_SELECTION(selected_type)
   ENUMERATELISTS(target_dest_list)
   SELECT_SHOW_COMMANDS()
   COMMITCONFIRM_SAVE(selected_type)
   end_time = datetime.datetime.now()
   total_time = end_time - start_time
   print "\n\n Total time to complete script was %s" % (total_time)


#APPEND TEXT TO FILE
def TEE_TO_SPECIFIED_FILE(destination, command, output, device_type):
   global destfilename
   curpath = os.path.abspath(os.curdir)
   print "Your current directory path is: %s" % (curpath)
   if device_type == "cisco_ios":
      save_path = '/Users/USERNAME/NetworkAutonoma/config_backups/cisco_ios/'
      completename = os.path.join(save_path, destfilename+".txt")
   if device_type == "juniper":
      save_path = '/Users/USERNAME/NetworkAutonoma/config_backups/juniper/'
      completename = os.path.join(save_path, destfilename+".txt")
   print "Saving output to %s" % (completename)
   header = "##########START##########\nTARGET: %s\nCOMMAND: %s\nOUTPUT:\n%s" % (destination, command, output)
   print "Header is %s" % (header)
   writetofile = open(completename, "a")
   writetofile.write(header)
   writetofile.write("##########END##########")
   writetofile.write("\n")
   writetofile.close()




#####MAIN MENU#####

def main():
   print welcome_screen
   userselect = raw_input ("\nEnter the number corresponding to your selection below:\n\n1 - Send (one or many) SHOW commands to (one or many) destinations\n2 - Send (one or many) SHOW commands to (one or many) destinations & SAVE to file\n3 - Exit program\n\n>")

   if userselect == "1":
      MULTI_SHOW_MULTI_DEST()

   if userselect == "2":
      MULTI_SAVE_MULTI_DEST()

   if userselect == "3":
      print goodbye_screen
      print "Exiting program. Goodbye"
      sys.exit()

main()










##########################################
##########MISC STUFF TO ADD###############
##########################################

#1 - Configuration module (Send non-show commands)
#   ENTER ENABLE MODE
#               net_connect.enable()
#               #EXECUTE CHANGES (IN CONFIG MODE)
#   ENTER CONFIG MODE
#               config_commands = net_connect.send_config_set(COMMANDLIST)
#               print config_commands



#2 - run commands by device purpose?
#BDN
#CORP
#CMC
#I2
#I2-PRIME
#OTHER

#3 - add host ping checker?
#4 - jumphost zone on srx3400
#5 - 2fa



