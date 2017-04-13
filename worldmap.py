from __future__ import division
import numpy
import wx
from tile import Tile


class WorldMap(wx.Panel):

	# takes width and height in squares
	def __init__(self, parent, palette, height, width):
		wx.Panel.__init__(self, parent)
		self.height = height
		self.width = width
		self.tiles_across = 8

		self.tile_size = int(self.width / self.tiles_across)
		self.tiles_tall = int(self.height / self.tile_size)

		self.wmSizer = wx.BoxSizer(wx.VERTICAL)

		self.palette = palette

		self.tile_matrix = [[Tile(self, self.tile_size, self.tile_size, 10, bgcolor=(0,0,100)) for x in range(self.tiles_across)] for y in range(self.tiles_tall)]
		
		self.img = self.ArrayToImage(numpy.zeros( (self.height, self.width, 3),'uint8'))
		
		self.TileMatrixToImage()

		self.refresh()

# tile placement
#############################

	def PlaceTile(self, r, c, tile):
		self.tile_matrix[r][c] = tile
		
# image conversion juggling
###############################

	def ArrayToImage(self, array):
		height, width = len(array), len(array[0])
		image = wx.EmptyImage(width,height)
		image.SetData( array.tostring())
		return image

	# draws a tile into the array at the specified row and column
	def DrawTile(self, row, col):
		t = self.tile_matrix[row][col]
		tile_image = t.img
		for x in range(tile_image.GetWidth()):
			for y in range(tile_image.GetHeight()):
				self.img.SetRGB(x+col*self.tile_size, y+row*self.tile_size, tile_image.GetRed(x,y), tile_image.GetGreen(x,y), tile_image.GetBlue(x,y))

	def TileMatrixToImage(self):
		for r in range(self.tiles_tall):
			for c in range(self.tiles_across):
				self.DrawTile(r, c)


	def render(self):
		self.bmp = self.img.ConvertToBitmap()
		self.stat_bmp = wx.StaticBitmap(self, -1, self.bmp, (10, 5), (self.img.GetWidth(), self.img.GetHeight()))
		self.stat_bmp.Bind(wx.EVT_LEFT_UP, self.onClick)
		self.wmSizer.Clear()
		self.wmSizer.Add(self.stat_bmp)

# wx window communication methods
####################################################

	def refresh(self):
		#self.DrawLattice(255,0,0)
		self.render()

	def onClick(self, e):
		y, x = e.GetPositionTuple()[0], e.GetPositionTuple()[1]
		row, col = self.get_tile_coordinate(x, y)
		self.PlaceTile(row, col, self.palette.get_active())
		self.DrawTile(row,col)
		self.refresh()

# draw methods
##############################################

	def HorizontalLine(self, yval, linewidth, r, g, b):
		for x in range(self.width):
			for y in range(yval, yval+linewidth):
				self.img.SetRGB(x,y,r,g,b)
		
	def VerticalLine(self, xval, linewidth, r, g, b):
		for x in range(xval, xval+linewidth):
			for y in range(self.height):
				self.img.SetRGB(x,y,r,g,b)

	def DrawLattice(self, r, g, b):
		for yval in range(self.tile_size,self.height,self.tile_size):
			self.HorizontalLine(yval,1,r,g,b)
		for xval in range(self.tile_size,self.width,self.tile_size):
			self.VerticalLine(xval,1,0,100,100)

	# given an image, draws it in at the corresponding position
	def DrawImageAtPosition(self, img, row, col):

		tile = self.tile_matrix[row][col]
		tile_width, tile_height = self.tile_size, self.tile_size
		img_width, img_height = img.GetSize()

		if img_width > tile_width and img_height > tile_height:
			img = img.ShrinkBy(img_width/tile_width, img_height/tile_height)

		img_width, img_height = img.GetSize()

		for x in range(img_width):
				for y in range(img_height):
					r,g,b = img.GetRed(x,y), img.GetGreen(x,y), img.GetBlue(x,y)
					if r+g+b > 0:
						self.img.SetRGB(x+col*self.tile_size, y+row*self.tile_size, r,g,b)

		"""
		if shrink_to_fit:
			for x in range(img_width):
				proportional_x = numpy.floor(x / img_width * tile_width)
				for y in range(img_height):
					proportional_y = numpy.floor(y / img_height * tile_height)
					r,g,b = img.GetRed(x,y), img.GetGreen(x,y), img.GetBlue(x,y)
					if r+g+b > 0:
						self.img.SetRGB(proportional_x+col*self.tile_size, proportional_y+row*self.tile_size, r,g,b)
		else:
			for x in range(tile_width):
				for y in range(tile_height):
					r,g,b = img.GetRed(x,y), img.GetGreen(x,y), img.GetBlue(x,y)
					self.img.SetRGB(x+col*self.tile_size, y+row*self.tile_size, r,g,b)
		"""



	# given an absolute coordinate, returns tile matrix coordinate
	def get_tile_coordinate(self, y_coord, x_coord):
		r = y_coord // self.tile_size
		c = x_coord // self.tile_size
		return r, c

	def center_of_tile(self, x, y):
		return (x + 0.5) * self.tile_size, (y+ 0.5) * self.tile_size

	def get_tile(self, coordinate):
		return self.tile_matrix[coordinate[0]][coordinate[1]]

	def GetScreen(self, x, y, width, height):
		rect = wx.Rect(x-width/2, y-height/2, width, height)
		return self.GetSub(self.img, rect)
		#return self.img.GetSubImage(rect)

	def GetSub(self, img, rect):
		new_img = wx.EmptyImage(rect.width, rect.height)
		for x in range(rect.x, rect.x + rect.width):
			for y in range(rect.y, rect.y + rect.height):
				new_img.SetRGB(x-rect.x, y-rect.y, img.GetRed(x,y), img.GetGreen(x,y), img.GetBlue(x,y))
		return new_img

	def SquareIsEmpty(self, r, c):
		if 0 <= r < self.tiles_tall and 0 <= c < self.tiles_across:
			t = self.tile_matrix[r][c]
			return t.emptiness




