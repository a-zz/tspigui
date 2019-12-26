# ############################################################################ #
# tspigui - Simple, touch-screen Raspberry Pi GUI for personal projects        #
# main.py - App main window                                                    #
# pareidolia.es, 2020                                                          #
# ############################################################################ #
# TODO Improve error handling for non-existent properties
# TODO Implement status bar / log widget
# TODO On-screen keyboard support (matchbox-keyboard)
from guizero import App, MenuBar
import os

app = None

def init(r):
    
    r.log.info('Building GUI')
    app = App()
    
    # Window title
    if r.has_property('gui.title.ro'): 
        app.title = r.get_property('gui.title.ro')
        r.log.debug('GUI title set to "%s"', app.title)
    else:
        app.title = 'tspigui'
        r.log.debug('GUI title set to "pigui" \
(gui.title.ro property not found)')
        
    # Window geometry & appearance
    geometry = r.get_property('gui.geometry.ro')
    if geometry=='fs':
        app.tk.attributes("-fullscreen",True)
        r.log.debug('GUI size set to fullscreen')
    else:
        try:
            w_h = geometry.split('x')
            app.width = w_h[0]
            app.height = w_h[1]
            r.log.debug('GUI size set to %s', geometry)
        except:
            r.log.debug('GUI size not set (bad geometry in gui.geometry.ro \
property)')
        
    bg = r.get_property('gui.bg.ro')
    app.bg = bg
    r.log.debug('GUI bg colour set to %s', bg)

    # GUI menu
    MenuBar(app, ['System'],
            [
                [
                    ['Exit GUI', lambda:gui_exit(app, r)],
                    ['---', None],
                    ['Reboot OS', lambda:os_reboot(r)],
                    ['Halt OS', lambda:os_halt(r)]
                ]
            ])

    # All done
    r.log.info('GUI complete, showing now \o/')
    app.display()
    r.log.info('GUI closed :_(')
    
# Menu option functions
def gui_exit(app, r):
    r.log.debug('Menu option: exit GUI')
    app.destroy()

def os_reboot(r):
    r.log.debug('Menu option: reboot OS')
    exitcode = os.system(r.get_property('gui.cmd.os.reboot.ro'))
    if exitcode!=0:
        r.log.error('OS reboot failed, exit code: %d', exitcode)

def os_halt(r):
    r.log.debug('Menu option: halt OS')
    exitcode = os.system(r.get_property('gui.cmd.os.halt.ro'))
    if exitcode!=0:
        r.log.error('OS halt failed, exit code: %d', exitcode)
    
# ############################################################################ #
