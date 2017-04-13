from __future__ import division
import wx
import numpy

class Tile(wx.Panel):
	def __init__(self, parent, pixel_size, pixels_tall, pixels_across, bgcolor=(0,0,0)):
		wx.Panel.__init__(self, parent, size = (pixels_tall*pixel_size,pixels_across*pixel_size))
		
		self.pixel_size = pixel_size
		self.height = pixels_tall
		self.width = pixels_across

		self.full = True
		self.active = False

		self.pixel_array = numpy.zeros((self.height, self.width, 3),'uint8')
		self.pixel_array[:,:] = bgcolor
		
		self.big_array = numpy.zeros((int(self.height*self.pixel_size), int(self.width*self.pixel_size), 3),'uint8')

		self.render(self.big_array)

	# sets the pixel at specified coordinate to specified color
	def paint_pixel(self, r, c, color):
		self.pixel_array[r][c] = color

	def set_color(self, color):
		self.pixel_array[:,:] = color
		self.render(self.big_array)

	def randomize_pixels(self):
		for r in range(len(self.pixel_array)):
			for c in range(len(self.pixel_array[r])):
				self.pixel_array[r,c] = self.random_color()
		self.render(self.big_array)

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

		self.render(self.big_array)

	def render(self, target_array):
		for r in range(len(self.pixel_array)):
			row = self.pixel_array[r]
			y_min = r * self.pixel_size
			y_max = ((r+1) * self.pixel_size)
			for c in range(len(row)):
				color = self.pixel_array[r, c]
				x_min = c * self.pixel_size
				x_max = ((c+1) * self.pixel_size)

				for x in range(x_min, x_max):
					for y in range(y_min, y_max):
						target_array[y,x] = color

	def get_palette_array(self):
		big_array = numpy.zeros((int(self.height*self.pixel_size), int(self.width*self.pixel_size), 3),'uint8')
		self.render(big_array)
		if self.active:
			self.DrawBorder(big_array, (250,250,50), 4)
		return big_array

	# draws the protagonist in this tile
	def MrCircle(self):
		self.pixel_array[:,:] = (100,200,200)
		self.render(self.big_array)


	def get_array(self):
		big_array = numpy.zeros((int(self.height*self.pixel_size), int(self.width*self.pixel_size), 3),'uint8')
		self.render(big_array)
		return big_array

	def DrawBorder(self, array, color, bwidth):
		awidth = len(array[0])
		aheight = len(array)
		for y in range(aheight):
			for x in range(awidth):
				if x < bwidth or x > awidth - bwidth or y < bwidth or y > aheight - bwidth:
					array[y][x] = color

	def random_color(self, color_ranges= [(0,255),(0,255),(220,221)]):
		rmin, rmax, gmin, gmax, bmin, bmax = color_ranges[0][0], color_ranges[0][1], color_ranges[1][0], color_ranges[1][1], color_ranges[2][0], color_ranges[2][1]
		return (numpy.random.uniform(rmin,rmax),numpy.random.uniform(gmin,gmax),numpy.random.uniform(bmin,bmax))


