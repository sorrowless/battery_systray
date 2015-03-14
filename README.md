Simple system tray widget that show battery status. Written with GTK 3.
To use, just place it where you want and start.
Themes can be placed in:
~/.config/batticon/themes/
/usr/share/batticon/themes/
or in 'themes' directory where program lay.

Also can be placed config file, but it is also can be in:
/etc/

In settings file you can set a theme by theme name and timeout interval to
update indicator.

You can create your own theme. It is very easy to so. You should just remember
about next things:

1. All your icons should be or svg or png format.
2. You should have icon with name 'default.<png|svg>'
3. You should create 2 sets of icons - one set for charging battery and one for
discharging battery. Actually, it can be equal set of icons, but it should have
different names (<battery_percent>-charging.<png|svg> for charging and similar
but with 'discharging' instead 'charging' for discharging battery mode.
