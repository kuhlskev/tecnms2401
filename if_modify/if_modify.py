#! /usr/bin/env python
# Sample if_modify routine. This uses ncclient to send NETCONF XML RPC's
# Reads ISIS adjacency status and an IPv4 prefix every cycle from XR
# If conditions are met, a loopback is added/deleted or no change
# Two logs appended, one detailed, the other is a one liner per interval
# mamikhai@cisco.com

import sys, os, warnings
warnings.simplefilter("ignore", DeprecationWarning)
from ncclient import manager
import time
from datetime import datetime

# target NETCONF server
server = '10.101.112.1'
# time between checks in seconds
t = 300.000
# filters and responses
filter1 = 'filter-oper-router-isis-neighbors.xml'
filter2 = 'filter-oper-rib-ipv4-default.xml'
response1 = 'isis.xml'
response2 = 'rib.xml'
action1 = 'edit-config-delete-loopback55.xml'
action2 = 'edit-config-add-loopback55.xml'

# minimum IGP adjacencies for no need for loopback
min_adj = 2

logfile = 'if_modify.log'
tracefile = 'if_modify.trace.log'

user ='cisco'
password ='cisco'

def check_oper(subtree_filter, response, trace_string, count_string):
    count = 0
    trace = open(tracefile,'a')
    op_time = str(datetime.now())
    trace.write(op_time + ' ' + str(trace_string) + ' ' + str(count_string) + '\n')
    
    # Get data, record
    c = m.get(filter = ('subtree', open(subtree_filter, 'r').read()))
    with open(response, 'w') as f:
        f.write(str(c))
    # Check for target data, record, count
    with open(response, 'r') as f:
        for line in f:
            if trace_string and (trace_string in line):
                trace.write(line)
            if count_string in line:
                count +=1
    trace.close()
    return count

if __name__ == '__main__':
    # Log start time
    trace = open(tracefile,'a')
    log = open(logfile,'a')
    op_time = str(datetime.now())
    trace.write(op_time + ' start' + '\n')
    log.write(op_time + ' start' + '\n')
    trace.close()
    log.close()
    
    with manager.connect(host=server, port=830, username=user, password=password) as m:
        # Endless cycle
        while True:
            log = open(logfile, 'a')
            op_time = str(datetime.now())
            
            # Read ISIS adjacencies
            adj = check_oper(filter1, response1, '<system-id>', '<neighbor-state>isis-adj-up-state</neighbor-state>')
            log.write(op_time + ' adjacencies: ' + str(adj))
            
            # Check for presence of a specfic interface in IPv4 global RIB
            route = check_oper(filter2, response2, None, '<interface-name>Loopback55</interface-name>')
            
            # If adjacencies back to normal and loopback is in RIB, delete loopback55
            if adj >= min_adj:
                if route:
                    m.edit_config(open(action1, 'r').read(), format='xml', target='candidate', default_operation='merge')
                    m.commit()
                    log.write('; loopback55 deleted')
            # If adjacencies drop and loopback is not in RIB, configure loopback55
            elif not route:
                m.edit_config(open(action2, 'r').read(), format='xml', target='candidate', default_operation='merge')
                m.commit()
                log.write('; loopback55 configured')
            log.write('\n')
            log.close()
            
            # Wait for next cycle
            time.sleep(t)
