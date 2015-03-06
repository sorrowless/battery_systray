#!/usr/bin/env python
from gi.repository import Gtk, GObject

import sys
import subprocess
import os
import json
import re

class Indicator:
    def __init__(self, icon):
        self.appicon = icon
        self.icon = Gtk.StatusIcon()
        self.icon.set_from_file(self.appicon)

        self.menu = Gtk.Menu()
        self.icon.connect('popup-menu', self.right_click_event_statusicon)

    def set_refresh(self, timeout, callback, *callback_args):
        GObject.timeout_add(timeout, callback, *callback_args)

    def set_icon(self, icon):
        self.icon.set_from_file(icon)

    def add_menu_item(self, command, title):
        mItem = Gtk.MenuItem()
        mItem.set_label(title)
        mItem.connect('activate', command)
        self.menu.append(mItem)
        self.menu.show_all()

    def add_seperator(self):
        mItem = Gtk.SeparatorMenuItem()
        self.menu.append(mItem)
        self.menu.show_all()

    def right_click_event_statusicon(self, icon, button, time):

        def pos(menu, aicon):
            return (Gtk.StatusIcon.position_menu(menu, aicon))

        self.menu.popup(None, None, pos, icon, button, time)


class Application:
    def __init__(self):
        if os.path.isfile('settings.json'):
            settings = json.load(open('settings.json','r'))
        elif os.path.isfile('%s/.config/battery-systray/settings.json' % os.getenv('HOME')):
            settings = json.load(open('%s/.config/battery-systray/settings.json' % os.getenv('HOME'),'r'))
        elif os.path.isfile('/etc/battery-systray/settings.json'):
            settings = json.load(open('/etc/battery-systray/settings.json','r'))
        else:
          print('Settings file not found.')
          sys.exit()

        # TODO: check files existance in theme dir
        theme = settings['theme']['themeName']
        if os.path.isdir('themes/%s' % theme):
            path = os.path.abspath('themes/%s' % theme)
        elif os.path.isdir('%s/.config/battery-systray/themes/%s' % (os.getenv('HOME'),theme)):
            path = os.path.abspath('%s/.config/battery-systray/themes/%s' % (os.getenv('HOME'),theme))
        elif os.path.isdir('/usr/share/battery-systray/themes/%s' % theme):
            path = os.path.abspath('/usr/share/battery-systray/themes/%s' % theme)
        else:
            print('Theme directory not found.')
            sys.exit()

        self.chlist = []
        self.dischlist = []
        regex = re.compile(r'(?P<val>\d\d|100)-(?P<stat>charging|discharging)\.(?P<ext>png|svg)')
        # it's a bad idea, but right now I cannot do any else
        ext = ''
        for file in os.listdir(path):
          answer = regex.match(file)
          if (file.endswith('-charging.png') or file.endswith('-charging.svg')) and answer.group('val'):
            self.chlist.append(answer.group('val'))
          elif (file.endswith('-discharging.png') or file.endswith('-discharging.svg')) and answer.group('val'):
            self.dischlist.append(answer.group('val'))
          if (file.endswith('-discharging.png') or file.endswith('-discharging.svg')) and answer.group('ext'):
            ext = answer.group('ext')
        self.chlist.sort()
        self.dischlist.sort()
        self.deficon = path + '/default.' + ext
        self.chformat = path + '/{value}-charging.' + ext
        self.dischformat = path + '/{value}-discharging.' + ext

        self.indicator = Indicator(self.deficon)
        self.indicator.add_menu_item(lambda x: Gtk.main_quit(), "Quit")
        refresh_timeout = int(settings['common']['refresh_timeout'])
        if not refresh_timeout or refresh_timeout < 1000: refresh_timeout = 1000
        self.indicator.set_refresh(refresh_timeout, self.check_battery)
        #self.indicator.icon.set_tooltip_text(subprocess.getoutput("acpi"))
        self.indicator.icon.set_has_tooltip(True)
        self.indicator.icon.connect("query-tooltip", self.tooltip_query)
        #self.indicator.add_menu_item(lambda x: self.indicator.set_icon(os.path.abspath('icon1.svg')),'New Icon')

    def check_battery(self):
        self.charging = False if subprocess.getoutput("cat /sys/class/power_supply/BAT0/status") == 'Discharging' else True
        percent = subprocess.getoutput("cat /sys/class/power_supply/BAT0/capacity")
        if not self.charging:
          for v in self.dischlist:
            self.indicator.set_icon(self.dischformat.format(value=v)) if int(percent) <= int(v) else False
        else:
          for v in self.chlist:
            self.indicator.set_icon(self.chformat.format(value=v)) if int(percent) <= int(v) else False
        return True

    def tooltip_query(self, widget, x, y, keyboard_mode, tooltip):
        tooltip.set_text(subprocess.getoutput("acpi"))
        return True

if __name__ == '__main__':
    app = Application()
    Gtk.main()
