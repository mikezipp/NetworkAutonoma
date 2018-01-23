
"""
Purpose
This Script allows multiple show commands to be run to multiple devices

Dependancies:
sudo python -m pip install netmiko <- TO INSTALL NETMIKO
#pip install netmiko tinydb pyperclip getpass <- TO INSTALL EVERYTHING ELSE

Author: Mike Zipp (themikezipp @ gmail)
"""
import time
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

#USER'S SELECTED TARGETS
target_device_list = []

#
target_list = []

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
#STEP 1.1 - User selects targets
##############################################################################

def CUSTOMSEARCH():
   global searchtype
   global target_list
   selected_zone = raw_input("\nFind Device By: (I) - IP, (H) - HOSTNAME, (D) - DEVICE TYPE\n>")
   if selected_zone == "I":
      searchtype = 'IP_Address'
      target = raw_input("\nEnter Partial or Complete IP Address\n>")
      TSVSEARCH(searchtype, target)
   if selected_zone == "H":
      searchtype = 'SysName'
      target = raw_input("\nEnter Partial or Complete HOSTNAME\n>")
      TSVSEARCH(searchtype, target)
   if selected_zone == "D":
      searchtype = 'device_type'
      selected_vendor = raw_input("\n(J) - All JUNIPER devices\n(C) - All CISCO devices\n>")
      if selected_vendor == "J":
         print "You Selected JUNIPER"
         target = "juniper"
         TSVSEARCH(searchtype, target)
      if selected_vendor == "C":
         print "You Selected CISCO"
         target = "cisco_ios"
         TSVSEARCH(searchtype, target)


##############################################################################
#STEP 2.1 - Python searches for targets
##############################################################################

