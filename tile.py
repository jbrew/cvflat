from __future__ import division
import numpy

class Tile(object):
	def __init__(self, pixel_size, pixels_across, pixels_tall, bgcolor=(0,0,0), ranges = [(0,255),(0,255),(220,221)]):
		self.pixel_size = pixel_size
		self.width = pixels_across
		self.height = pixels_tall
		self.array = numpy.zeros((self.height, self.width, 3),'uint8')
		self.array[:,:] = bgcolor
		self.random_pixels = False

		self.paint_pixel((0,0),(100,200,100))
		self.paint_pixel((1,1),(100,200,100))
		self.paint_pixel((2,2),(100,200,100))
		self.paint_pixel((3,3),(100,200,100))
		self.paint_pixel((4,4),(100,200,100))
		
		self.color_ranges = ranges

	# sets the pixel at specified coordinate to specified color
	def paint_pixel(self, coordinate, color):
		self.array[coordinate[1],coordinate[0]] = color

	def get_array(self):
		big_array = numpy.zeros((int(self.height*self.pixel_size), int(self.width*self.pixel_size), 3),'uint8')
		for row_index in range(len(self.array)):
			row = self.array[row_index]
			y_min = row_index * self.pixel_size
			y_max = ((row_index+1) * self.pixel_size)
			for pixel_index in range(len(row)):
				if self.random_pixels:
					color = self.random_color()
				else:
					color = self.array[row_index, pixel_index]
				x_min = pixel_index * self.pixel_size
				x_max = ((pixel_index+1) * self.pixel_size)

				for x in range(x_min, x_max):
					for y in range(y_min, y_max):
						big_array[y,x] = color
		return big_array

	def random_color(self):
		rmin, rmax, gmin, gmax, bmin, bmax = self.color_ranges[0][0], self.color_ranges[0][1], self.color_ranges[1][0], self.color_ranges[1][1], self.color_ranges[2][0], self.color_ranges[2][1]
		return (numpy.random.uniform(rmin,rmax),numpy.random.uniform(gmin,gmax),numpy.random.uniform(bmin,bmax))


