#!/usr/bin/python
#
# Example application for the geo python module
#
# Copyright (C) 2010  Maximilian Hoegner <hp.maxi@hoegners.de>
#
# I grant anyone the right to use this work for any purpose, without
# any conditions, unless such conditions are required by law. There
# is no warranty.
#

import geo

import gtk
gtk.gdk.threads_init()

try:
	import osmgpsmap
	HAVE_MAP=True
except ImportError:
	HAVE_MAP=False

try:
	import geomag
	HAVE_GEOMAG=True
except ImportError:
	HAVE_GEOMAG=False

class Program(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)

		self.start_pos=None
		self.dest_pos=None

		table = gtk.Table()
		self.add(table)

		if HAVE_MAP:
			self.map = osmgpsmap.GpsMap()
			self.map.set_size_request(400,400)
			table.attach(self.map,0,1,0,1)
		else:
			maplabel = gtk.Label("Install python-osmgpsmap to display map.")
			maplabel.set_padding(10,10)
			table.attach(maplabel,0,1,0,1)

		controltable=gtk.Table()

		controltable.attach(gtk.Label("Start"),0,1,0,1)
		self.start=gtk.Entry()
		controltable.attach(self.start,1,2,0,1)
		startbtn=gtk.Button("Set")
		startbtn.connect("clicked", self.set_start)
		controltable.attach(startbtn,2,3,0,1)

		controltable.attach(gtk.Label("Destination"),0,1,1,2)
		self.dest=gtk.Entry()
		controltable.attach(self.dest,1,2,1,2)
		destbtn=gtk.Button("Set")
		destbtn.connect("clicked", self.set_dest)
		controltable.attach(destbtn,2,3,1,2)

		table.attach(controltable,0,1,1,2,0,0)

		table.attach(gtk.HSeparator(),0,1,2,3,gtk.FILL|gtk.EXPAND,0)

		self.data_start=gtk.Label()
		self.data_start.set_alignment(0,0)
		table.attach(self.data_start,0,1,3,4,gtk.FILL|gtk.EXPAND,0)

		self.data_dest=gtk.Label()
		self.data_dest.set_alignment(0,0)
		table.attach(self.data_dest,0,1,4,5,gtk.FILL|gtk.EXPAND,0)

		self.data_dist=gtk.Label("Set start point and destination...")
		self.data_dist.set_alignment(0,0)
		table.attach(self.data_dist,0,1,5,6,gtk.FILL|gtk.EXPAND,0)

		self.data_dir=gtk.Label()
		self.data_dir.set_alignment(0,0)
		table.attach(self.data_dir,0,1,6,7,gtk.FILL|gtk.EXPAND,0)

		self.connect("delete_event", gtk.main_quit)

		if not HAVE_GEOMAG:
			d = gtk.MessageDialog(type=gtk.MESSAGE_WARNING,buttons=gtk.BUTTONS_OK)
			d.set_markup("Install geomag (http://code.google.com/p/geomag/) to get declination compensated angles.")
			d.run()
			d.destroy()

	def set_start(self,*args):
		s=self.start.get_text()
		pos=geo.parse_position(s)
		if pos==None:
			d = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,buttons=gtk.BUTTONS_OK)
			d.set_markup("Invalid format.")
			d.run()
			d.destroy()
		else:
			if HAVE_MAP:
				self.map.draw_gps(pos[0],pos[1],0.)
			self.data_start.set_text("Start position: %f\xc2\xb0 N %f\xc2\xb0 E" % pos)
			self.start_lat,self.start_lon=pos
			self.start_pos=geo.xyz(*pos)
			self.update_data()

	def set_dest(self,*args):
		s=self.dest.get_text()
		pos=geo.parse_position(s)
		if pos==None:
			d = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,buttons=gtk.BUTTONS_OK)
			d.set_markup("Invalid format.")
			d.run()
			d.destroy()
		else:
			if HAVE_MAP:
				self.map.draw_gps(pos[0],pos[1],0.)
			self.data_dest.set_text("Destination: %f\xc2\xb0 N %f\xc2\xb0 E" % pos)
			self.dest_pos=geo.xyz(*pos)
			self.update_data()

	def update_data(self):
		if self.start_pos==None or self.dest_pos==None: return

		self.data_dist.set_text("Distance: %f km" % (geo.distance(self.start_pos,self.dest_pos)/1000.))

		if not self.start_pos==self.dest_pos:
			if HAVE_GEOMAG:
				true_north = geo.great_circle_angle(self.dest_pos,self.start_pos,geo.geographic_northpole)
				angle = geomag.mag_heading(true_north,dlat=self.start_lat,dlon=self.start_lon)
			else:
				angle = geo.great_circle_angle(self.dest_pos,self.start_pos,geo.magnetic_northpole)
				
			self.data_dir.set_text("Direction: %f\xc2\xb0 from north (%s)" % (angle, geo.direction_name(angle)))
		else:
			self.data_dir.set_text("Start point and destination is the same!")	

	def run(self):
		self.show_all()
		gtk.main()

if __name__=="__main__":
	prog = Program()
	prog.run()
