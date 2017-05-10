from __future__ import division
import wx
import numpy
import json
from room import Room
from tile import Tile
from image import Image
from palette import Palette
from slide import Slide
from viewer import Viewer

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

		self.controlPanel = wx.Panel(self)
		self.controlSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.controlPanel.SetSizer(self.controlSizer)

		self.makeCVButton = wx.Button(self, label = "Make slides")
		self.makeCVButton.Bind(wx.EVT_LEFT_UP, lambda event: self.onClickMakeCV(event))
		self.controlSizer.Add(self.makeCVButton, 0, wx.CENTER)

		self.viewButton = wx.Button(self, label = "View")
		self.viewButton.Bind(wx.EVT_LEFT_UP, lambda event: self.onView(event))
		self.controlSizer.Add(self.viewButton, 0, wx.CENTER)
		
		self.mainSizer.Add(self.controlPanel, 0, wx.CENTER)

		self.mainSizer.AddSpacer(40)
		self.mainSizer.Add(self.hSizer, 0, wx.CENTER)

		self.position = (0,0)
		self.slides = []

		self.palette = Palette(self, height = 100, width = 100, tiles_across=2, tiles_tall=2, full_tile_size=100)
		self.current_room = Room(self, self.palette, width=800, height=500)

		#filepath = 'images/sonic.jpg'
		filepath = 'images/smileface.png'
		self.avatar = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
		#self.current_room.DrawImageAtPosition(self.avatar, 2, 2)
		self.current_room.refresh()

		#self.current_room.DrawImageAtPosition(self.get_screencap(2,2,200), 2, 4)

		self.avatar_at_position(self.position[0], self.position[1])

		self.Bind(wx.EVT_CHAR_HOOK, lambda event: self.onKey(event))

		self.refresh()


	def get_screencap(self, xpos, ypos, scope=100):
		x, y = self.current_room.center_of_tile(xpos,ypos)
		return self.current_room.GetScreen(x, y, scope, scope)

	def refresh(self):

		self.hSizer.Add(self.palette)
		self.hSizer.AddSpacer(50)
		self.hSizer.Add(self.current_room)
		self.Layout()

	def avatar_at_position(self, x, y):
		self.current_room.DrawImageAtPosition(self.avatar, x, y)
		self.current_room.refresh()


	def onKey(self, event):
		keycode = event.GetKeyCode()
		shift_down = event.ShiftDown()
		command_down = event.CmdDown()

		if keycode == wx.WXK_LEFT:
			new_x, new_y = self.position[0]-1, self.position[1]
			self.TryMove(new_x, new_y)
		elif keycode == wx.WXK_RIGHT:
			new_x, new_y = self.position[0]+1, self.position[1]
			self.TryMove(new_x, new_y)
		elif keycode == wx.WXK_UP:
			new_x, new_y = self.position[0], self.position[1]-1
			self.TryMove(new_x, new_y)
		elif keycode == wx.WXK_DOWN:
			new_x, new_y = self.position[0], self.position[1]+1
			self.TryMove(new_x, new_y)

	def onClickMakeCV(self, event):
		tile_matrix = self.current_room.tile_matrix
		slide_matrix = [[None for y in range(len(tile_matrix[0]))] for x in range(len(tile_matrix))]
		current_slide_id = 0
		for x in range(len(tile_matrix)):
			for y in range(len(tile_matrix[x])):
				tile = tile_matrix[x][y]
				if tile.emptiness:
					self.TryMove(x,y)
					s = Slide(current_slide_id, self.current_room.img, self.name)
					slide_matrix[x][y] = s
					self.slides.append(s)
					current_slide_id += 1
		self.add_direction_options(slide_matrix)


		data = [(s.to_json()) for s in self.slides]
		with open('data.json', 'w') as outfile:
			json.dump(data, outfile)
		

	def onView(self, event):
		self.viewer = Viewer(self, self.slides)
					
	def add_direction_options(self, slide_matrix):
		for x in range(len(slide_matrix)):
			for y in range(len(slide_matrix[0])):
				if slide_matrix[x][y]:
					s = slide_matrix[x][y]
					print slide_matrix[x][y].slide_id
					if x-1 in range(len(slide_matrix)) and slide_matrix[x-1][y]:
						left = slide_matrix[x-1][y]
						s.choices.append(('Left',left.slide_id))
					if x+1 in range(len(slide_matrix)) and slide_matrix[x+1][y]:
						right = slide_matrix[x+1][y]
						s.choices.append(('Right',right.slide_id))
					if y-1 in range(len(slide_matrix[0])) and slide_matrix[x][y-1]:
						above = slide_matrix[x][y-1]
						s.choices.append(('Up',above.slide_id))
					if y+1 in range(len(slide_matrix[0])) and slide_matrix[x][y+1]:
						below = slide_matrix[x][y+1]
						s.choices.append(('Down',below.slide_id))



	def TryMove(self, new_x, new_y):
		if self.current_room.SquareIsEmpty(new_x, new_y):
				self.current_room.DrawTile(self.position[0],self.position[1])
				self.position = (new_x, new_y)
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