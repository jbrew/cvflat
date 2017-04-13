from __future__ import division
import numpy
from tile import Tile

class Image(object):

	def __init__(self, height=0, width=0):

		self.height = height
		self.width = width

		self.canvas = self.BlankArray(self.width, self.height)


	def BlankArray(self, width, height, bgcolor = (0,0,0)):
		array = numpy.zeros( (height, width, 3),'uint8')
		array[:,:] = bgcolor
		return array