#WHY AM I PASSING THIS FUNCTION A SEARCHTYPE?
def TSVSEARCH(searchtype, target):
   global outcome
   global pingstatus
   global target_list
   with open("company.csv", mode='r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
         if target in row[searchtype]:
            hostname = row['SysName']
            device_type = row['device_type']
            ipaddr = row['IP_Address']
            outcome = "%s | %s | %s" % (ipaddr, hostname, device_type)
            target_list.append(outcome)
   enumeratedictionary = dict(enumerate(target_list))
   for k, v in enumeratedictionary.iteritems():
      print k, "-", v
   selected_number = raw_input("\nInput one host # per line, end with an extra newline. (ALL) to add all hosts: ")
   if selected_number == "ALL":
      print "Added all hosts to target list"
      for k, v in enumeratedictionary.iteritems():
         hostnames_only = v.split(" ", 1)[0]
         target_device_list.append(hostnames_only)
   while selected_number is not "":
      for k, v in enumeratedictionary.iteritems():
         hostnames_only = v.split(" ", 1)[0]
         if selected_number == str(k):
            target_device_list.append(hostnames_only)
      selected_number = raw_input("Input one host # per line, end with an extra newline: ")
   print "\nHere are the targeted device(s): %s" % (target_device_list)

   print "Testing reachability to devices"
   time.sleep(2)
   for host in target_device_list:
      PINGCHECK(host)
      if pingstatus == "PASS":
         print "############################################\nPingstatus %s for %s\n############################################\n" % (pingstatus, host)
      if pingstatus == "FAIL":
         print "############################################\nPingstatus %s for %s, skipping\n############################################" % (pingstatus, host)
         target_device_list.remove(host)

   if len(target_device_list) == 0:
      print "no reachable hosts, exiting program"
      sys.exit()

   if len(target_device_list) >= 1:
      SELECT_SHOW_COMMANDS()
      save_output = raw_input("\nWould you like to save the output to file? (Y) (N)\n>")
      if save_output == "Y":
         print "Saving to file"
         COMMITCONFIRM_SAVE(searchtype)
      if save_output != "Y":
         print "Not saving to file"
         COMMITCONFIRM()


#############################
#STEP 3.1 - Python pingcheck
#############################
def PINGCHECK(host):
   global pingstatus
   print "Testing %s" % (host)
   response = os.system("ping -c 1 " + host)
   if response == 0:
      pingstatus = "PASS"
   else:
      pingstatus = "FAIL"
   return pingstatus


###############################################
#Step 4.1 - User selects which commands to send
###############################################
def SELECT_SHOW_COMMANDS():
   show_command = raw_input("Input one show command per line, end with an extra newline: ")
   while show_command is not "":
      if "show" in show_command:
         show_commands_list.append(show_command)
      else:
         print "%s is not a valid command, Enter SHOW commands only" % (show_command)
      show_command = raw_input("Input one show command per line, end with an extra newline: ")
   print show_commands_list


#######################################
#Step 5.1 - Confirm Selection & Execute
#######################################
def COMMITCONFIRM():
   print "\n\n####################\nSending User Commands \n%s \nTo \n%s\n####################\nTYPE YES TO CONTINUE, NO TO EXIT" % (show_commands_list, target_device_list)
   userconfirm = raw_input("\n>")
   if userconfirm == "YES":
      for host in target_device_list:
         print "Connecting to %s" % (host)
         print "Index:",target_device_list.index(host), "of", len(target_device_list)
         COMMITUSINGIP(host)
   elif userconfirm == "NO":
      print goodbye_screen
      sys.exit()


##############################################
#Step 5.2 = Confirm Selection & Execute + Save
##############################################
def COMMITCONFIRM_SAVE(selected_type):
   global destfilename
   savetofile = "YES"
   print "\n\n##########\nSending User Commands \n%s \nTo \n%s\n##########\nTYPE YES TO CONTINUE, NO TO EXIT" % (show_commands_list, target_device_list)
   userconfirm = raw_input("\n>")
   if userconfirm == "YES":
      for host in target_device_list:
         print "Connecting to %s" % (host)
         destfilename = raw_input("Enter custom filename or hit ENTER to save file as %s-%s.txt\n>" % (host, today))
         if destfilename == "":
            destfilename = "%s-%s.txt" % (host, today)
         TEE_USING_HOSTNAME(host)
   else:
      print goodbye_screen


############################################
#Step 6.1 - Execute commands IP ONLY
############################################
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


###########################################
#Step 6.2 - Execute commands + SAVE to file
###########################################
def TEE_USING_HOSTNAME(destination):
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
               TEE_TO_SPECIFIED_FILE(destination, x, user_command, device_type)
            print "\n>>>>>>>>> Closed connection to %s <<<<<<<<<" % (destination)
            net_connect.disconnect()


#####################################
#Step 7 - Save to file specifications
#####################################
#APPEND TEXT TO FILE
def TEE_TO_SPECIFIED_FILE(destination, command, output, device_type):
   global destfilename
   curpath = os.path.abspath(os.curdir)
   print "Your current directory path is: %s" % (curpath)
   if device_type == "cisco_ios":
      save_path = '/Users/mzipp/P12NetworkAutonoma/config_backups/cisco_ios/'
      completename = os.path.join(save_path, destfilename+".txt")
   if device_type == "juniper":
      save_path = '/Users/mzipp/P12NetworkAutonoma/config_backups/juniper/'
      completename = os.path.join(save_path, destfilename+".txt")
   print "Saving output to %s" % (completename)
   header = "##########START##########\nTARGET: %s\nCOMMAND: %s\nOUTPUT:\n%s" % (destination, command, output)
   print "Header is %s" % (header)
   writetofile = open(completename, "a")
   writetofile.write(header)
   writetofile.write("##########END##########")
   writetofile.write("\n")
   writetofile.close()


###########
#MAIN MENU#
###########
def main():
   print welcome_screen
   userselect = raw_input ("\nEnter the number corresponding to your selection below:\n\n1 - Send (one or many) SHOW commands to (one or many) destinations & (Optional) save to file\n2 - Exit program\n\n>")

   if userselect == "1":
      start_time = datetime.datetime.now()
      CUSTOMSEARCH()
      end_time = datetime.datetime.now()
      total_time = end_time - start_time
      print "\n\n Total time to complete script was %s" % (total_time)
      sys.exit()

   if userselect == "2":
      print goodbye_screen
      print "Exiting program. Goodbye"
      sys.exit()

   else:
      print "Invalid Selection"

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

#4 - jumphost zone on srx3400
#5 - 2fa



