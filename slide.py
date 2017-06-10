from __future__ import division
from collections import OrderedDict
import json
import numpy
import os
import wx


class Slide(object):

	def __init__(self, slide_id, image, image_dir):
		self.slide_id = slide_id
		self.image = image
		self.image_dir = image_dir
		self.title = ''
		self.text = ''
		self.choices = []
		self.finish = False
		self.shareable = False
		self.start = False
		self.link_style = u'action'
		self.save_to_file()

	def save_to_file(self):
		if not os.path.exists(self.image_dir):
			os.makedirs(self.image_dir)
		self.image_path = '%s/%s' % (self.image_dir, self.slide_id)
		self.image.SaveFile(self.image_path, wx.BITMAP_TYPE_PNG)

	def get_links(self):
		return [{u'body': choice[0], 
		u'float': False, 
		u'from_node': self.slide_id, 
		u'link_style': u'action', 
		u'order': None, 
		u'to_node': choice[1], 
		u'transition': u''} for choice in self.choices]

	def to_json(self):
		ordered = json.dumps(OrderedDict([(u'body', self.text),
		(u'finish', self.finish), 
		(u'id', self.slide_id), 
		(u'link_style', u'action'), 
		(u'links', self.get_links()),
		(u'photo_description', u''),
		(u'photo_final', {u'alt': None, u'caption': None, u'id': 0}),
		(u'photo_note', u''),
		(u'photo_placeholder_page_url', None),
		(u'photo_placeholder_url', self.image_path),
		(u'share_text', u''),
		(u'shareable', self.shareable),
		(u'sister_pages', []),
		(u'start', self.start),
		(u'statuses', {u'photo': u'Image ready'}),
		(u'title', self.title)]))
		return ordered





