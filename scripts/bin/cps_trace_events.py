#!/usr/bin/env python
#
# Copyright (c) 2015 Dell Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT
# LIMITATION ANY IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS
# FOR A PARTICULAR PURPOSE, MERCHANTABLITY OR NON-INFRINGEMENT.
#
# See the Apache Version 2.0 License for specific language governing
# permissions and limitations under the License.
#

import sys
import cps
import cps_utils

def cps_trace_usage():
    print ""
    print "Usage: cps_trace_events.py <qualifier> [object]"
    print "   qualifier (mandatory): observed,target,proposed or realtime"
    print "   object (optional): if object is not given all the event related to the qualifier will be captured"
    print "Example: cps_trace_events.py observed base-pas/media OR cps_trace_events.py observed"
    print ""
    exit(1)


if __name__ == '__main__':

    _qual = ["target", "observed", "proposed", "realtime"]

    if (len(sys.argv) < 2) or (len(sys.argv) > 3):
         cps_trace_usage()
         exit(1)

    in_qual = sys.argv[1].lower();
    if in_qual not in _qual:
         print "\nCheck the qualifier, not a valid qualifier "
         cps_trace_usage()
         exit(1)

    if len(sys.argv) > 2:
       _key = cps.key_from_name(in_qual, sys.argv[2])
    else:
       _key = cps.key_from_qual(in_qual)

    print "Key : " + _key

    if ((_key == "") or (_key == None)):
        print "Check the object name, not a valid object\n"
        exit(1)

    if len(sys.argv) > 2:
        print " Registering for " + in_qual + " " + sys.argv[2]
    else:
        print " Registering for " + in_qual

    handle = cps.event_connect()

    cps.event_register(handle, _key)

    while True:
        ev = cps.event_wait(handle)
        print ev['key']
        if 'operation' in ev:
            print "Operation : ", ev['operation']
        cps_utils.print_obj(ev)
