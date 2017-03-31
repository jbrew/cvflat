from __future__ import division
import wx
import numpy
from worldmap import WorldMap
from tile import Tile
from image import Image

class CVFlat(wx.Panel):
	""""""
 
	#----------------------------------------------------------------------
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size = (1050,600))
		self.SetBackgroundColour((60,70,100))
		self.SetForegroundColour((255,255,255))

		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.mainSizer)

		tiles_across = 3
		tiles_tall = 4

		worldmap = WorldMap(tiles_across,tiles_tall,100)

		self.img = worldmap.to_image(0,tiles_across,0,tiles_tall)
		canvas = self.img.canvas
		self.png = self.ArrayToBitmap(canvas)
		self.bmp = wx.StaticBitmap(self, -1, self.png, (10, 5), (self.png.GetWidth(), self.png.GetHeight()))
		self.bmp.Bind(wx.EVT_LEFT_UP, self.onClick)

		self.mainSizer.AddSpacer(50)
		self.mainSizer.Add(self.bmp, 0, wx.CENTER)

	def ArrayToBitmap( self, array):
		height, width = len(array), len(array[0])
		image = wx.EmptyImage(width,height)
		image.SetData( array.tostring())
		wxBitmap = image.ConvertToBitmap()       # OR:  wx.BitmapFromImage(image)
		return wxBitmap

	def onClick(self, e):
		x, y = e.GetPositionTuple()[0], e.GetPositionTuple()[1]
		print self.img.get_tile(x, y)
		


########################################################################
class TopFrame(wx.Frame):
	""""""
 
	#----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		wx.Frame.__init__(self, parent=None, title="CV FLAT")
		menubar = wx.MenuBar()
		fileMenu = wx.Menu()
		menubar.Append(fileMenu, '&File')
		self.SetMenuBar(menubar)
		self.fSizer = wx.BoxSizer(wx.VERTICAL)
		panel = CVFlat(self)
		self.fSizer.Add(panel, 1, wx.EXPAND)
		self.SetSizer(self.fSizer)
		self.Fit()
		self.Center()
		self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
	app = wx.App(False)
	frame = TopFrame()
	app.MainLoop()