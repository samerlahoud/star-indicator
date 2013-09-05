#### Webapp that indicates the next rounds of Rennes STAR bus lines at "Tournebride" towards "Republique"
#### Deployed on http://bus-tournebride.appspot.com/
#### Can be added as a bookmark or a quick launch app on smartphones, PCs, ...
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import webapp2
from datetime import datetime
from xml.dom.minidom import parseString
#from google.appengine.api import urlfetch
import codecs
import sys
import urllib2

class MainHandler(webapp2.RequestHandler):

  def get(self):
    # Download xml from Keolis :
    keolis_url = 'http://data.keolis-rennes.com/xml/?cmd=getbusnextdepartures&version=2.1&key=UQ24KM4DB4U8E4O&param[mode]=stop&param[direction][]=1&param[stop][]=1160'
    #xml_response = urlfetch.fetch(keolis_url, deadline=60)
    #xml = xml.response
    try:
    	xml_response = urllib2.urlopen(keolis_url, timeout=120)
    	xml = xml_response.read()
    except urllib2.URLError, e:
    	handleError(e)
    	
    dom = parseString(xml)
    
    #Get the Star time from the data tag in XML 
    data_tag = dom.getElementsByTagName('data')
    star_time = data_tag[0].attributes["localdatetime"].value[11:-9]
    
    self.response.write("<h3>Il est %s &agrave; Beaulieu Tournebride</h3>" %star_time)
	
	# Navigate through bus lines (stopline) and rounds (route)
    for stopline in dom.getElementsByTagName('stopline'):
      for route in stopline.getElementsByTagName('route'):
		bus = route.firstChild.data
		j = 0
		for departure in stopline.getElementsByTagName('departure'):
			bus_time = departure.firstChild.data[11:-9]
			# Get a clean bus number
			if bus[-1:] == '0':
				if j == 0:
					bus = bus[2:]
			else:
				bus = bus.replace('0','')
			j += 1
			
			# Get the time delta and the destination headsign
			time_to_run = datetime.strptime(bus_time, "%H:%M") - datetime.strptime(star_time, "%H:%M")
			destination = departure.attributes["headsign"].value
			accuracy = departure.attributes["accurate"].value
			self.response.write("<h4>L%s vers %s &agrave; %s -- dans %s min %s</h4>" %(bus, destination, bus_time, int(time_to_run.total_seconds()/60), "*" if accuracy == "1" else ""))
            
app = webapp2.WSGIApplication([
  ('/.*', MainHandler),
], debug=True)

