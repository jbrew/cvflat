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
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)

		self.createWidgets()
		self.buttonBox = wx.Panel(self.panel)
		self.buttonSizer = wx.BoxSizer(wx.VERTICAL)
		self.buttonBox.SetSizer(self.buttonSizer)
		self.loadslide(0)

	def loadslide(self, slide_id):
		self.mainSizer.Clear()
		self.buttonSizer.Clear(True)
		self.current_slide = self.slides[slide_id]
		self.textbox.SetValue(self.current_slide.text)

		self.loadimage(self.current_slide.imagepath)
		
		self.mainSizer.Add(self.buttonBox)

		for choice in self.current_slide.choices:
			print 'choice', choice
			choice_text, target_id = choice[0], choice[1]
			cbutton = wx.Button(self.buttonBox, label=choice_text)
			cbutton.Bind(wx.EVT_LEFT_UP, lambda event, target_id = target_id: self.onChoice(event, target_id))
			self.buttonSizer.Add(cbutton)

		self.buttonSizer.Layout()
		self.buttonBox.Refresh()
		self.buttonBox.Layout()
		self.panel.Layout()
		self.panel.Refresh()

	def loadimage(self, filepath):
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


	def createWidgets(self):
		img = wx.EmptyImage(240,240)
		self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
										 wx.BitmapFromImage(img))
		
		self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
						   0, wx.ALL|wx.EXPAND, 5)
		self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
 
 		self.textbox = wx.TextCtrl(self.panel)
 		self.textbox.Bind(wx.EVT_TEXT, self.onText)
 		self.mainSizer.Add(self.textbox)

		self.panel.SetSizer(self.mainSizer)
		self.mainSizer.Fit(self.frame)
 
		self.panel.Layout()

	def onChoice(self, event, target_id):
		self.loadslide(target_id)

	def onText(self, e):
		print self.textbox.GetValue()
		self.current_slide.text = self.textbox.GetValue()


