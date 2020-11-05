import requests
import json
import re
import time
url = 'http://157.245.130.37:10007/blackhole'
username = 'admin'
password = '3110'
data = ""

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
  data = requests.get(url, auth=(username, password)).content
  datadict = json.loads(data)
  try:
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
        active.append(i)
        cgnatcmd = ":put \"OK\"; :log info \"blackhole: "+str(i)+"\"; :global ddosdetected 1"
        #print(str(cgnatcmd))
        thereturn = ssh(i,'admin','3110',"22",cgnatcmd,"10","10")
        print("DDOS HIT: "+str(i))
        #thecgnat = ""
        #thecgnat = tracking[i]
        #if i not in activeddos:
        #  print("We set a active ddos for cgnat "+str(i))
        #  activeddos.append(i)
        #else:
        #  print("")
    # lets check to see if a ddos is gone
    for i in active:
      #print("Active IP: "+i)
      if i not in ips:
        print("DDOS is gone: "+str(i))
        active.remove(i)
        cgnatcmd = ":put \"OK\"; :log info \"blackhole: "+str(i)+"\"; :global ddosdetected 0"
        #print(str(cgnatcmd))
        thereturn = ssh(i,'admin','3110',"22",cgnatcmd,"10","10")
  except Exception as ex:
    print("Woo, "+str(ex))
    pass
  time.sleep(1)