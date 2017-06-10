from __future__ import division
import numpy
import wx
from tile import Tile


class WallToggler(wx.Panel):

	# takes width and height in squares
	def __init__(self, parent, current_tile):
		wx.Panel.__init__(self, parent)

		self.current_tile = current_tile

		self.mainsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.setSizer(self.mainsizer)

		self.cb_east = wx.CheckBox(self, label='East')
		self.cb_west = wx.CheckBox(self, label='West')
		self.cb_north = wx.CheckBox(self, label='North')
		self.cb_south = wx.CheckBox(self, label='South')

		self.mainsizer.Add(self.cb_east)
		self.mainsizer.Add(self.cb_west)
		self.mainsizer.Add(self.cb_north)
		self.mainsizer.Add(self.cb_south)

	def onClick(self, e):
		cb = e.GetEventObject()
		wallname = cb.GetLabel()
		self.current_tile.walls[wallname] = cb.GetValue()
		print self.current_tile.walls