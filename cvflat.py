from __future__ import division
import wx
import numpy
import os
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

class CVFlat(wx.Panel):
	""""""
 
	#----------------------------------------------------------------------
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size = (1100,600))
		self.SetBackgroundColour((60,70,100))
		self.SetForegroundColour((255,255,255))

		self.screens_tall = 2
		self.screens_wide = 2
		self.tiles_per_axis = 5

		self.name = 'circleburg'
		self.image_dir = '%s_images' % self.name
		self.savepath = 'saved/%s' % self.name
		self.make_widgets()

		self.position = (0,0)
		self.slides = []

		self.palette = Palette(self, tiles_across=2, tiles_tall=10, full_tile_size=50)

		self.worldmap = Worldmap(self, self.palette, self.screens_wide, self.screens_tall, self.tiles_per_axis)
		self.room_index = (0,0)
		
		self.current_room = self.worldmap.room_grid[self.room_index[0]][self.room_index[1]]
		self.display_window = DisplayWindow(self, height=500, width=800, current_room=self.current_room)

		self.highlighter = self.make_highlighter(1,0,0,5)
		self.avatar = wx.Image('characters/Mr_Circle.png', wx.BITMAP_TYPE_ANY)

		self.current_room.DrawImageAtPosition(self.highlighter, self.position[0], self.position[1])
		self.display_window.refresh()

		self.Bind(wx.EVT_CHAR_HOOK, lambda event: self.onKey(event))

		#self.load_path('saved/circleburg')

		self.refresh()

	def make_widgets(self):
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.SetSizer(self.mainSizer)
		self.mainSizer.AddSpacer(10)

		self.controlPanel = wx.Panel(self)
		self.controlPanelSizer = wx.BoxSizer(wx.VERTICAL)
		self.controlPanel.SetSizer(self.controlPanelSizer)

		# control bar 1

		self.controlBar = wx.Panel(self.controlPanel)
		self.controlBarSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.controlBar.SetSizer(self.controlBarSizer)


		self.makeCVButton = wx.Button(self.controlBar, label = "Make slides")
		self.makeCVButton.Bind(wx.EVT_LEFT_UP, lambda event: self.onMakeCV(event))
		self.controlBarSizer.Add(self.makeCVButton, 0, wx.CENTER)

		self.loadCVButton = wx.Button(self.controlBar, label = "Load existing")
		self.loadCVButton.Bind(wx.EVT_LEFT_UP, lambda event: self.onLoad(event))
		self.controlBarSizer.Add(self.loadCVButton, 0, wx.CENTER)

		self.viewButton = wx.Button(self.controlBar, label = "View")
		self.viewButton.Bind(wx.EVT_LEFT_UP, lambda event: self.onView(event))
		self.controlBarSizer.Add(self.viewButton, 0, wx.CENTER)
		
		## control bar 2

		self.controlBar2 = wx.Panel(self.controlPanel)
		self.controlBar2Sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.controlBar2.SetSizer(self.controlBar2Sizer)

		self.name_field= wx.TextCtrl(self.controlBar2, style=wx.TE_PROCESS_ENTER, size = (300,-1))
		self.name_field.Bind(wx.EVT_TEXT, self.onNameText)
		self.controlBar2Sizer.Add(self.name_field)

		# control panel adds bars

		self.controlPanelSizer.Add(self.controlBar)
		self.controlPanelSizer.Add(self.controlBar2)
		self.mainSizer.Add(self.controlPanel, 0, wx.CENTER)

		self.mainSizer.AddSpacer(40)
		self.mainSizer.Add(self.hSizer, 0, wx.CENTER)

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
			self.TryMove(self.highlighter, new_x, new_y, self.current_room)
		elif keycode == wx.WXK_RIGHT:
			new_x, new_y = self.position[0]+1, self.position[1]
			self.TryMove(self.highlighter, new_x, new_y, self.current_room)
		elif keycode == wx.WXK_UP:
			new_x, new_y = self.position[0], self.position[1]-1
			self.TryMove(self.highlighter, new_x, new_y, self.current_room)
		elif keycode == wx.WXK_DOWN:
			new_x, new_y = self.position[0], self.position[1]+1
			self.TryMove(self.highlighter, new_x, new_y, self.current_room)
		else:
			event.DoAllowNextEvent()

	def onMakeCV(self, event):
		self.image_dir = '%s_images' % self.name
		self.savepath = 'saved/%s' % self.name

		if os.path.isdir(self.image_dir):
			self.clear_directory(self.image_dir)
		else:
			os.mkdir(self.image_dir)

		self.current_room.DrawTile(self.position[0],self.position[1])
		current_id = 0
		sm_grid = numpy.zeros(shape=(len(self.worldmap.room_grid), len(self.worldmap.room_grid[0])),dtype=object)
		for x in range(len(self.worldmap.room_grid)):
			for y in range(len(self.worldmap.room_grid[0])):
				room = self.worldmap.room_grid[x][y]
				self.room_index = (x,y)
				sm, current_id = self.make_room(room, current_id)
				sm_grid[x][y] = sm
		self.connect_rooms(sm_grid)

		dlg = wx.TextEntryDialog(self, 'Name your output file','Output naming')
		dlg.SetValue(self.savepath)
		
		#if dlg.ShowModal() == wx.ID_OK:
		#	print('Saved!')

		self.savepath = dlg.GetValue()

		dlg.Destroy()
		data = [(s.to_json()) for s in self.slides]

		print 'saving to', self.savepath
		with open(self.savepath, 'w') as outfile:
			json.dump(data, outfile)
		
	def clear_directory(self, dirpath):
		for fpath in os.listdir(dirpath):
			path = '%s/%s' % (dirpath, fpath)
			os.remove(path)

	def make_room(self, room, id_start):
		tile_matrix = room.tile_matrix
		slide_matrix = [[None for y in range(len(tile_matrix[0]))] for x in range(len(tile_matrix))]
		current_slide_id = id_start
		for x in range(len(tile_matrix)):
			for y in range(len(tile_matrix[x])):
				tile = tile_matrix[x][y]
				if tile.emptiness:
					self.TryMove(self.avatar,x,y,room)
					s = Slide(current_slide_id, room.img, self.image_dir)
					s.title = 'room (%s,%s) tile (%s, %s)' % (self.room_index[0], self.room_index[1], x, y)
					slide_matrix[x][y] = s
					self.slides.append(s)
					current_slide_id += 1
		for x in range(len(slide_matrix)):
			print 'row', x
			for y in range(len(slide_matrix[0])):
				if slide_matrix[x][y]:
					print slide_matrix[x][y].slide_id
				else:
					print 'None'
		self.add_direction_options(slide_matrix)
		room.DrawTile(self.position[0],self.position[1])
		return slide_matrix, current_slide_id		# this is the id of the next slide to be created


	def add_direction_options(self, slide_matrix):
		for x in range(len(slide_matrix)):
			for y in range(len(slide_matrix[0])):
				if slide_matrix[x][y]:
					#print x, y
					#print slide_matrix[x][y].slide_id
					
					s = slide_matrix[x][y]

					if y-1 in range(len(slide_matrix[0])) and slide_matrix[x][y-1]:
						above = slide_matrix[x][y-1]
						s.choices.append(('North',above.slide_id))
					else:
						s.choices.append(('North',s.slide_id))

					if y+1 in range(len(slide_matrix[0])) and slide_matrix[x][y+1]:
						below = slide_matrix[x][y+1]
						s.choices.append(('South',below.slide_id))
					else:
						s.choices.append(('South',s.slide_id))

					if x+1 in range(len(slide_matrix)) and slide_matrix[x+1][y]:
						right = slide_matrix[x+1][y]
						s.choices.append(('East',right.slide_id))
					else:
						s.choices.append(('East',s.slide_id))

					if x-1 in range(len(slide_matrix)) and slide_matrix[x-1][y]:
						left = slide_matrix[x-1][y]
						s.choices.append(('West',left.slide_id))
					else:
						s.choices.append(('West',s.slide_id))


					#print 'after'
					#print s.choices
					#print '\n'

	# given two west-east adjacent rooms (represented as slide matrices), connects all adjacent open squares
	def connect_west_east(self, west_room, east_room):
		for y in range(len(east_room[0])):
			edge_of_east_room = east_room[0][y]
			edge_of_west_room = west_room[-1][y]
			if edge_of_east_room and edge_of_west_room: 	# if these positions in the slide matrices are not 'None'
				edge_of_west_room.choices[2] = ('East', edge_of_east_room.slide_id)
				edge_of_east_room.choices[3] = ('West', edge_of_west_room.slide_id)
				#print edge_of_west_room.slide_id, 'now goes east to', + edge_of_east_room.slide_id

	# given two north-south adjacent rooms, (represented as slide matrices), connects all adjacent open squares
	def connect_north_south(self, north_room, south_room):
		for x in range(len(north_room)):
			edge_of_north_room = north_room[x][-1]
			edge_of_south_room = south_room[x][0]
			if edge_of_north_room and edge_of_south_room:
				edge_of_south_room.choices[0] = ('North', edge_of_north_room.slide_id)
				edge_of_north_room.choices[1] = ('South', edge_of_south_room.slide_id)
	
	# given a grid of slide matrices, connects the appropriate rooms
	def connect_rooms(self, sm_grid):
		for x in range(len(sm_grid)):
			for y in range(len(sm_grid[0])):
				if x < len(sm_grid)-1:
					west_room = sm_grid[x][y]
					east_room = sm_grid[x+1][y]
					self.connect_west_east(west_room, east_room)
				if y < len(sm_grid[0])-1:
					north_room = sm_grid[x][y]
					south_room = sm_grid[x][y+1]
					self.connect_north_south(north_room, south_room)


	def onView(self, event):
		viewer = Viewer(self, self.slides, self.savepath, self.name)

	def onLoad(self, event):
		self.loadDialog()

	# selects existing cv to load
	def loadDialog(self):
		loadChannelDialog = wx.FileDialog(self)

		loadChannelDialog.SetMessage("Choose a map to load")

		loadChannelDialog.ShowModal()

		path = loadChannelDialog.GetPath()
		
		self.load_path(path)
		loadChannelDialog.Destroy()

	# receives path from loadDialog
	def load_path(self, path):
		with open(path) as data_file:
			data = json.load(data_file)

		self.slides = [self.slide_from_json(json.loads(d)) for d in data]


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

	def TryMove(self, image_to_draw, new_x, new_y, room):
		if -1 < new_x < self.current_room.tiles_across and -1 < new_y < self.current_room.tiles_tall:
			room.DrawTile(self.position[0],self.position[1])
			self.position = (new_x, new_y)
			room.DrawImageAtPosition(image_to_draw, self.position[0], self.position[1])
			self.display_window.refresh()
		elif new_x == self.current_room.tiles_across and self.room_index[0] < self.worldmap.rooms_across-1:
			room.DrawTile(self.position[0],self.position[1])
			self.room_index = (self.room_index[0] + 1, self.room_index[1])
			self.position = (0, new_y)
			self.set_current_room(self.room_index)
			self.current_room.DrawImageAtPosition(image_to_draw, self.position[0], self.position[1])
			self.display_window.refresh()
		elif new_x == -1 and self.room_index[0] > 0:
			room.DrawTile(self.position[0],self.position[1])
			self.room_index = (self.room_index[0] - 1, self.room_index[1])
			self.position = (self.current_room.tiles_across-1, new_y)
			self.set_current_room(self.room_index)
			self.current_room.DrawImageAtPosition(image_to_draw, self.position[0], self.position[1])
			self.display_window.refresh()
		elif new_y == self.current_room.tiles_tall and self.room_index[1] < self.worldmap.rooms_tall-1:
			room.DrawTile(self.position[0],self.position[1])
			self.room_index = (self.room_index[0], self.room_index[1]+1)
			self.position = (new_x, 0)
			self.set_current_room(self.room_index)
			self.current_room.DrawImageAtPosition(image_to_draw, self.position[0], self.position[1])
			self.display_window.refresh()
		elif new_y == -1 and self.room_index[1] > 0:
			room.DrawTile(self.position[0],self.position[1])
			self.room_index = (self.room_index[0], self.room_index[1]-1)
			self.position = (new_x, self.current_room.tiles_tall-1)
			self.set_current_room(self.room_index)
			self.current_room.DrawImageAtPosition(image_to_draw, self.position[0], self.position[1])
			self.display_window.refresh()
		else:
			print "Can't make that move"

	def onNameText(self, e):
		self.name = self.name_field.GetValue()


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