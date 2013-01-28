#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gtk
import appindicator
import urllib2

from xml.dom.minidom import parseString

# The main class
# This is the root class that contains
# all of the core logic for StarIndicator
class starindicator:
	
	# Our constructor
	def __init__ (self):
		# Create an AppIndicator
		self.ind = appindicator.Indicator ("star-indicator", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
		self.ind.set_status (appindicator.STATUS_ACTIVE)
		
		self.ind.set_icon_theme_path("/home/baptiste/Sources")
		self.ind.set_icon("bus")
		
		self.fetch_data()
		self.create_menu()
 
	# Creates the menu for the application
	def create_menu(self):
		# create a menu
		menu = gtk.Menu()
		
		i = 0
		for stopline in self.dom.getElementsByTagName('stopline'):
			for route in stopline.getElementsByTagName('route'):
				if i!=0:
					menu_items = gtk.SeparatorMenuItem()
					menu.append(menu_items)
					menu_items.show()
				bus = route.firstChild.data
				i+=1
				j = 0
				for departure in stopline.getElementsByTagName('departure'):
					time = departure.firstChild.data[11:-9]
					img = gtk.Image()
					# get a clean bus number
					if bus[-1:] == '0':
						if j == 0:
							bus = bus[2:]
					else:
						bus = bus.replace('0','')
					img.set_from_file("/home/baptiste/Sources/Pictogrammes_21/" + bus + ".png")
					j += 1
					print j
					#print "/home/baptiste/Sources/Pictogrammes_21/" + bus + ".png"
					menu_items = gtk.ImageMenuItem(time)
					#menu_items.set_sensitive(False)
					menu_items.set_always_show_image(True)
					menu_items.set_image(img)
					menu.append(menu_items)
					menu_items.show()
		menu_items.show()
		
		sep = gtk.SeparatorMenuItem()
		menu.append(sep)
		sep.show()
		refresh = gtk.MenuItem("Rafraichir")
		refresh.connect("activate", self.update)
		menu.append(refresh)
		refresh.show()
		quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		quit.connect("activate", gtk.main_quit)
		menu.append(quit)
		quit.show()
		
		self.ind.set_menu(menu)

	# fetch data from Keolis
	def fetch_data(self):
		#download xml from Keolis :
		xml = urllib2.urlopen('http://data.keolis-rennes.com/xml/?cmd=getbusnextdepartures&version=2.1&key=HWXEIBF8HJPVPHE&param[mode]=stop&param[direction][]=1&param[stop][]=1168')
		#filesystem testing
		#xml = open('/home/baptiste/Sources/data2.xml')
		#convert to string:
		data = xml.read()
		#close file because we dont need it anymore:
		xml.close()
		
		#parse the xml you downloaded
		self.dom = parseString(data)
	
	# update menu
	def update(self, widget):
		# update menu
		self.fetch_data()
		self.create_menu()

# Create the primary instance and
# enter the main GTK loop
if __name__ == "__main__":
	instance = starindicator()
	gtk.main()
	
