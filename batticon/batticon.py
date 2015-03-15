#!/usr/bin/env python
"""
This module defining classes to create system tray indicator and application based on it.
Class Indicator can be easily reused in any other project.
Class Application implements main logic of battery system tray indicator.
"""
from gi.repository import Gtk, GObject

import sys
import subprocess
import os
import json
import re

class Indicator:
    """
    This class defining standard GTK3 system tray indicator.
    """
    def __init__(self, icon):
        """
        Args:
          icon (str): path to initial icon that will be shown on system panel
        """
        self.appicon = icon
        self.icon = Gtk.StatusIcon()
        self.icon.set_from_file(self.appicon)

        self.menu = Gtk.Menu()
        self.icon.connect('popup-menu', self.right_click_event_statusicon)

    def set_refresh(self, timeout, callback, *callback_args):
        """
        It is just stub for simplify setting timeout.
        Args:
          timeout (int): timeout in milliseconds, after which callback will be called
          callback (callable): usually, just a function that will be called each time after timeout
          *callback_args (any type): arguments that will be passed to callback function
        """
        GObject.timeout_add(timeout, callback, *callback_args)

    def set_icon(self, icon):
        """
        Set new icon in system tray.
        Args:
          icon (str): path to file with new icon
        """
        self.icon.set_from_file(icon)

    def add_menu_item(self, command, title):
        """
        Add mouse right click menu item.
        Args:
          command (callable): function that will be called after left mouse click on title
          title (str): label that will be shown in menu
        """
        m_item = Gtk.MenuItem()
        m_item.set_label(title)
        m_item.connect('activate', command)
        self.menu.append(m_item)
        self.menu.show_all()

    def add_seperator(self):
        """
        Add separator between labels in menu that called on right mouse click.
        """
        m_item = Gtk.SeparatorMenuItem()
        self.menu.append(m_item)
        self.menu.show_all()

    def right_click_event_statusicon(self, icon, button, time):
        """
        It's just way how popup menu works in GTK. Don't ask me how it works.
        """

        def pos(menu, aicon):
            """Just return menu"""
            return Gtk.StatusIcon.position_menu(menu, aicon)

        self.menu.popup(None, None, pos, icon, button, time)


class Application:
    """
    This class implements logic of battery system indicator itself.
    """
    def __init__(self):
        if os.path.isfile('settings.json'):
            settings = json.load(open('settings.json', 'r'))
        elif os.path.isfile('%s/.config/batticon/settings.json' % os.getenv('HOME')):
            settings = json.load(open('%s/.config/batticon/settings.json' % os.getenv('HOME'), 'r'))
        elif os.path.isfile('/etc/batticon/settings.json'):
            settings = json.load(open('/etc/batticon/settings.json', 'r'))
        else:
            print('Settings file not found.')
            sys.exit()

        theme = settings['theme']['themeName']
        if os.path.isdir('themes/%s' % theme):
            path = os.path.abspath('themes/%s' % theme)
        elif os.path.isdir('%s/.config/batticon/themes/%s' % (os.getenv('HOME'), theme)):
            path = os.path.abspath('%s/.config/batticon/themes/%s' % (os.getenv('HOME'), theme))
        elif os.path.isdir('/usr/share/batticon/themes/%s' % theme):
            path = os.path.abspath('/usr/share/batticon/themes/%s' % theme)
        else:
            print('Theme directory not found.')
            sys.exit()

        self.chlist = []
        self.dischlist = []
        regex = re.compile(r'(?P<val>\d\d\d)-(?P<stat>charging|discharging)\.(?P<ext>png|svg)')
        # it's a bad idea, but right now I cannot do any else
        ext = ''
        for file in os.listdir(path):
            answer = regex.match(file)
            if ((file.endswith('-charging.png') or file.endswith('-charging.svg')) and
                    answer.group('val')):
                self.chlist.append(answer.group('val'))
            elif ((file.endswith('-discharging.png') or file.endswith('-discharging.svg')) and
                  answer.group('val')):
                self.dischlist.append(answer.group('val'))
            if ((file.endswith('-discharging.png') or file.endswith('-discharging.svg')) and
                    answer.group('ext')):
                ext = answer.group('ext')
        self.chlist.sort()
        self.dischlist.sort()
        print(self.dischlist)
        self.deficon = path + '/default.' + ext
        self.chformat = path + '/{value}-charging.' + ext
        self.dischformat = path + '/{value}-discharging.' + ext

        self.indicator = Indicator(self.deficon)
        self.indicator.add_menu_item(lambda x: Gtk.main_quit(), "Quit")
        refresh_timeout = int(settings['common']['refresh_timeout'])
        if not refresh_timeout or refresh_timeout < 1000:
            refresh_timeout = 1000
        self.indicator.set_refresh(refresh_timeout, self.check_battery)
        self.indicator.icon.set_has_tooltip(True)
        self.indicator.icon.connect("query-tooltip", self.tooltip_query)

    def check_battery(self):
        """
        Implement how we will check battery condition. Now it just trying to check standard battery
        in /sys
        """
        self.charging = False if \
            subprocess.getoutput("cat /sys/class/power_supply/BAT0/status") == 'Discharging' \
            else True
        percent = subprocess.getoutput("cat /sys/class/power_supply/BAT0/capacity")
        if not self.charging:
            for val in self.dischlist:
                if int(percent) <= int(val):
                    self.indicator.set_icon(self.dischformat.format(value=val))
                    break
        else:
            for val in self.chlist:
                if int(percent) <= int(val):
                    self.indicator.set_icon(self.chformat.format(value=val))
                    break
        return True

    def tooltip_query(self, widget, x, y, keyboard_mode, tooltip):
        """
        Set tooltip which appears when you hover mouse curson onto icon in system panel.
        """
        tooltip.set_text(subprocess.getoutput("acpi"))
        return True

def main():
    """Helper function. I'm using it in console_entrypoint to easy call program from cli or gui."""
    Application()
    Gtk.main()

if __name__ == '__main__':
    main()
