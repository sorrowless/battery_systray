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

		#self.set_refresh(10000, self.set_icon, os.path.abspath('icon1.svg'))
		#GObject.timeout_add(10000, self.set_icon, os.path.abspath('icon1.svg'))

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
		#self.get_tray_menu()

		def pos(menu, aicon):
			return (Gtk.StatusIcon.position_menu(menu, aicon))

		self.menu.popup(None, None, pos, icon, button, time)


class Application:
	def __init__(self):
		settings = json.load(open('settings.json','r'))
		theme = settings['theme']['themeName']
		self.null_icon = os.path.abspath('themes/%s/00-nocharging.svg' % theme)
		self.caution_icon = os.path.abspath('themes/%s/01-caution.svg' % theme)
		self.low_icon = os.path.abspath('themes/%s/05-low.svg' % theme)
		self.good_icon = os.path.abspath('themes/%s/10-good.svg' % theme)
		self.full_icon = os.path.abspath('themes/%s/15-full.svg' % theme)
		self.charging_icon = os.path.abspath('themes/%s/50-charging.svg' % theme)
		self.full_charging_icon = os.path.abspath('themes/%s/99-full-charging.svg' % theme)

		self.indicator = Indicator(self.null_icon)
		self.indicator.add_menu_item(lambda x: Gtk.main_quit(), "Quit")
		self.indicator.set_refresh(10000, self.check_battery)
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

if __name__ == '__main__':
	app = Application()
	Gtk.main()