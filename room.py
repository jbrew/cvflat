from __future__ import division
import numpy
import wx
from tile import Tile


class Room(object):

	# takes width and height in squares
	def __init__(self, parent, palette, width, height, tiles_across, tiles_tall):
		self.active = True

		self.tiles_across = tiles_across
		self.tiles_tall = tiles_tall
		self.tile_size = 50
		self.height = self.tiles_tall * self.tile_size
		self.width = self.tiles_across * self.tile_size

		self.palette = palette

		self.tile_matrix = [[Tile(parent, self.tile_size, self.tile_size, 10, bgcolor=(300,200,100)) for y in range(self.tiles_tall)] for x in range(self.tiles_across)]
		
		self.img = self.ArrayToImage(numpy.zeros( (self.height, self.width, 3),'uint8'))
		
		self.DrawTileMatrix()

# tile placement
#############################

	def PlaceTile(self, x, y, tile):
		self.tile_matrix[x][y] = tile
		
# image conversion juggling
###############################

	def ArrayToImage(self, array):
		height, width = len(array), len(array[0])
		image = wx.EmptyImage(width,height)
		image.SetData( array.tostring())
		return image

	# draws a tile into the array at the specified x and y position
	def DrawTile(self, xpos, ypos):
		t = self.tile_matrix[xpos][ypos]
		#print t.img.GetSize()
		tile_image = t.img
		for x in range(self.tile_size):
			for y in range(self.tile_size):
				self.img.SetRGB(x+xpos*self.tile_size, y+ypos*self.tile_size, tile_image.GetRed(x,y), tile_image.GetGreen(x,y), tile_image.GetBlue(x,y))

	def DrawTileMatrix(self):
		for x in range(self.tiles_across):
			for y in range(self.tiles_tall):
				self.DrawTile(x, y)

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
	def DrawImageAtPosition(self, img, xpos, ypos):

		tile = self.tile_matrix[xpos][ypos]
		tile_width, tile_height = self.tile_size, self.tile_size
		W = img.GetWidth()
		H = img.GetHeight()
		if W > H:
			NewW = self.tile_size
			NewH = self.tile_size * H / W
		else:
			NewH = self.tile_size
			NewW = self.tile_size * W / H
		img = img.Scale(NewW,NewH)

		img_width, img_height = img.GetSize()

		for x in range(img_width):
				for y in range(img_height):
					r,g,b = img.GetRed(x,y), img.GetGreen(x,y), img.GetBlue(x,y)
					if r+g+b > 0:
						self.img.SetRGB(x+xpos*self.tile_size, y+ypos*self.tile_size, r,g,b)


	# given an absolute coordinate, returns tile matrix coordinate
	def get_tile_coordinate(self, x_coord, y_coord):
		x = x_coord // self.tile_size
		y = y_coord // self.tile_size
		return x, y

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

	def SquareIsEmpty(self, xpos, ypos):
		if 0 <= xpos < self.tiles_across and 0 <= ypos < self.tiles_tall:
			t = self.tile_matrix[xpos][ypos]
			return t.emptiness




