from __future__ import division
import numpy
import wx
from tile import Tile


class DisplayWindow(wx.Panel):

	# takes width and height in squares
	def __init__(self, parent, height, width, current_room):
		wx.Panel.__init__(self, parent)
		self.height = height
		self.width = width
		self.current_room = current_room

		self.wmSizer = wx.BoxSizer(wx.VERTICAL)

		self.img = self.current_room.ArrayToImage(numpy.zeros( (self.height, self.width, 3),'uint8'))
		self.current_mouse_position = (0,0)

		self.refresh()

# wx window communication methods
####################################################

	def refresh(self):
		self.img = self.current_room.img
		self.bmp = self.img.ConvertToBitmap()
		self.stat_bmp = wx.StaticBitmap(self, -1, self.bmp, (10, 5), (self.img.GetWidth(), self.img.GetHeight()))
		self.stat_bmp.Bind(wx.EVT_LEFT_UP, self.onClick)
		self.stat_bmp.Bind(wx.EVT_MOTION, self.onMotion)
		self.wmSizer.Clear()
		self.wmSizer.Add(self.stat_bmp)

	def onClick(self, e):
		x, y = e.GetPositionTuple()[0], e.GetPositionTuple()[1]
		xpos, ypos = self.current_room.get_tile_coordinate(x, y)
		self.current_room.PlaceTile(xpos, ypos, self.current_room.palette.get_active())
		self.current_room.DrawTile(xpos,ypos)
		self.refresh()

	def onMotion(self, e):
		x, y = e.GetPositionTuple()[0], e.GetPositionTuple()[1]
		xpos, ypos = self.current_room.get_tile_coordinate(x, y)
		if not (xpos, ypos) == self.current_mouse_position:
			self.current_mouse_position = (xpos, ypos)
			if e.LeftIsDown():
				self.current_room.PlaceTile(xpos, ypos, self.current_room.palette.get_active())
				self.current_room.DrawTile(xpos,ypos)
				self.refresh()

	def set_current_room(self, room):
		self.current_room = room




