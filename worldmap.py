from __future__ import division
from room import Room
import numpy
import wx


# a grid of rooms width rooms across and height rooms high

class Worldmap(object):
	def __init__(self, parent, palette, width, height, tiles_per_axis):
		self.rooms_across = width
		self.rooms_tall = height
		self.room_grid = [[Room(parent, palette, width=800, height=500, tiles_across=tiles_per_axis, tiles_tall=tiles_per_axis) for y in range(self.rooms_tall)] for x in range(self.rooms_across)]


	def get_room(self, x, y):
		return self.room_grid[x][y]
