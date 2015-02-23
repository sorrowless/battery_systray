#!/usr/bin/env python
from gi.repository import Gtk, GObject

import sys
import subprocess
import os
import json

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
        if os.path.isfile('%s/.config/battery-systray/settings.json' % os.getenv('HOME')):
            settings = json.load(open('%s/.config/battery-systray/settings.json' % os.getenv('HOME'),'r'))
        elif os.path.isfile('/etc/battery-systray/settings.json'):
            settings = json.load(open('/etc/battery-systray/settings.json','r'))
        elif os.path.isfile('settings.json'):
            settings = json.load(open('settings.json','r'))
        else:
          print('Settings file not found.')
          sys.exit()

        # TODO: check files existance in theme dir
        theme = settings['theme']['themeName']
        if os.path.isdir('%s/.config/battery-systray/themes/%s' % (os.getenv('HOME'),theme)):
            path = '%s/.config/battery-systray/themes' % os.getenv('HOME')
            self.null_icon = os.path.abspath('%s/%s/00-nocharging.svg' % (path,theme))
            self.caution_icon = os.path.abspath('%s/%s/01-caution.svg' % (path,theme))
            self.low_icon = os.path.abspath('%s/%s/05-low.svg' % (path,theme))
            self.good_icon = os.path.abspath('%s/%s/10-good.svg' % (path,theme))
            self.full_icon = os.path.abspath('%s/%s/15-full.svg' % (path,theme))
            self.charging_icon = os.path.abspath('%s/%s/50-charging.svg' % (path,theme))
            self.full_charging_icon = os.path.abspath('%s/%s/99-full-charging.svg' % (path,theme))
        elif os.path.isdir('/usr/share/battery-systray/themes/%s' % theme):
            path = '/usr/share/battery-systray/themes'
            self.null_icon = os.path.abspath('%s/%s/00-nocharging.svg' % (path,theme))
            self.caution_icon = os.path.abspath('%s/%s/01-caution.svg' % (path,theme))
            self.low_icon = os.path.abspath('%s/%s/05-low.svg' % (path,theme))
            self.good_icon = os.path.abspath('%s/%s/10-good.svg' % (path,theme))
            self.full_icon = os.path.abspath('%s/%s/15-full.svg' % (path,theme))
            self.charging_icon = os.path.abspath('%s/%s/50-charging.svg' % (path,theme))
            self.full_charging_icon = os.path.abspath('%s/%s/99-full-charging.svg' % (path,theme))
        elif os.path.isdir('themes/%s' % theme):
            path = 'themes'
            self.null_icon = os.path.abspath('%s/%s/00-nocharging.svg' % (path,theme))
            self.caution_icon = os.path.abspath('%s/%s/01-caution.svg' % (path,theme))
            self.low_icon = os.path.abspath('%s/%s/05-low.svg' % (path,theme))
            self.good_icon = os.path.abspath('%s/%s/10-good.svg' % (path,theme))
            self.full_icon = os.path.abspath('%s/%s/15-full.svg' % (path,theme))
            self.charging_icon = os.path.abspath('%s/%s/50-charging.svg' % (path,theme))
            self.full_charging_icon = os.path.abspath('%s/%s/99-full-charging.svg' % (path,theme))
        else:
            print('Theme directory not found.')
            sys.exit()

        self.indicator = Indicator(self.null_icon)
        self.indicator.add_menu_item(lambda x: Gtk.main_quit(), "Quit")
        self.indicator.set_refresh(10000, self.check_battery)
        #self.indicator.icon.set_tooltip_text(subprocess.getoutput("acpi"))
        self.indicator.icon.set_has_tooltip(True)
        self.indicator.icon.connect("query-tooltip", self.tooltip_query)
        #self.indicator.add_menu_item(lambda x: self.indicator.set_icon(os.path.abspath('icon1.svg')),'New Icon')

    def check_battery(self):
        self.charging = False if subprocess.getoutput("cat /sys/class/power_supply/BAT0/status") == 'Discharging' else True
        percent = subprocess.getoutput("cat /sys/class/power_supply/BAT0/capacity")
        if not self.charging:
            if int(percent) > 70:
                self.indicator.set_icon(self.full_icon)
            elif int(percent) > 40:
                self.indicator.set_icon(self.good_icon)
            elif int(percent) > 10:
                self.indicator.set_icon(self.low_icon)
            elif int(percent) <= 10:
                self.indicator.set_icon(self.caution_icon)
        else:
            if int(percent) > 70:
                self.indicator.set_icon(self.full_charging_icon)
            else:
                self.indicator.set_icon(self.charging_icon)
        return True

    def tooltip_query(self, widget, x, y, keyboard_mode, tooltip):
        tooltip.set_text(subprocess.getoutput("acpi"))
        return True

if __name__ == '__main__':
    app = Application()
    Gtk.main()
