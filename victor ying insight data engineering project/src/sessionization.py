#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 13:33:13 2018

@author: victorying
"""

# load libraries
import sys
import csv
from datetime import datetime as dt # for representing date-time objects, which are more usefull
from datetime import timedelta as td # for adding units of time

# set paths
log_csv_path = sys.argv[1]
inactivity_period_txt_path = sys.argv[2]
sessionization_txt_path = sys.argv[3]

# get threshold value from initialization.txt
input = open(inactivity_period_txt_path, 'r', 1)
deltat_threshold = td(0, int(input.read().strip()))
input.close()

# initialize
active = {} # dictionary of IPs with sessions that have yet to be identified
add = {} # dictionary of IPs to be added to "active" dictionary

output = open(sessionization_txt_path, 'w')
with open(log_csv_path, newline='') as input:    
    reader = csv.DictReader(input, delimiter=',')
    for row in reader:
        ip = row['ip']
        date = row['date']
        time = row['time']
        t_present =  dt.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S") # current (date-)time
        if ip not in active:
            add.update({ ip :{ 't_1':t_present, 't_n':t_present, 'n':1}})
        for key in list(active): 
            t_1 = active[key]['t_1'] # (date-)time of first request in session
            t_n = active[key]['t_n'] # (date-)time of last request (so far) in session
            n = active[key]['n'] # total number of requests made (so far) in session
            deltat_npresent = t_present - t_n # Δt_n,present -- the amount of time from last document request to present time
            deltat_1n = t_n - t_1 # Δt_1,n -- session time, amount of time from first request to last request
            if (deltat_npresent > deltat_threshold):
                output.write( str(key) + ',' + str(t_1) + ',' + str(t_n) + ',' + str((deltat_1n + td(0,1)).seconds) + ',' + str(n) + '\n' )
                del active[key]
                if key==ip: # if IP is the one making the request, then add it to dictonary of active sessions, with current request as first request of a new session.
                    active.update( { key : { 't_1' : t_present, 't_n' : t_present, 'n' : 1 } } )
            elif key==ip:
              active.update( { key : { 't_1' : t_1, 't_n' : t_present, 'n' : n + 1 } } ) # update dictonary entry of IP making request to reflect new information
        for key in list(add):
            active.update( { key : { 't_1' : t_present, 't_n' : t_present, 'n' : 1 } } )
            del add[ip]

for k, v in sorted(active.items(), key=lambda e: e[1]['t_1']):
    output.write( str( k ) + ',' + str( v['t_1'] ) + ',' + str( v['t_n'] ) + ',' + str( (v['t_n'] - v['t_1'] + td(0,1)).seconds) + ',' + str( v['n'] ) + '\n')

# close sessionization.txt file
output.close()