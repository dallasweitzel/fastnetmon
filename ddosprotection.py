import requests
import json
import re
import time
url = 'http://157.245.130.37:10007/blackhole'
username = 'admin'
password = '3110'
data = ""

def rochsshadd(blacklistip):
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
      thecmd.append(":execute \"/routing bgp network add network="+str(blacklistip)+" comment=blacklisted synchronize=no;\"")
      thecmd.append(":execute \"/routing filter find; /routing filter add chain=ebgp-out comment=blacklisted disabled=no prefix="+str(blacklistip)+" prefix-length=32 set-bgp-communities=6939:666 action=accept place-before=0;\"")
      thecmd.append(":execute \"/routing filter find; /routing filter add chain=ebgp-out comment=blacklisted disabled=no prefix="+str(blacklistip)+" prefix-length=32 set-bgp-communities=6939:666 action=passthrough place-before=0\"")
      thecmd.append(":execute \"/ip route add comment=blacklisted distance=1 dst-address="+str(blacklistip)+" type=blackhole\"")
      thecmd.append(":log info \"blackhole: "+str(blacklistip)+"\";")
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

def rochsshdel():
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
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #print('connecting to %s' % ip + 'end')
    ssh.connect(hostname=str(ip), port=str(port), username=str(username), password=str(password), look_for_keys=False, allow_agent=False, timeout=float(conntimeout))
    #print('Successfully connected to %s' % ip)
    remote_conn = ssh.invoke_shell()
    time.sleep(0.300)
    thecmd = []
    thecmd.append("/routing bgp network remove [find comment=blacklisted];")
    thecmd.append("/routing filter remove [find comment=blacklisted and chain=ebgp-out];")
    thecmd.append("/ip rou remove [find comment=blacklisted]")
    thecmd.append(":log info \"blackhole removal\";")
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

def ssh(ip,username,password,port,thecmd,conntimeout,cmdtimeout):
  import paramiko
  import time
  theoutput = []
  # lets remove any new lines
  ip = ip.rstrip("\n\r")
  theoutput = []
  ssh = paramiko.SSHClient()
  try:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #print('connecting to %s' % ip + 'end')
    ssh.connect(hostname=str(ip), port=str(port), username=str(username), password=str(password), look_for_keys=False, allow_agent=False, timeout=float(conntimeout))
    #print('Successfully connected to %s' % ip)
    remote_conn = ssh.invoke_shell()
    time.sleep(0.001)
    stdin,stdout,stderr = ssh.exec_command(thecmd, timeout=float(cmdtimeout))
    theoutput = stdout.readlines()
    ssh.close()
  except Exception as e:
    if ssh:
      ssh.close()
      #print("closed ssh conn"+str(e))
    pass
  if ssh:
    ssh.close()
  return theoutput

thedict = {}
#tracking = {}
#tracking['64.62.238.202'] = '64.62.238.2'
#tracking['64.62.238.203'] = '64.62.238.2'
#for i in tracking:
#  tracking[i]
active = []
activeddos = []
datadict = {}
while True:
  try:
    data = requests.get(url, auth=(username, password)).content
    datadict = json.loads(data)
    ips = []
    thedict = datadict['values']
    # making list
    for i in thedict:
      #print(i)
      for e in i:
        #print(i[e])
        #print(e)
        ip = i[e]
        m = re.search(r"(\d+\.\d+\.\d+\.\d+)\/\d+", ip)
        if m:
          ip = m.group(1)
        key = e
        if e == "ip":
          ips.append(ip)
    # looking for new ddos
    for i in ips:
      #print("IP: "+i)
      if i not in active:
        #print("Not in active")
        m = re.search(r"204.16.58.150\/\d+", i)
        if not m:
          active.append(i)
          cgnatcmd = ":put \"OK\"; :log info \"blackhole: "+str(i)+"\"; :global ddosdetected 1"
          #print(str(cgnatcmd))
          thereturn = ssh(i,'admin','3110',"22",cgnatcmd,"10","10")
          rochsshadd(str(i))
          print("DDOS HIT: "+str(i))
          #thecgnat = ""
          #thecgnat = tracking[i]
          #if i not in activeddos:
          #  print("We set a active ddos for cgnat "+str(i))
          #  activeddos.append(i)
          #else:
          #  print("")
    # lets check to see if a ddos is gone, we only want to remove if all the ddos are gone
    removalisdone = 0
    for i in active:
      #print("Active IP: "+i)
      if len(ips) == 0:
        print("DDOS is gone, removing blackholes and waiting...: "+str(i))
        active.remove(i)
        if removalisdone == 0:
          rochsshdel()
          removalisdone = 1
        cgnatcmd = ":put \"OK\"; :log info \"blackhole removed: "+str(i)+"\"; :global ddosdetected 0"
        #print(str(cgnatcmd))
        print("DDOS is gone, flipping redundancies...: "+str(i))
        ssh(str(i),'admin','3110',"22",cgnatcmd,"10","10")
    removalisdone = 0
      #print("Active IP: "+i)
      #if i not in ips:
      #  print("We are just removing the blackhole "+str(i))
      #  active.remove(i)
      #  #once we do this once, lets remove it from active
      #  #rochsshdel(str(i))
  except Exception as ex:
    print("Woo, "+str(ex))
    pass
  time.sleep(1)