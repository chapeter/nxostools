#!/usr/bin/env python3
###This script takes minimal user input to create a VPC domain between two switches.###
###Currently assumes switches will peer via mgmt port and vrf, could easily be changed###
###Currently does not check for any previous config on ports defined for use###
###Script will wipe VPC config before running###

__author__ = 'chapeter@cisco.com'

import nxapilib
import pprint




def domain_input():
    vpc = {}
    #VPC Variables
    vpc['domainid'] = input("Enter VPC Domain ID: ")
    vpc['keepalive_vrf'] = "mgmt"
    return vpc

# def test_domain_input():
#     vpc = {}
#     #VPC Variables
#     vpc['domainid'] = "1"
#     vpc['keepalive_vrf'] = "mgmt"
#     return vpc



def switch1_input():
    switch1 = {}
    #Switch1 Variables
    switch1['ip'] = input("Switch 1's mgmt IP address: ")
    switch1['user'] = input("username: ")
    switch1['pass'] = input("password: ")
    switch1['vpc_peer'] = input("VPC Peer-link Portchannel ID: ")
    switch1['vpc_peer_members'] = list()

    port_count = input("Number of ports in Peer-Link Portchannel: ")
    for i in range(int(port_count)):
        port = input("port: ")
        switch1['vpc_peer_members'].append(port)

    return switch1

# def test_switch1_input():
#     switch1 = {}
#     #Switch1 Variables
#     switch1['ip'] = "10.94.238.75"
#     switch1['user'] = "admin"
#     switch1['pass'] = "cisco"
#     switch1['vpc_peer'] = "1"
#     switch1['vpc_peer_members'] = list()
#
#     port_count = "1"
#     for i in range(int(port_count)):
#         port = "e1/4"
#         switch1['vpc_peer_members'].append(port)
#
#     return switch1


def switch2_input():
    switch2 = {}
    #Switch2 Variables
    switch2['ip'] = input("Switch 2's mgmt IP address: ")
    switch2['user'] = input("username: ")
    switch2['pass'] = input("password: ")
    switch2['vpc_peer'] = input("VPC Peer-link Portchannel ID: ")
    switch2['vpc_peer_members'] = list()

    port_count = input("Number of ports in Peer-Link Portchannel: ")
    for i in range(int(port_count)):
        port = input("port: ")
        switch2['vpc_peer_members'].append(port)

    return switch2

# def test_switch2_input():
#     switch2 = {}
#     #Switch1 Variables
#     switch2['ip'] = "2.2.2.2"
#     switch2['user'] = "admin"
#     switch2['pass'] = "cisco"
#     switch2['vpc_peer'] = "1"
#     switch2['vpc_peer_members'] = list()
#
#     port_count = "1"
#     for i in range(int(port_count)):
#         port = "e1/4"
#         switch2['vpc_peer_members'].append(port)
#
#     return switch2




#Gather VPC Domain info
vpc = domain_input()
#vpc = test_domain_input()
#print(vpc)

#Gather Switch1 info
switch1 = switch1_input()
#switch1 = test_switch1_input()
#print(switch1)

#Gather Swtich2 info
switch2 = switch2_input()
#switch2 = test_switch2_input()
#print(switch2)


switch1_config = ["no feature vpc", "feature vpc", "feature lacp", "vpc domain " + vpc['domainid'], "peer-keepalive destination " + switch2['ip'] + " source " + switch1['ip'] + " vrf " + vpc['keepalive_vrf'], "interface port-channel " + switch1['vpc_peer'], "switchport mode trunk", "vpc peer-link", "no shut", "interface " + ",".join(switch1['vpc_peer_members']), "switchport", "switchport mode trunk", "channel-group " + switch1['vpc_peer'] + " mode active", "no shut"]
switch2_config = ["no feature vpc", "feature vpc", "feature lacp", "vpc domain " + vpc['domainid'], "peer-keepalive destination " + switch1['ip'] + " source " + switch2['ip'] + " vrf " + vpc['keepalive_vrf'], "interface port-channel " + switch2['vpc_peer'], "switchport mode trunk", "vpc peer-link", "no shut", "interface " + ",".join(switch2['vpc_peer_members']), "switchport", "switchport mode trunk", "channel-group " + switch2['vpc_peer'] + " mode active"]

switch1_status = nxapilib.send_config(switch1['ip'], switch1['user'], switch1['pass'], switch1_config)
switch2_status = nxapilib.send_config(switch2['ip'], switch2['user'], switch2['pass'], switch2_config)


print("Switch1")
pprint.pprint(switch1_status)

print("Switch2")
pprint.pprint(switch2_status)





