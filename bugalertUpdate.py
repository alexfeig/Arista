#!/usr/bin/env python
#
# Copyright (c) 2017, Arista Networks, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#  - Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#  - Neither the name of Arista Networks nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#
# Bug Alert Database Updater
#
#    Version 1.0 2/23/2017
#    Written by:
#       Corey Hines, Arista Networks
#
#    Revision history:
#       .1 - Minor edits
#       .2 - Initial version tested on EOS (CVX) 4.18.0F

"""
   DESCRIPTION
   A Python script for updating the AlertBase.json file on CVX running EOS.
   Script can be run manually, or using a scheduler to automatically check www.arista.com
   for database updates for the CVX Bugalerts feature.

   To learn more about BugAlerts see: https://eos.arista.com/eos-4-17-0f/bug-alerts/


   INSTALLATION
   change values of username and password to a valid www.arista.com account

   RFEs
   Add error handling, any error handling at all ;-)
   Add ability to specify username and password as ARGV0/1 for running interactively and not storing password in script
   Add some kind of progress indicator and/or send some loggging output to STDOUT and/or system log
   Add code with eAPI or python ssh library to copy AlertBase.json to all CVX cluster members
"""
__author__ = 'chines'

import base64, json, warnings, requests

username = 'CHANGEME'
password = 'CHANGEME'

string = username + ':' + password
creds = (base64.b64encode(string.encode()))

url = 'https://www.arista.com/custom_data/bug-alert/alertBaseDownloadApi.php'

warnings.filterwarnings("ignore")

jsonpost = {'user_auth': creds}

result = requests.post(url, data=json.dumps(jsonpost))

web_data = json.loads(result.text)
web_data_final = result.text


try:
    current_json = open('/mnt/flash/AlertBase.json', 'r')
    local_data = json.loads(current_json.read())
except:
    print "Bug Alert Databse does not exist. Installing..."
    alertdbfile = open('/mnt/flash/AlertBase.json', 'w')
    alertdbfile.write(web_data_final)
    alertdbfile.close   
    exit(0)

current_version = local_data['genId']

web_version = web_data['genId']

print('\n' + 'DB' + '\t'+ 'Release Date' + '\t' + 'Version').expandtabs(18)
print('----------' + '\t' + '------------' + '\t' + '-----------------------------').expandtabs(18)
print('local version' + '\t' + local_data['releaseDate'] + '\t' + current_version).expandtabs(18)
print('web version' + '\t' + web_data['releaseDate'] + '\t' + web_version).expandtabs(18)

if current_version == web_version:
    print "\nBugAlert database is up to date BUZZ OFF\n"
    exit(0)
else:    
    print "\nUpdating BugAlert database!\n"
    alertdbfile = open('/mnt/flash/AlertBase.json', 'w')
    alertdbfile.write(web_data_final)
    alertdbfile.close
exit(0)