from __future__ import division
import wx
import numpy

class Tile(object):
	def __init__(self, parent, height, width, pixels_across, bgcolor=(0,0,0)):
		self.parent = parent

		self.height = height
		self.width = width
		self.pixels_across = pixels_across
		self.pixels_tall = self.pixels_across

		self.pixel_size = int(self.width/self.pixels_across)

		self.emptiness = True
		self.active = False

		self.pixel_array = numpy.zeros((self.pixels_across, self.pixels_tall, 3),'uint8')
		self.pixel_array[:,:] = bgcolor
		
		self.img = self.render()

		self.stat_bmp = self.get_static_bmp(1)



	def render(self):
		array = self.pixel_array_to_array(self.pixel_array)
		self.img = self.ArrayToImage(array)
		return self.img

	def pixel_array_to_array(self, pixel_array):
		array = numpy.zeros((int(self.height), int(self.width), 3),'uint8')
		for r in range(len(pixel_array)):
			row = pixel_array[r]
			y_min = r * self.pixel_size
			y_max = ((r+1) * self.pixel_size)
			for c in range(len(row)):
				color = pixel_array[r, c]
				x_min = c * self.pixel_size
				x_max = ((c+1) * self.pixel_size)

				for x in range(x_min, x_max):
					for y in range(y_min, y_max):
						array[x,y] = color
		return array

	def get_static_bmp(self, shrink_factor):
		scaled_img = self.img.ShrinkBy(shrink_factor, shrink_factor)
		bmp = scaled_img.ConvertToBitmap()
		return wx.StaticBitmap(self.parent, -1, bmp, (10, 5), (scaled_img.GetWidth(), scaled_img.GetHeight()))

	def ArrayToImage(self, array):
		height, width = len(array), len(array[0])
		image = wx.EmptyImage(width,height)
		image.SetData( array.tostring())
		return image

	def DrawBorder(self, array, color, bwidth):
		awidth = len(array[0])
		aheight = len(array)
		for y in range(aheight):
			for x in range(awidth):
				if x < bwidth or x > awidth - bwidth or y < bwidth or y > aheight - bwidth:
					array[y][x] = color

	# sets the pixel at specified coordinate to specified color
	def paint_pixel(self, x, y, rval,gval,bval):
		self.pixel_array[x][y] = (rval,gval,bval)

	def set_color(self, color):
		self.pixel_array[:,:] = color

	def randomize_pixels(self):
		for r in range(len(self.pixel_array)):
			for c in range(len(self.pixel_array[r])):
				self.pixel_array[r,c] = self.random_color()

	def randomize_type(self):
		x = numpy.random.uniform()

		if 0 <= x < 0.25:
			self.randomize_pixels()
		elif 0.25 <= x < 0.5:
			for n in range(5):
				if n<self.height and n<self.width:
					self.paint_pixel(n, n, (100,200,100))
		elif 0.5 <= x < 0.75:
			self.set_color((0,100,255))
		else:
			self.set_color((100,100,255))

	# draws a little red line
	def DrawTinyRedLine(self):
		for x in range(10):
			self.img.SetRGB(x, 10, 255,0,0)

	def random_color(self, color_ranges= [(0,255),(0,255),(220,221)]):
		rmin, rmax, gmin, gmax, bmin, bmax = color_ranges[0][0], color_ranges[0][1], color_ranges[1][0], color_ranges[1][1], color_ranges[2][0], color_ranges[2][1]
		return (numpy.random.uniform(rmin,rmax),numpy.random.uniform(gmin,gmax),numpy.random.uniform(bmin,bmax))


