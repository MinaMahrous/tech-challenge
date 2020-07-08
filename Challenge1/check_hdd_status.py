#!/usr/bin/python

import sys


with open( './hdd_status', 'r' ) as f:
    read_data = f.read()
f.close()

if 'WARNING' in read_data:
    print('WARNING: %s' %(read_data))
    sys.exit(1)
elif 'CRITICAL' in read_data:
    print('CRITICAL: %s' %(read_data))
    sys.exit(2)
elif 'OK' in read_data:
    print('OK: %s' %(read_data))
    sys.exit(0)


print('UNKNOWN - %s' %(read_data))
sys.exit(0)
