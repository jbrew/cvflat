from __future__ import division
from room import Room
import numpy
import wx


# a grid of rooms width rooms across and height rooms high

class WorldMap(object):
	def __init__(self, parent, palette, width, height):
		self.room_grid = [[Room(self, parent, palette, width=800, height=500) for y in range(height)] for x in range(width)]
