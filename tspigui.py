#!/usr/bin/env python3
# ############################################################################ #
# tspigui - Simple, touch-screen Raspberry Pi GUI for personal projects        #
# tspigui.py - App startup                                                     #
# pareidolia.es, 2020                                                          #
# ############################################################################ #
import os
import sys
os.chdir(os.path.dirname(sys.argv[0]))
from sys import path
path.append('./lib')
from tspigui import main, rcic

# App startup
r = rcic.Rcic('tspigui')
r.log.info('Starting up!')
main.init(r)

# App shut down
r.log.info('Shut down!')
# ############################################################################ #
