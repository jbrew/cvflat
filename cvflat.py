from __future__ import division
import wx
import numpy
from worldmap import WorldMap
from tile import Tile
from image import Image
from palette import Palette
from slide import Slide

class CVFlat(wx.Panel):
	""""""
 
	#----------------------------------------------------------------------
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size = (1100,600))
		self.SetBackgroundColour((60,70,100))
		self.SetForegroundColour((255,255,255))

		self.name = 'testcv'
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.SetSizer(self.mainSizer)
		self.mainSizer.AddSpacer(10)
		self.makeCVButton = wx.Button(self, label = "Make slides")
		self.makeCVButton.Bind(wx.EVT_LEFT_UP, lambda event: self.onClickMakeCV(event))
		self.mainSizer.Add(self.makeCVButton, 0, wx.CENTER)
		self.mainSizer.AddSpacer(40)
		self.mainSizer.Add(self.hSizer, 0, wx.CENTER)


		self.position = (0,0)
		self.slides = []

		self.palette = Palette(self, height = 100, width = 100, tiles_across=2, tiles_tall=2, full_tile_size=100)
		self.worldmap = WorldMap(self, self.palette, height=500, width=800)

		#filepath = 'images/sonic.jpg'
		filepath = 'images/smileface.png'
		self.avatar = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
		self.worldmap.DrawImageAtPosition(self.avatar, 2, 2)
		self.worldmap.refresh()

		self.worldmap.DrawImageAtPosition(self.get_screencap(2,2,200), 2, 4)

		self.avatar_at_position(self.position[0], self.position[1])

		self.Bind(wx.EVT_CHAR_HOOK, lambda event: self.onKey(event))

		self.refresh()


	def get_screencap(self, xpos, ypos, scope=100):
		x, y = self.worldmap.center_of_tile(xpos,ypos)
		return self.worldmap.GetScreen(x, y, scope, scope)

	def refresh(self):

		self.hSizer.Add(self.palette)
		self.hSizer.AddSpacer(50)
		self.hSizer.Add(self.worldmap)
		self.Layout()

	def avatar_at_position(self, x, y):
		self.worldmap.DrawImageAtPosition(self.avatar, x, y)
		self.worldmap.refresh()


	def onKey(self, event):
		keycode = event.GetKeyCode()
		shift_down = event.ShiftDown()
		command_down = event.CmdDown()

		if keycode == wx.WXK_LEFT:
			new_r, new_c = self.position[0], self.position[1]-1
			self.TryMove(new_r, new_c)
		elif keycode == wx.WXK_RIGHT:
			new_r, new_c = self.position[0], self.position[1]+1
			self.TryMove(new_r, new_c)
		elif keycode == wx.WXK_UP:
			new_r, new_c = self.position[0]-1, self.position[1]
			self.TryMove(new_r, new_c)
		elif keycode == wx.WXK_DOWN:
			new_r, new_c = self.position[0]+1, self.position[1]
			self.TryMove(new_r, new_c)

	def onClickMakeCV(self, event):
		tm = self.worldmap.tile_matrix
		current_slide_id = 0
		for x in range(len(tm)):
			for y in range(len(tm[0])):
				tile = tm[x][y]
				if tile.emptiness:
					self.TryMove(x,y)
					s = Slide(current_slide_id, self.worldmap.img, self.name)
					self.slides.append(s)
					current_slide_id += 1


	def TryMove(self, new_r, new_c):
		if self.worldmap.SquareIsEmpty(new_r, new_c):
				self.worldmap.DrawTile(self.position[0],self.position[1])
				self.position = (new_r, new_c)
				self.avatar_at_position(self.position[0], self.position[1])
		else:
			print "Can't make that move"



		


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