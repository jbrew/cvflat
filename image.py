from __future__ import division
import numpy
from tile import Tile

class Image(object):

	def __init__(self, width, height, tiles_across=8, tiles_tall=5):

		self.width = width
		self.height = height

		self.tiles_across = tiles_across
		self.tiles_tall = tiles_tall

		self.tile_size = 100

		self.canvas = self.BlankArray(self.width, self.height)

		self.DrawPinkCircles(2)

	# creates a variegated color grid
	def RandomSquares(self):
		for r in range(self.tiles_tall):
			for c in range(self.tiles_across):
				if numpy.random.uniform() > 0:
					rmin = numpy.random.uniform(110,170)
					rmax = rmin + 60*numpy.random.normal()
					gmin = numpy.random.uniform(110,170)
					gmax = gmin + 60*numpy.random.normal()
					bmin = numpy.random.uniform(110,160)
					bmax = bmin + 60*numpy.random.normal()
					t = Tile(self.pixel_size, self.resolution, bgcolor = (255,255,255), ranges = [(rmin,rmax),(gmin,gmax),(bmin,bmax)])
					big_t = t.get_array()
					self.DrawTile(self.top_l_position((r,c)), big_t)


	def BlankArray(self, width, height, bgcolor = (0,0,0)):
		array = numpy.zeros( (height, width, 3),'uint8')
		array[:,:] = bgcolor
		return array

	# returns pixel of top left corner of specified tile
	def get_position(self, row_index, col_index):
		return (row_index * self.tile_size, col_index * self.tile_size)

	# given a position, return the tile index
	def get_tile(self, y_coord, x_coord):
		ypos = y_coord // self.tile_size
		xpos = x_coord // self.tile_size
		return ypos, xpos

	# true if coordinate is in array
	def IsInArray(self, coordinate, array):
		xval, yval = coordinate[0], coordinate[1]
		width, height = len(array), len(array[0])
		return xval in range(width) and yval in range(height)

	# draws a tile into the array with the top left corner at the specified position
	def DrawTile(self, row_index, col_index, tile):
		y = row_index * self.tile_size
		x = col_index * self.tile_size
		self.get_position(row_index, col_index)
		height, width = len(tile), len(tile[0])
		for r in range(height):
			for c in range(width):
				self.canvas[y+c,x+r] = tile[r,c]

	# modifies an array
	def DrawCircle(self, r, array, position, linewidth, color):
		height, width = 2*r, 2*r
		center = position
		for x in range(int(center[0]-r-linewidth), int(center[0]+r+linewidth)):
			for y in range(int(center[1]-r-linewidth), int(center[1]+r+linewidth)):
				distance = numpy.sqrt((x-center[0])*(x-center[0]) + (y-center[1])*(y-center[1]))
				if numpy.absolute(distance - (r-5)) <= linewidth/2:
					if self.IsInArray((x,y),array):
						array[x,y] = color
		return array

	# draws the specified number of pink circles at random places on the image
	def DrawPinkCircles(self, num_pink_circles):
		num_circles = 2

		positions = [(numpy.random.uniform()*self.height, numpy.random.uniform()*self.width) for x in range(num_circles)]
		
		for p in positions:
			self.DrawCircle(40, self.canvas, position = p, linewidth = 2.5, color = (200,100,100))


	def DrawGrid(self, color):

		# horizontal lines
		for y_tiles in range(self.tiles_tall+1):
			for x_pixels in range(self.width):
				self.canvas[y_tiles*self.tile_size, x_pixels] = color

		# vertical lines
		for x_tiles in range(self.tiles_across+1):
			for y_pixels in range(self.height):
				self.canvas[y_pixels, x_tiles*self.tile_size] = color



