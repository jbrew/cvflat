from __future__ import division
import wx
import numpy
import json
import pickler
from room import Room
from worldmap import Worldmap
from displaywindow import DisplayWindow
from tile import Tile
from image import Image
from palette import Palette
from slide import Slide
from viewer import Viewer
from walltoggler import WallToggler

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
		self.makeCVButton.Bind(wx.EVT_LEFT_UP, lambda event: self.onMakeCV(event))
		self.controlSizer.Add(self.makeCVButton, 0, wx.CENTER)

		self.loadCVButton = wx.Button(self, label = "Load existing")
		self.loadCVButton.Bind(wx.EVT_LEFT_UP, lambda event: self.onLoad(event))
		self.controlSizer.Add(self.loadCVButton, 0, wx.CENTER)

		self.viewButton = wx.Button(self, label = "View")
		self.viewButton.Bind(wx.EVT_LEFT_UP, lambda event: self.onView(event))
		self.controlSizer.Add(self.viewButton, 0, wx.CENTER)
		
		self.mainSizer.Add(self.controlPanel, 0, wx.CENTER)

		self.mainSizer.AddSpacer(40)
		self.mainSizer.Add(self.hSizer, 0, wx.CENTER)

		self.position = (0,0)
		self.slides = []

		self.palette = Palette(self, height = 100, width = 100, tiles_across=2, tiles_tall=2, full_tile_size=50)

		self.worldmap = Worldmap(self, self.palette, 4, 1)
		self.room_index = (0,0)
		
		self.current_room = self.worldmap.room_grid[self.room_index[0]][self.room_index[1]]
		self.display_window = DisplayWindow(self, height=500, width=800, current_room=self.current_room)

		self.avatar = wx.Image('images/mrcircle.png', wx.BITMAP_TYPE_ANY)
		self.highlighter = self.make_highlighter(1,0,0,5)

		self.current_room.DrawImageAtPosition(self.highlighter, self.position[0], self.position[1])
		self.display_window.refresh()

		self.Bind(wx.EVT_CHAR_HOOK, lambda event: self.onKey(event))

		self.refresh()

	def set_current_room(self, room_index):
		self.current_room = self.worldmap.room_grid[self.room_index[0]][self.room_index[1]]
		self.display_window.set_current_room(self.current_room)
		self.display_window.refresh()

	def refresh(self):
		self.hSizer.Add(self.palette)
		self.hSizer.AddSpacer(50)
		self.hSizer.Add(self.display_window)
		self.Layout()

	# returns an image with a transparent center and a colored border
	def make_highlighter(self, r, g, b, linewidth):
		highlighter = wx.EmptyImage(100,100)
		highlighter.InitAlpha()
		for x in range(0, highlighter.GetWidth()):
			for y in range(0, highlighter.GetHeight()):
				highlighter.SetAlpha(x,y,0)
				if x < linewidth or y < linewidth or x > highlighter.GetWidth()-linewidth or y > highlighter.GetHeight() - linewidth:
					highlighter.SetRGB(x,y,r,g,b)
					highlighter.SetAlpha(x,y,1)
		return highlighter





	def onKey(self, event):
		keycode = event.GetKeyCode()
		shift_down = event.ShiftDown()
		command_down = event.CmdDown()

		if keycode == wx.WXK_LEFT:
			new_x, new_y = self.position[0]-1, self.position[1]
			self.TryMove(self.highlighter, new_x, new_y)
		elif keycode == wx.WXK_RIGHT:
			new_x, new_y = self.position[0]+1, self.position[1]
			self.TryMove(self.highlighter, new_x, new_y)
		elif keycode == wx.WXK_UP:
			new_x, new_y = self.position[0], self.position[1]-1
			self.TryMove(self.highlighter, new_x, new_y)
		elif keycode == wx.WXK_DOWN:
			new_x, new_y = self.position[0], self.position[1]+1
			self.TryMove(self.highlighter, new_x, new_y)

	def onMakeCV(self, event):
		tile_matrix = self.current_room.tile_matrix
		slide_matrix = [[None for y in range(len(tile_matrix[0]))] for x in range(len(tile_matrix))]
		current_slide_id = 0
		for x in range(len(tile_matrix)):
			for y in range(len(tile_matrix[x])):
				tile = tile_matrix[x][y]
				if tile.emptiness:
					self.TryMove(self.avatar,x,y)
					s = Slide(current_slide_id, self.current_room.img, self.name)
					slide_matrix[x][y] = s
					self.slides.append(s)
					current_slide_id += 1
		self.add_direction_options(slide_matrix)

		dlg = wx.TextEntryDialog(self, 'Name your output file','Output naming')
		dlg.SetValue("Default")
		#if dlg.ShowModal() == wx.ID_OK:
		#	print('You entered: %s\n' % dlg.GetValue())

		jsonfilepath = 'saved/json/%s.json' % dlg.GetValue()

		dlg.Destroy()
		data = [(s.to_json()) for s in self.slides]
		with open(jsonfilepath, 'w') as outfile:
			json.dump(data, outfile)

		
		picklepath = 'saved/pickles/%s.pkl' % dlg.GetValue()
		pickler.save_object(self.worldmap, picklepath)
		

	def make_room(self, room, west=None, east=None, north=None, south=None):
		tile_matrix = self.current_room.tile_matrix
		slide_matrix = [[None for y in range(len(tile_matrix[0]))] for x in range(len(tile_matrix))]
		current_slide_id = 0
		for x in range(len(tile_matrix)):
			for y in range(len(tile_matrix[x])):
				tile = tile_matrix[x][y]
				if tile.emptiness:
					self.TryMove(self.avatar,x,y)
					s = Slide(current_slide_id, self.current_room.img, self.name)
					slide_matrix[x][y] = s
					self.slides.append(s)
					current_slide_id += 1


	def add_direction_options(self, slide_matrix):
		for x in range(len(slide_matrix)):
			for y in range(len(slide_matrix[0])):
				if slide_matrix[x][y]:
					s = slide_matrix[x][y]

					if y-1 in range(len(slide_matrix[0])) and slide_matrix[x][y-1]:
						above = slide_matrix[x][y-1]
						s.choices.append(('North',above.slide_id))
					if y+1 in range(len(slide_matrix[0])) and slide_matrix[x][y+1]:
						below = slide_matrix[x][y+1]
						s.choices.append(('South',below.slide_id))
					if x-1 in range(len(slide_matrix)) and slide_matrix[x-1][y]:
						left = slide_matrix[x-1][y]
						s.choices.append(('West',left.slide_id))
					if x+1 in range(len(slide_matrix)) and slide_matrix[x+1][y]:
						right = slide_matrix[x+1][y]
						s.choices.append(('East',right.slide_id))
		

	def onView(self, event):
		self.viewer = Viewer(self, self.slides)

	def onLoad(self, event):
		self.loadDialog()

	# selects existing cv to load
	def loadDialog(self):
		loadChannelDialog = wx.FileDialog(self)

		loadChannelDialog.SetMessage("Choose a CV to load")

		loadChannelDialog.ShowModal()

		path = loadChannelDialog.GetPath()
		
		with open(path) as data_file:    
			data = json.load(data_file)

		loadChannelDialog.Destroy()

		self.slides = [self.slide_from_json(json.loads(d)) for d in data]

		"""
		pathstub = path.split('/')[-1]
		print 'stub:',pathstub
		picklepath = 'saved/pickles/%s' % pathstub
		self.worldmap = pickler.loadobject(picklepath)
		"""

		print 'choices for first 3 slides'
		for s in self.slides[0:3]:
			print s.choices

	# given a json object representing a slide, returns the slide object
	def slide_from_json(self, data):
		filepath = data[u'photo_placeholder_url']
		image = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

		s = Slide(data[u'id'], image, self.name)
		s.title = data[u'title']
		s.image = image
		s.text = data[u'body']
		s.start = data[u'start']
		s.finish = data[u'finish']
		s.shareable = data[u'shareable']
		s.choices = [(choice[u'body'], choice[u'to_node']) for choice in data[u'links']]

		return s

	def TryMove(self, image_to_draw, new_x, new_y):
		if -1 < new_x < self.current_room.tiles_across and -1 < new_y < self.current_room.tiles_tall:
			self.current_room.DrawTile(self.position[0],self.position[1])
			self.position = (new_x, new_y)
			self.current_room.DrawImageAtPosition(image_to_draw, self.position[0], self.position[1])
			self.display_window.refresh()
		elif new_x == self.current_room.tiles_across and self.room_index[0] < self.worldmap.rooms_across-1:
			self.current_room.DrawTile(self.position[0],self.position[1])
			self.room_index = (self.room_index[0] + 1, self.room_index[1])
			self.position = (0, new_y)
			self.set_current_room(self.room_index)
			self.current_room.DrawImageAtPosition(image_to_draw, self.position[0], self.position[1])
			self.display_window.refresh()
		elif new_x == -1 and self.room_index[0] > 0:
			self.current_room.DrawTile(self.position[0],self.position[1])
			self.room_index = (self.room_index[0] - 1, self.room_index[1])
			self.position = (self.current_room.tiles_across-1, new_y)
			self.set_current_room(self.room_index)
			self.current_room.DrawImageAtPosition(image_to_draw, self.position[0], self.position[1])
			self.display_window.refresh()
		elif new_y == self.current_room.tiles_tall and self.room_index[1] < self.worldmap.rooms_tall-1:
			self.current_room.DrawTile(self.position[0],self.position[1])
			self.room_index = (self.room_index[0], self.room_index[1]+1)
			self.position = (new_x, 0)
			self.set_current_room(self.room_index)
			self.current_room.DrawImageAtPosition(image_to_draw, self.position[0], self.position[1])
			self.display_window.refresh()
		elif new_y == -1 and self.room_index[1] > 0:
			self.current_room.DrawTile(self.position[0],self.position[1])
			self.room_index = (self.room_index[0], self.room_index[1]-1)
			self.position = (new_x, self.current_room.tiles_tall-1)
			self.set_current_room(self.room_index)
			self.current_room.DrawImageAtPosition(image_to_draw, self.position[0], self.position[1])
			self.display_window.refresh()
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