from __future__ import division
import numpy
from tile import Tile
from image import Image


class WorldMap(object):

	# takes width and height in squares
	def __init__(self, tiles_across, tiles_tall, tile_size):

		self.tiles_across = tiles_across
		self.tiles_tall = tiles_tall

		self.tile_size = tile_size

		self.wmap = [[self.new_tile() for x in range(self.tiles_across)] for y in range(self.tiles_tall)]

	def new_tile(self):
		return Tile(pixel_size = 5, pixels_across = 20, pixels_tall = 20)

	def place_tile(self, tile, xpos, ypos):
		self.map[xpos,ypos] = tile

	def to_image(self, xmin=0, xmax=1, ymin=0, ymax=1):
		width_in_tiles = xmax - xmin
		width_in_pixels = self.tile_size * width_in_tiles

		height_in_tiles = ymax - ymin
		height_in_pixels = self.tile_size * height_in_tiles

		img = Image(width = width_in_pixels+1, height = height_in_pixels+1, tiles_across = width_in_tiles, tiles_tall = height_in_tiles)
		
		
		for r in range(self.tiles_tall):
			for c in range(self.tiles_across):
				img.DrawTile(r, c, self.wmap[r][c].get_array())


		img.DrawGrid((255,255,255))
		return img

