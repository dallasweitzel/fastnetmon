#!/usr/bin/python
import sys
import re
import time
import logging
import json
import pprint
import subprocess

def ssh(ip,username,password,port,thecmd,conntimeout,cmdtimeout):
  import paramiko
  import time
  theoutput = []
  # lets remove any new lines
  ip = ip.rstrip("\n\r")
  theoutput = []
  try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #print('connecting to %s' % ip + 'end')
    ssh.connect(hostname=str(ip), port=str(port), username=str(username), password=str(password), look_for_keys=False, allow_agent=False, timeout=float(conntimeout))
    #print('Successfully connected to %s' % ip)
    remote_conn = ssh.invoke_shell()
    time.sleep(0.001)
    stdin,stdout,stderr = ssh.exec_command(thecmd, timeout=float(cmdtimeout))
    theoutput = stdout.readlines()
    ssh.close()
    if ssh:
      ssh.close()
  except Exception as e:
    if ssh:
      ssh.close()
      #print("closed ssh conn"+str(e))
    pass
  return theoutput

def rochssh(blacklistip):
  import paramiko
  import time
  ip = "204.16.58.150"
  username = "admin"
  password = "3110"
  port = 22
  conntimeout = 10
  cmdtimeout = 10
  theoutput = []
  # lets remove any new lines
  ip = ip.rstrip("\n\r")
  theoutput = []
  try:
    ssh = paramiko.SSHClient()
    m = re.search(r"\d+\.\d+\.\d+\.\d+", blacklistip)
    if m:
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      #print('connecting to %s' % ip + 'end')
      ssh.connect(hostname=str(ip), port=str(port), username=str(username), password=str(password), look_for_keys=False, allow_agent=False, timeout=float(conntimeout))
      #print('Successfully connected to %s' % ip)
      remote_conn = ssh.invoke_shell()
      time.sleep(0.300)
      thecmd = []
      #thecmd.append(":execute \"/routing bgp network add network="+str(blacklistip)+" comment="+str(blacklistip)+" synchronize=no; :delay 10s; /routing bgp network remove [find comment="+str(blacklistip)+"];\"")
      #thecmd.append(":execute \"/routing filter find; /routing filter add chain=ebgp-out comment="+str(blacklistip)+" disabled=no prefix="+str(blacklistip)+" prefix-length=32 set-bgp-communities=6939:666 action=accept place-before=0;\"")
      #thecmd.append(":execute \"/routing filter find; /routing filter add chain=ebgp-out comment="+str(blacklistip)+" disabled=no prefix="+str(blacklistip)+" prefix-length=32 set-bgp-communities=6939:666 action=passthrough place-before=0\"")
      #thecmd.append(":execute \"/ip route add comment="+str(blacklistip)+" distance=1 dst-address="+str(blacklistip)+" type=blackhole\"")
      thecmd.append(":put \"OK\";")
      for cmd in thecmd:
        stdin,stdout,stderr = ssh.exec_command(cmd, timeout=float(cmdtimeout))
        time.sleep(0.300)
      theoutput = stdout.readlines()
      ssh.close()
    if ssh:
      ssh.close()
  except Exception as e:
    if ssh:
      ssh.close()
      logging.info("Could not ssh to rochfiber"+str(e))
      #print("closed ssh conn"+str(e))
    pass
  return theoutput

#thereturn = ssh(str(gipaddress),str(theuser[authcnt]),str(thepass[authcnt]),"22",str(thecmd),"10","20")
logging.basicConfig(filename='/tmp/fastnetmon_notify_script.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
if len(sys.argv) != 3:
    logging.error("Please provide two arguments for script: action and IP address")
    sys.exit(1)
# Action could be: ban, unban, partial_block
action = sys.argv[1]
ip_address = sys.argv[2]
#logging.info("Start for action %s and IP %s" % (action, ip_address))
# Read all data from stdin
stdin_data = sys.stdin.read()
#logging.info("We got following details: " + stdin_data)
parsed_details = json.loads(stdin_data)
#logging.info("Decoded details from JSON: " + pprint.pformat(parsed_details))
# You can use attack details in this form:
try:
  # need to find out if this is ban or unban
  gaction = parsed_details['action']
  if gaction == "ban":
    gip = str(parsed_details['ip'])
    gip = "64.62.238.202"
    #logging.info("Action: " + str(parsed_details['ip'] + " " + parsed_details['action']))
    #logging.info("Action: " + str(parsed_details['attack_details']['total_incoming_flows']))
    #logging.info("Action: " + str(parsed_details['attack_details']['total_incoming_traffic']))
    #logging.info("Action: " + str(parsed_details['attack_details']['total_incoming_pps']))
    # lets flip the cgnat
    cgnatcmd = ":put \"OK\"; :log info \"blackhole test: "+str(gip)+"\"; :global ddosdetected 3"
    thereturn = ""
    retries = 2
    retriescnt = 0
    while len(thereturn) == 0 and retriescnt < retries:
      retriescnt = retriescnt + 1
      logging.info("Action: "+str(cgnatcmd))
      #thereturn = ssh(gip,'admin','3110',"22",cgnatcmd,"5","5")
      logging.info("Action return: "+str(thereturn))
      logging.info("Action: "+str(len(thereturn)))
      time.sleep(5)
    if len(thereturn) == 0:
      logging.info("Action: Failed to ssh to cgnat to stop the attack: "+str(gip))
    # lets blackhole at roch
    thereturn = ""
    retries = 10
    retriescnt = 0
    while len(thereturn) == 0 and retriescnt < retries:
      retriescnt = retriescnt + 1
      #logging.info("Action: "+str(rochcmd))
      #thereturn = rochssh(gip)
      logging.info("Action return: "+str(thereturn))
      logging.info("Action: "+str(len(thereturn)))
      time.sleep(5)
    if len(thereturn) == 0:
      logging.info("Action: Failed to ssh to Roch to stop the attack: 204.16.58.150")
  if gaction == "unban":
    #
  # + parsed_details['attack_details']['total_incoming_flows'])
except Exception as ex:
  logging.info("Action Error: "+str(ex))

