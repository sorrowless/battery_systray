Batticon
========

Description
-----------
Batticon is simple system tray widget that show battery status. Written with GTK 3.
To use, just place it where you want and start by running

``$ batticon``

Also you can install it from PyPi, for that just run

``$ pip install batticon``


Settings
--------
Settings file named *settings.json* and used standard JSON markup.
Today it have only two settings:

* theme that can be set by theme name
* timeout interval to update indicator.

Settings file can be placed in 3 places:

* program executable directory
* ~/.config/batticon/
* /etc/batticon/

Themes can be placed in:

* in *'themes'* directory where program lay
* ~/.config/batticon/themes/
* /usr/share/batticon/themes/


How to create new theme
-----------------------
You can create your own theme. It is very easy to do. All what you should do:

#. Create new directory and place it into themes one

#. Create 2 sets of icons - one set for charging battery and one for discharging battery. Actually, it can be equal set of icons, but it should have different names (*<battery_percent>-charging.<png|svg>* for charging and similar but with *'discharging'* instead 'charging' for discharging battery mode. You can place any number of icon for percent from 00 to 100 (it means that you can have 00,01,02...98,99,100 - full set of 101 icon for charging and 101 for discharging or you can just have 10,30,70,100 - set from 4 icon for charging and 4 for discharging; app will handle it right)

#. You should remember that all icons should be or svg or png format

#. Create icon with name *'default.<png|svg>'*

#. It's all - you can change name of theme to yours in settings and restart app

Your app doesn't work!!
-----------------------
Just write to me, don't be shy. I will really glad to help you with your problem.
Also, be cautious - program depends on pygobject for GTK3 and this package usually
distributed by OS itself. For example, it just doesn't work if I trying to
install it from pip in my Arch laptop, but works well if I install it from repos.



