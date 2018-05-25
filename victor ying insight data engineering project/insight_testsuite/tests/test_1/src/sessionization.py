#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 13:33:13 2018

@author: victorying
"""

# load libraries
import sys
import csv
#from datetime import date as d
from datetime import datetime as dt
from datetime import timedelta as td

# initialize:
#input2 = open('../input/inactivity_period.txt', 'r', 1)
input = open(sys.argv[2], 'r', 1)
#output = open('../output/sessionization2.txt', 'w')
output = open(sys.argv[3], 'w')
deltat_threshold = td(0, int(input.read().strip()))
input.close()
active = {}
add = {}

with open(sys.argv[1], newline='') as input:    
    reader = csv.DictReader(input, delimiter=',')
    
    for row in reader:
        ip = row['ip']
#        print(ip)
        date = row['date']
#        print(' ' + date)
        time = row['time']
#        print(' ' + time)
        t_present =  dt.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S")
#        print(' ' + str(t_present))
        cik = row['cik']
        accession = row['accession']
        extention = row['extention']
    
        if ip not in active:
            add.update({ ip :{ 't_1':t_present, 't_n':t_present, 'n':1}})
        
        for key in list(active):
            t_1 = active[key]['t_1']
            t_n = active[key]['t_n']
            n = active[key]['n']
            deltat_npresent = t_present - t_n
            deltat_1n = t_n - t_1
            
#            print("  " + str(deltat_npresent > deltat_threshold) )
            if (deltat_npresent > deltat_threshold):
#                print("    " + key)
#                print("    " + str( deltat_1n.seconds ) )
                output.write( str(key) + ',' + 
                               str(t_1) + ',' + 
                               str(t_n) + ',' + 
                               str((deltat_1n + td(0,1)).seconds) + ',' + 
                               str(n) + '\n' )
                del active[key]
                if key==ip:
                    active.update( { key : { 't_1' : t_present,
                                            't_n' : t_present,
                                              'n' : 1 } } )
            elif key==ip:
              active.update( { key : { 't_1' : t_1,
                                      't_n' : t_present,
                                        'n' : n + 1 } } )

        for key in list(add):
            active.update( { key : { 't_1' : t_present,
                                     't_n' : t_present,
                                       'n' : 1 } } )
            del add[ip]

for k, v in sorted(active.items(), key=lambda e: e[1]['t_1']):
    output.write( str( k ) + ',' + 
                   str( v['t_1'] ) + ',' + 
                   str( v['t_n'] ) + ',' +
                   str( (v['t_n'] - v['t_1'] + td(0,1)).seconds) + ',' +
                   str( v['n'] ) + '\n')
output.close()

#for k, v in sorted(active.items(), key=lambda e: e[1]['t_1']):
#    print(k,v)