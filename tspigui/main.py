# ############################################################################ #
# tspigui - Simple, touch-screen Raspberry Pi GUI for personal projects        #
# main.py - App main window                                                    #
# pareidolia.es, 2020                                                          #
# ############################################################################ #
# TODO Improve error handling for non-existent properties
# TODO Implement status bar / log widget
from guizero import App, MenuBar
import os
import sys

_m_ = sys.modules[__name__]
_m_.app = None
_m_.r = None
_m_.kb_subp = None

def init(r):
    _m_.r = r
    _m_.r.log.info('Building GUI')
    _m_.app = App()
    
    # Window title
    if _m_.r.has_property('gui.title.ro'): 
        _m_.app.title = _m_.r.get_property('gui.title.ro')
        _m_.r.log.debug('GUI title set to "%s"', _m_.app.title)
    else:
        _m_.app.title = 'tspigui'
        _m_.r.log.debug('GUI title set to "pigui" \
(gui.title.ro property not found)')
        
    # Window geometry & appearance
    geometry = _m_.r.get_property('gui.geometry.ro')
    if geometry=='fs':
        _m_.app.tk.attributes("-fullscreen", True)
        _m_.r.log.debug('GUI size set to fullscreen')
    else:
        try:
            w_h = geometry.split('x')
            _m_.app.width = w_h[0]
            _m_.app.height = w_h[1]
            _m_.r.log.debug('GUI size set to %s', geometry)
        except:
            _m_.r.log.debug('GUI size not set (bad geometry in gui.geometry.ro \
property)')
        
    bg = _m_.r.get_property('gui.bg.ro')
    _m_.app.bg = bg
    _m_.r.log.debug('GUI bg colour set to %s', bg)

    # GUI menu
    MenuBar(_m_.app, ['System'],
            [
                [
                    ['Exit GUI', lambda:gui_exit()],
                    ['---', None],
                    ['Reboot OS', lambda:os_reboot()],
                    ['Halt OS', lambda:os_halt()]
                ]
            ])

    # All done
    _m_.r.log.info('GUI complete, showing now \o/')
    _m_.app.display()
    _m_.r.log.info('GUI closed :_(')
    
# Menu option functions

def gui_exit():
    _m_.r.log.debug('Menu option: exit GUI')
    _m_.app.destroy()

def os_reboot():
    cmd = _m_.r.get_property('gui.cmd.os.reboot.ro')
    _m_.r.log.debug('Menu option: reboot OS (run: %s)', cmd)
    exitcode = os.system(cmd)
    if exitcode!=0:
        _m_.r.log.error('OS reboot failed, exit code: %d', exitcode)

def os_halt():
    cmd = _m_.r.get_property('gui.cmd.os.halt.ro')
    _m_.r.log.debug('Menu option: halt OS (run: %s)', cmd)
    exitcode = os.system(cmd)
    if exitcode!=0:
        _m_.r.log.error('OS halt failed, exit code: %d', exitcode)

# ############################################################################ #
