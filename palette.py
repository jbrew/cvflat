from __future__ import division
import wx
import numpy
from tile import Tile

class Palette(wx.Panel):

	def __init__(self, parent, height, width, tiles_across, tiles_tall, full_tile_size):
		wx.Panel.__init__(self, parent)
		self.height = height
		self.width = width
		self.tiles_across = tiles_across
		self.tiles_tall = tiles_tall
		self.tile_size = full_tile_size
		self.shrunken_size = int(width / tiles_across)
		self.shrink_factor = self.tile_size / self.shrunken_size

		#wx.Panel.__init__(self, parent, size =(self.width, self.height))
		
		self.palSizer = wx.BoxSizer(wx.VERTICAL)

		self.active_index = (0,0)

		self.tile_matrix = [[Tile(self, self.tile_size, self.tile_size, 10, bgcolor=(0,0,100)) for y in range(self.tiles_tall)] for x in range(self.tiles_across)]

		self.img = self.ArrayToImage(numpy.zeros( (self.width, self.height,  3),'uint8'))

		blue_tile = Tile(self, self.tile_size, self.tile_size, 10, bgcolor = (0,100,250))
		
		green_tile = Tile(self, self.tile_size, self.tile_size, 10, bgcolor = (0,255,210))
		orange_tile = Tile(self, self.tile_size, self.tile_size, 10, bgcolor = (255,100,0))
		black_tile = Tile(self, self.tile_size, self.tile_size, 10, bgcolor = (0,0,0))
		orange_tile.emptiness = False

		self.tile_matrix[0][0] = blue_tile
		self.tile_matrix[0][1] = green_tile
		self.tile_matrix[1][0] = orange_tile
		self.tile_matrix[1][1] = black_tile


		self.refresh()

	def get_active(self):
		return self.tile_matrix[self.active_index[0]][self.active_index[1]]

# conversion to bitmap
###############################

	def ArrayToImage(self, array):
		height, width = len(array), len(array[0])
		image = wx.EmptyImage(width,height)
		image.SetData( array.tostring())
		return image

	def render(self):
		bmp = self.img.ConvertToBitmap()
		self.stat_bmp = wx.StaticBitmap(self, -1, bmp, (10, 5), (self.img.GetWidth(), self.img.GetHeight()))
		self.stat_bmp.Bind(wx.EVT_LEFT_UP, self.onClick)

	def refresh(self):
		for x in range(len(self.tile_matrix[0])):
			for y in range(len(self.tile_matrix[x])):
				self.DrawTile(x, y)
		self.DrawGrid(255,0,0)
		self.render()
		self.palSizer.Add(self.stat_bmp)


	# draws a tile into the array at the specified row and column
	def DrawTile(self, xpos, ypos):
		t = self.tile_matrix[xpos][ypos]
		tile_image = t.img.ShrinkBy(self.shrink_factor,self.shrink_factor)
		for x in range(tile_image.GetWidth()):
			for y in range(tile_image.GetHeight()):
				self.img.SetRGB(x+xpos*self.shrunken_size, y+ypos*self.shrunken_size, tile_image.GetRed(x,y), tile_image.GetGreen(x,y), tile_image.GetBlue(x,y))

	def DrawGrid(self, r, g, b):
		for yval in range(self.tile_size,self.height,self.tile_size):
			self.HorizontalLine(yval,1,r,g,b)
		for xval in range(self.tile_size,self.width,self.tile_size):
			self.VerticalLine(xval,1,0,100,100)

	def HorizontalLine(self, yval, linewidth, r, g, b):
		for x in range(self.width):
			for y in range(yval, yval+linewidth):
				self.img.SetRGB(x,y,r,g,b)
		
	def VerticalLine(self, xval, linewidth, r, g, b):
		for x in range(xval, xval+linewidth):
			for y in range(self.height):
				self.img.SetRGB(x,y,r,g,b)

	# given an absolute coordinate, returns tile matrix coordinate
	def get_tile_coordinate(self, y_coord, x_coord):
		xpos = x_coord // self.shrunken_size
		ypos = y_coord // self.shrunken_size
		return xpos, ypos

	def onClick(self, e):

		self.get_active().active = False
		self.get_active().render()

		x, y = e.GetPositionTuple()[0], e.GetPositionTuple()[1]
		xpos, ypos = self.get_tile_coordinate(y, x)

		self.active_index = (xpos,ypos)
		self.tile_matrix[xpos][ypos].active = True
		self.tile_matrix[xpos][ypos].render()

		
		self.refresh()