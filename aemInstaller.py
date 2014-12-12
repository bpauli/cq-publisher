#!/usr/bin/python

import subprocess
import signal
import os
import sys
import psutil
import json
import requests

from time import sleep
from optparse import OptionParser
from requests.exceptions import ConnectionError
from simplejson.scanner import JSONDecodeError

# defaults
port = "4503"
runmode = "publish"
filename = "cq-publish-4503.jar"

# Argument definition
usage = "usage: %prog [options] arg"
parser = OptionParser(usage)
parser.add_option("-i", "--install_file", dest="filename",
                    default=filename, help="AEM install file")
parser.add_option("-r", "--runmode", dest="runmode",
                    default=runmode, help="Run mode for the installation")
parser.add_option("-p", "--port", dest="port", default=port, help="Port for instance")

options, args = parser.parse_args()
optDic = vars(options)

# Copy out parameters
fileName = optDic['filename']
runmode = optDic['runmode']
port = optDic['port']

baseUrl = "http://localhost:" + port

def allBundlesRunning():
    body = requests.get(baseUrl + "/system/console/bundles/.json", auth=('admin', 'admin')).json()
    allBundlesRunning = True
    for bundle in body["data"]:
        if bundle["state"] != "Active" and bundle["state"] != "Fragment":
            allBundlesRunning = False
            break
    return allBundlesRunning

# Starts AEM installer
installProcess = subprocess.Popen(['java', '-jar', fileName, '-r',runmode,'nosample','-p',port])
successfulStart = False


while 1:
    try:
        if allBundlesRunning() == True:
            successfulStart = True
            break
    except (ConnectionError, JSONDecodeError):
        sleep(1)

#Post install hook
postInstallHook = "postInstallHook.py"
if os.path.isfile(postInstallHook):
    print "Executing post install hook"
    returncode = subprocess.call(["python", postInstallHook])
    print returncode
else:
    print "No install hook found"

# Stop install process
print "Stopping instance"
if successfulStart == True:
  parentProcess = psutil.Process(installProcess.pid)
  for childProcess in parentProcess.get_children():
    os.kill(childProcess.pid,signal.SIGINT)

  os.kill(parentProcess.pid, signal.SIGINT)

  installProcess.wait()
  sys.exit(0)
else:
  installProcess.kill()
  sys.exit(1)
