# tspigui
Simple, touch-screen Raspberry Pi GUI for personal projects

It may come handy for PI's running as backend / controller with a touch-screen and no keyboard.

It will likely feature flexible widget-modules support for extending the GUI functionality without the need to deal with its core. Anytime.

## Deployment
```
$ git clone https://github.com/a-zz/tspigui
$ cd tspigui
$ pip3 install -t lib/ guizero
$ cp tspigui.properties.sample tspigui.properties
$ ./tspigui.py
```
You may also want to add a tspigui.desktop file to ~/.config/autostart to get the GUI launched at PI startup, and customize your 
tspigui.properties file to suit your needs.

