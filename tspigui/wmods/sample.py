# ############################################################################ #
# tspigui - Simple, touch-screen Raspberry Pi GUI for personal projects        #
# sample.py - Sample widgets module                                            #
# pareidolia.es, 2020                                                          #
# ############################################################################ #
from guizero import Text
import sys

_m_ = sys.modules[__name__]
_m_.wmod_cntnr_box = None
_m_.r = None

# Required members for widget integration within tspigui main window
_m_.wmod_name = 'Sample'
_m_.wmod_order = 1          # Widgets modules are sorted by _order and _name
                            #   _order<=0 disables the module

# Required member for widget integration within tspigui main window
def init(cntnr_box, r):
    if _m_.wmod_order<=0:
        raise Exception('Tried to init() disabled module %s', _m_.wmod_name)
                        
    _m_.wmod_cntnr_box = cntnr_box
    _m_.r = r

    _m_.r.log.info('Building widgets module %s', _m_.wmod_name)
    Text(cntnr_box, 'Sample module', color='#ffffff')
    _m_.r.log.info('Module %s complete', _m_.wmod_name)

# ############################################################################ #
