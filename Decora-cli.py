#!/usr/bin/python

from decora_wifi import DecoraWiFiSession
from decora_wifi.person import Person
from decora_wifi.residential_account import ResidentialAccount
from decora_wifi.residence import Residence
import sys
import time

req_switch_ids = False
execute_ON_OFF = False

if len(sys.argv) < 4:
    print('\nUsage: {} [email] [pswd] [id#:ON|OFF|0-100] <[id#:ON|OFF|0-100]> <etc.>'.format(sys.argv[0]))
    print(  'Usage: {} [email] [pswd] [id#:?] <[id#:?]> <etc.>   ... list current status of switch(es)'.format(sys.argv[0]))
    print(  'Usage: {} [email] [pswd] ?         ... list all switch ids\n'.format(sys.argv[0]))
    sys.exit(1)

decora_email = sys.argv[1]
decora_pass = sys.argv[2]
if sys.argv[3] == '?':       # request a list of all switches with switch id's
    req_switch_ids = True

else:                        # execute ON|OFF|0-100 and/or get status
    execute_ON_OFF = True

session = DecoraWiFiSession()
session.login(decora_email, decora_pass)

perms = session.user.get_residential_permissions()
# print('{} premissions'.format(len(perms)))
all_residences = []
for permission in perms:
    # print("Permission: {}".format(permission))
    if permission.residentialAccountId is not None:
        acct = ResidentialAccount(session, permission.residentialAccountId)
        for res in acct.get_residences():
            # print("Residence: {}".format(res))
            all_residences.append(res)
    elif permission.residenceId is not None:
        res = Residence(session, permission.residenceId)
        # print("Residence: {}".format(res))
        all_residences.append(res)

all_switches = []
for residence in all_residences:    # only tested with one residence

    if execute_ON_OFF == True: # execute ON|OFF|0-100 for each switch designated on command line
        i = 4
        while i <= len(sys.argv):
            decora_pair = sys.argv[i-1].split(":")
            decora_id = decora_pair[0] 
            decora_cmd = decora_pair[1]

            switch_num = residence.find_by_id_iot_switches(decora_id)

            attribs = {}
            if decora_cmd == 'ON':
                attribs['power'] = 'ON'
                print("{}. #{} {} ({})".format(i-3,switch_num.id,decora_cmd,switch_num.name))
                switch_num.update_attributes(attribs)   # perform command on the designated switch
            elif decora_cmd == 'OFF':
                attribs['power'] = 'OFF'
                print("{}. #{} {} ({})".format(i-3,switch_num.id,decora_cmd,switch_num.name))
                switch_num.update_attributes(attribs)   # perform command on the designated switch
            elif decora_cmd == '?':
                print("{}  ID#{}  ({})".format(switch_num.power,switch_num.id,switch_num.name))
            elif decora_cmd == '??':
                if switch_num.model == 'DW6HD':
                    print(switch_num.brightness)
                else:
                    print(switch_num.power)
            else:
                decora_bright = int(decora_cmd)
                attribs['brightness'] = decora_bright
                print("{}. #{} {}% ({})".format(i-3,switch_num.id,decora_cmd,switch_num.name))
                switch_num.update_attributes(attribs)   # perform command on the designated switch

            time.sleep(.300)       # sleep 300 milliseconds
            i += 1

    elif req_switch_ids == True:    # print residence and switch imformation

        print("Permission id#{} (Accountid#{})".format(permission.id, permission.residentialAccountId))
        # print("Permission: {}".format(permission))   # prints all information
        print("Residence  id#{}  ({})".format(res.id,res.name))
        # print("Residence: {}".format(res))  # prints all information
        i = 1
        for switch in residence.get_iot_switches():
            print("Switch{}    id#{} ({})  status: {}".format(i,switch.id,switch.name,switch.power))
            # print("Switch: {}".format(switch))   # prints all information
            i += 1


Person.logout(session)
