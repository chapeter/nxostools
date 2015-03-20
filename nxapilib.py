#!/usr/bin/env python3
__author__ = 'chapeter@cisco.com'

import requests
import json

###This is a libary of various tasks I needed to do or data to collect from a NXOS box via NXAPI.  Main function is
###send_command.  This will format the post properly. send_config will take configs and run them against the box
###Need to write some more generic functions.  The rest of the funcitons very specific and do the data parsing w/in them
###Error handling needs to be addressed at some point if this is really going to be utlized

#To do:
#   Write function to take show commands and display in either dict format or raw ascii

def send_config(ip, user, password, commands):
    #This function defines attributes for the post.  Will take a list of any number of configuration commands, run them
    #via NXAPI.  It returns all commands run and their status.

    #To Do:
    #   Needs error handling.  If something doesn't execute return something useful...don't bomb out
    url = 'http://%s/ins' % (ip)
    type = "cli_conf"
    output = "json"
    raw_data = send_command(url, user, password, type, ' ; '.join(commands), output)
    print(raw_data)
    command_status = {}
    y=0
    for x in commands:
        print(commands[y], raw_data['ins_api']['outputs']['output'][y]['code'])
        command_status[commands[y]] = raw_data['ins_api']['outputs']['output'][y]['code']
        y = y + 1

    return command_status


def send_command(url, user, password, type, myinput, output):
    #This function formats the post properly and returns raw data.  It will work with any type of NXAPI call.
    #Cleanup to do:
    #   Should only require ip, not URL.  URL construction should be performed within this function.
    #   My headers needs to be adjusted to match output variable
    #   Should check for json or xml...or perhaps only allow json, don't ask for any formatting, and conversion would
    #       happen elsewhere
    myheaders={'content-type':'application/json'}
    payload={
        "ins_api": {
            "version": "1.0",
            "type": type,
            "chunk": "0",
            "sid": "1",
            "input": myinput,
            "output_format": output
        }
    }
    print(myinput)
    response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(user,password)).json()
    return response


def showver(ip, user, password):
    url = 'http://%s/ins' % (ip)
    type = "cli_show"
    command = "show ver"
    output = "json"

    raw_data = send_command(url, user, password, type, command, output)

    return (raw_data['ins_api']['outputs']['output']['body']['kickstart_ver_str'])


def getuptime(ip, user, password):
    url = 'http://%s/ins' % (ip)
    type = "cli_show"
    command = "show ver"
    output = "json"

    raw_data = send_command(url, user, password, type, command, output)

    uptime2 = raw_data['ins_api']['outputs']['output']['body']['kern_uptm_days'], "days", raw_data['ins_api']['outputs']['output']['body']['kern_uptm_hrs'],"hrs", raw_data['ins_api']['outputs']['output']['body']['kern_uptm_mins'],"min", raw_data['ins_api']['outputs']['output']['body']['kern_uptm_secs'], "sec"

    uptime = "%s days %s hours %s min %s sec" % (raw_data['ins_api']['outputs']['output']['body']['kern_uptm_days'], raw_data['ins_api']['outputs']['output']['body']['kern_uptm_hrs'], raw_data['ins_api']['outputs']['output']['body']['kern_uptm_mins'],raw_data['ins_api']['outputs']['output']['body']['kern_uptm_secs'])
    return uptime



def getinterfaceerrors(ip, user, password):
    url = 'http://%s/ins' % (ip)
    type = "cli_show"
    command = "show interface counters errors"
    output = "json"

    raw_data = send_command(url, user, password, type, command, output)

    return raw_data


def gettotalerrors(ip, user, password):
    raw_errors = getinterfaceerrors(ip, user, password)
    raw_errors = json.dumps(raw_errors, indent=2)

    str_errors = (str(raw_errors))
    error_count = 0
    #print(str_errors)

    for x in str_errors.splitlines(keepends=False):
        if "eth_giants" in x or "eth_inmacrx_err" in x or "eth_inmactx_err" in x or "eth_deferred_tx" in x or "eth_symbol_err" in x or "eth_align_error" in x or "eth_rcv_err" in x or "eth_fcs_err" in x or "eth_xmit_err" in x or "eth_undersize" in x or "eth_outdisc" in x or "eth_runts" in x or "eth_carri_sen" in x or "eth_excess_col" in x or "eth_multi_col" in x or "eth_late_col" in x or "eth_single_col" in x:
            #print(x)
            y = x.split(": ", 1)[1]
            #print(y)
            #print(y.split(",", 1)[0])
            error_count += int(y.split(",", 1)[0])
    return(error_count)


def getstpdetail(ip, user, password):
    url = 'http://%s/ins' % (ip)
    type = "cli_show_ascii"
    command = "show spanning-tree detail"
    output = "json"
    totaltcn = 0
    change_times = []
    raw_data = send_command(url, user, password, type, command, output)
    raw_body = raw_data["ins_api"]["outputs"]["output"]["body"]
    for x in raw_body.splitlines(keepends=False):
        if "Number of topology changes" in x:
            y = x.split("changes ", 1)
            #print(y)
            tcn = (y[1].split(" ",1))
            totaltcn += int(tcn[0])
            z = (tcn[1].split("occurred ",1))
            z = (z[1].split(" ",1))
            change_times.append(z[0])
    #print(totaltcn)
    #print(change_times)
    recenttcn = sorted(change_times)[0]
    #print(sorted(change_times)[0])
    stpinfo = [totaltcn, recenttcn]
    return stpinfo





