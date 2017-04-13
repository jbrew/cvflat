from __future__ import division
import numpy
import os
import wx


class Slide(object):

	def __init__(self, slide_id, map_wximage, cvname):
		self.slide_id = slide_id
		self.title = ''
		self.text = ''
		self.options =[]
		image_dir = cvname + '_images'
		if not os.path.exists(image_dir):
			os.makedirs(image_dir)
		self.imagepath = '%s/%s' % (image_dir, self.slide_id)
		map_wximage.SaveFile(self.imagepath, wx.BITMAP_TYPE_PNG)






