# ############################################################################ #
# tspigui - Simple, touch-screen Raspberry Pi GUI for personal projects        #
# main.py - App main window                                                    #
# pareidolia.es, 2020                                                          #
# ############################################################################ #
# TODO Improve error handling for non-existent or badly-formatted properties
# TODO Implement status bar / log widget
from functools import partial
from guizero import App, Box, MenuBar, PushButton, TextBox
import os
import pkgutil
import sys

_m_ = sys.modules[__name__]
_m_.app = None
_m_.r = None
_m_.kb_subp = None
_m_.wmods_names = []
_m_.wmods_boxes = []

# Main window layout ######################################################### #
def init(r):
    _m_.r = r
    _m_.r.log.info('Building GUI')
    _m_.app = App()
    w = _m_.app.width
    h = _m_.app.height
    
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

    # Available widgets modules
    wmods_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'wmods')
    _m_.r.log.debug('Looking for available widgets modules in %s', wmods_path)
    available_wmods = []
    for imp, name, _ in pkgutil.iter_modules([wmods_path]):
        loader = imp.find_module(name)
        wmod = loader.load_module()
        if hasattr(wmod, 'wmod_name') and hasattr(wmod, 'wmod_order'):
            if wmod.wmod_order>0:
                # TODO Check for duplicate names
                available_wmods.append(wmod)
                _m_.r.log.debug('Widgets module "%s" enabled', name)
            else:
                _m_.r.log.debug('Widgets module "%s" disabled; ignoring', name)
    # TODO Sort modules
    for wmod in available_wmods:
        wmod_box = Box(_m_.app, layout = 'auto', width=w, height=h,
                 visible = False)
        wmod.init(wmod_box, r)
        _m_.wmods_names.append(wmod.wmod_name)
        _m_.wmods_boxes.append(wmod_box)

    # System box (last module)
    sysbox = Box(_m_.app, layout = 'auto', width=w, height=h,
                 visible = False)
    sysbox_b = Box(sysbox, layout='grid', width=sysbox.width, height=1)
    PushButton(sysbox_b, text='Exit GUI', grid=[1,1], width=15,
               command=gui_exit)
    PushButton(sysbox_b, text='Reboot OS', grid=[2,1], width=15,
               command=os_reboot)
    PushButton(sysbox_b, text='Halt OS', grid=[3,1], width=15,
               command=os_halt)
    _m_.wmods_names.append('System')
    _m_.wmods_boxes.append(sysbox)

    # GUI menu
    wmod_submenu = []
    for i in range(len(_m_.wmods_names)):
        wmod_submenu.append([_m_.wmods_names[i], partial(show_module, i)])
    submenus = [
                wmod_submenu,
                [
                    ['Exit GUI',    lambda:gui_exit()],
                    ['Reboot OS',   lambda:os_reboot()],
                    ['Halt OS',     lambda:os_halt()]
                ]
            ]
    MenuBar(_m_.app, ['Show module', 'System'], submenus)
    
    # All done
    _m_.r.log.info('GUI complete, showing now \o/')
    _m_.wmods_boxes[0].visible = True
    _m_.app.display()
    _m_.r.log.info('GUI closed :_(')
    
# Menu / button actions ###################################################### #

def show_module(i):
    for wmod_box in _m_.wmods_boxes:
        wmod_box.visible = False
    _m_.wmods_boxes[i].visible = True

def gui_exit():
    _m_.r.log.debug('Action: exit GUI')
    _m_.app.destroy()

def os_reboot():
    cmd = _m_.r.get_property('gui.cmd.os.reboot.ro')
    _m_.r.log.debug('Action: reboot OS (run: %s)', cmd)
    exitcode = os.system(cmd)
    if exitcode!=0:
        _m_.r.log.error('OS reboot failed, exit code: %d', exitcode)

def os_halt():
    cmd = _m_.r.get_property('gui.cmd.os.halt.ro')
    _m_.r.log.debug('Action: halt OS (run: %s)', cmd)
    exitcode = os.system(cmd)
    if exitcode!=0:
        _m_.r.log.error('OS halt failed, exit code: %d', exitcode)

# ############################################################################ #
