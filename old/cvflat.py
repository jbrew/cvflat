from __future__ import division
import wx
import numpy
from worldmap import WorldMap
from tile import Tile
from image import Image
from palette import Palette

class CVFlat(wx.Panel):
	""""""
 
	#----------------------------------------------------------------------
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size = (1050,600))
		self.SetBackgroundColour((60,70,100))
		self.SetForegroundColour((255,255,255))

		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.SetSizer(self.mainSizer)
		self.mainSizer.AddSpacer(50)
		self.mainSizer.Add(self.hSizer, 0, wx.CENTER)

		self.palette = Palette(self, tiles_across=2,tiles_tall=2, tile_size=60)
		self.worldmap = WorldMap(self, self.palette, tiles_across=5, tiles_tall=5, tile_size=60)
		

		self.refresh()

		

	def refresh(self):

		self.hSizer.Add(self.palette)
		self.hSizer.AddSpacer(50)
		self.hSizer.Add(self.worldmap)
		self.Layout()




		


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