#!/usr/bin/env python3
# The shebang above is to tell the shell which interpreter to use. This make the file executable without "python3" in front of it (otherwise I had to use python3 pyvmc.py)
# I also had to change the permissions of the file to make it run. "chmod +x pyVMC.py" did the trick.
# I also added "export PATH="MY/PYVMC/DIRECTORY":$PATH" (otherwise I had to use ./pyvmc.y)
# For git BASH on Windows, you can use something like this #!/C/Users/usr1/AppData/Local/Programs/Python/Python38/python.exe
# Python Client for VMware Cloud on AWS
################################################################################
### Copyright (C) 2019-2020 VMware, Inc.  All rights reserved.
### SPDX-License-Identifier: BSD-2-Clause
################################################################################
"""
Welcome to PyVMC ! 
VMware Cloud on AWS API Documentation is available at: https://code.vmware.com/apis/920/vmware-cloud-on-aws
CSP API documentation is available at https://console.cloud.vmware.com/csp/gateway/api-docs
vCenter API documentation is available at https://code.vmware.com/apis/366/vsphere-automation
You can install python 3.8 from https://www.python.org/downloads/windows/ (Windows) or https://www.python.org/downloads/mac-osx/ (MacOs).
You can install the dependent python packages locally (handy for Lambda) with:
pip3 install requests or pip3 install requests -t . --upgrade
pip3 install configparser or pip3 install configparser -t . --upgrade
pip3 install PTable or pip3 install PTable -t . --upgrade
With git BASH on Windows, you might need to use 'python -m pip install' instead of pip3 install
"""
import requests                         # need this for Get/Post/Delete                    # parsing config file
import time
import sys
strProdURL      = "https://vmc.vmware.com"
strCSPProdURL   = "https://console.cloud.vmware.com"
def getAccessToken(myKey):
    """ Gets the Access Token using the Refresh Token """
    params = {'refresh_token': myKey}
    headers = {'Content-Type': 'application/json'}
    response = requests.post('https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize', params=params, headers=headers)
    jsonResponse = response.json()
    access_token = jsonResponse['access_token']
    return access_token
def getSDDCIDOdyssey(tenantid, sessiontoken, sddc_id):
    myHeader = {'csp-auth-token': sessiontoken}
    myURL = strProdURL + "/vmc/api/orgs/" + tenantid + "/sddcs/" + sddc_id
    response = requests.get(myURL, headers=myHeader)
    jsonResponse = response.json()
    sddc = jsonResponse['resource_config']
    sddc_password = sddc['cloud_password']
    sddc_url = sddc['vc_url']
    #print(sddc)
    with open('sddc_password.txt', 'w') as filehandle:
            filehandle.write(sddc_password)
    with open('sddc_url.txt', 'w') as filehandle:
            filehandle.write(sddc_url)
    return
# --------------------------------------------
# ---------------- Main ----------------------
# --------------------------------------------
if len(sys.argv) > 4:
    intent_name = sys.argv[4].lower()
else:
    intent_name = ""
ORG_ID = sys.argv[1]
sddc_id = sys.argv[2]
Refresh_Token = sys.argv[3]
session_token = getAccessToken(Refresh_Token)
getSDDCIDOdyssey(ORG_ID,session_token,sddc_id)
