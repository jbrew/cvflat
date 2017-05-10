from __future__ import division
import numpy
import os
import wx

class Viewer(object):

	def __init__(self, parent, slide_list):
		self.slides = slide_list
		self.frame = wx.Frame(None, title='Viewer')
		self.frame.Show()
		self.panel = wx.Panel(self.frame)
		self.PhotoMaxSize = 240
		self.createWidgets()
		self.loadimage(0)

	def loadimage(self, slide_id):
		self.mainSizer.Clear()
		current_slide = self.slides[slide_id]
		filepath = current_slide.imagepath
		img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
		W = img.GetWidth()
		H = img.GetHeight()
		if W > H:
			NewW = self.PhotoMaxSize
			NewH = self.PhotoMaxSize * H / W
		else:
			NewH = self.PhotoMaxSize
			NewW = self.PhotoMaxSize * W / H
		img = img.Scale(NewW,NewH)
		self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
		self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
		self.buttonSizer = wx.BoxSizer(wx.VERTICAL)
		self.buttonSizer.Clear()
		for choice in current_slide.choices:
			choice_text, target_id = choice[0], choice[1]
			print choice_text
			cbutton = wx.Button(self.panel, label=choice_text)
			cbutton.Bind(wx.EVT_LEFT_UP, lambda event, target_id = target_id: self.onChoice(event, target_id))
			self.buttonSizer.Add(cbutton)
		self.mainSizer.Add(self.buttonSizer)
		self.panel.Layout()
		self.panel.Refresh()


	def onChoice(self, event, target_id):
		self.loadimage(target_id)


	def createWidgets(self):
		img = wx.EmptyImage(240,240)
		self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
										 wx.BitmapFromImage(img))
 
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		
		self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
						   0, wx.ALL|wx.EXPAND, 5)
		self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
 
		self.panel.SetSizer(self.mainSizer)
		self.mainSizer.Fit(self.frame)
 
		self.panel.Layout()