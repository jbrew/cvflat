from __future__ import division
import numpy
import os
import wx
import json
import copy
from slide import Slide

class Viewer(wx.Frame):

	def __init__(self, parent, slide_list, savepath, cv_name):
		#self.current_id = start_id
		wx.Frame.__init__(self, None, title="Viewer")
		self.panel = wx.Panel(self, size = (600,600))
		self.slides = slide_list
		self.cv_name = cv_name
		self.savepath = savepath
		self.Show()
		self.PhotoMaxSize = 240
		self.slideSizer = wx.BoxSizer(wx.VERTICAL)
		self.hSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.createWidgets()
		self.buttonBox = wx.Panel(self.panel)
		self.buttonSizer = wx.BoxSizer(wx.VERTICAL)
		self.buttonBox.SetSizer(self.buttonSizer)

		self.addOptionBar = wx.Panel(self.panel)
		self.addOptionSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.addOptionBar.SetSizer(self.addOptionSizer)

		self.newOptionTextField = wx.TextCtrl(self.addOptionBar, style=wx.TE_PROCESS_ENTER)
		self.newOptionTargetField = wx.TextCtrl(self.addOptionBar, style=wx.TE_PROCESS_ENTER)
		self.addOptionButton = wx.Button(self.addOptionBar, label='Add option')
		self.addOptionButton.Bind(wx.EVT_LEFT_UP, self.onAddChoice)

		self.addOptionSizer.Add(self.newOptionTextField)
		self.addOptionSizer.Add(self.newOptionTargetField)
		self.addOptionSizer.Add(self.addOptionButton)

		self.loadslide(0)

	def loadslide(self, slide_id):
		self.slideSizer.Clear()
		self.buttonSizer.Clear(True)
		self.current_slide = self.slides[slide_id]
		s = self.current_slide

		self.textbox.SetValue(s.text)
		self.id_field.SetLabel(str(s.slide_id))
		self.title_field.SetValue(s.title)
		self.finishCheckbox.SetValue(s.finish)
		self.startCheckbox.SetValue(s.start)
		self.img = wx.Image(s.image_path, wx.BITMAP_TYPE_ANY)
		self.set_image(self.img)
		
		self.slideSizer.Add(self.buttonBox)
		self.slideSizer.Add(self.addOptionBar)

		for choice in s.choices:
			self.addChoice(choice)

		self.buttonSizer.Layout()
		self.buttonBox.Refresh()
		self.buttonBox.Layout()
		self.panel.Layout()
		self.panel.Refresh()
		self.panel.SetSize((1100,600))


	def addChoice(self, choice):
		#choiceBar = wx.Panel(self.buttonBox)
		cbarSizer = wx.BoxSizer(wx.HORIZONTAL)
		#choiceBar.SetSizer(cbarSizer)
		choice_text, target_id = choice[0], choice[1]
		cbutton = wx.Button(self.buttonBox, label=choice_text)
		cbutton.Bind(wx.EVT_LEFT_UP, lambda event, target_id = target_id: self.onChoice(event, target_id))

		textfield = wx.TextCtrl(self.buttonBox, style=wx.TE_PROCESS_ENTER)
		textfield.Bind(wx.EVT_TEXT_ENTER, lambda event, choice=choice: self.onTextSet(event, choice))
		textfield.SetValue(choice[0])

		targetfield = wx.TextCtrl(self.buttonBox, style=wx.TE_PROCESS_ENTER)
		targetfield.Bind(wx.EVT_TEXT_ENTER, lambda event, choice=choice: self.onTargetSet(event, choice))
		targetfield.SetValue(str(choice[1]))

		removeButton = wx.Button(self.buttonBox, label='X', size = (30,-1))
		removeButton.Bind(wx.EVT_LEFT_UP, lambda event, choice=choice: self.onRemoveChoice(event, choice))

		cbarSizer.Add(cbutton)
		cbarSizer.Add(textfield)
		cbarSizer.Add(targetfield)
		cbarSizer.Add(removeButton)
		self.buttonSizer.Add(cbarSizer)
		self.buttonSizer.Add((10,10),1)
		self.buttonSizer.Layout()
		self.buttonBox.Refresh()
		self.buttonBox.Layout()
		self.panel.Layout()
		self.panel.Refresh()

	def onRemoveChoice(self, event, choice):
		for c in self.current_slide.choices:
			if c == choice:
				print 'removing', c
				self.current_slide.choices.remove(c)
		self.loadslide(self.current_slide.slide_id)


	def onChoice(self, event, target_id):
		self.loadslide(target_id)

	def onTargetSet(self, event, choice):
		field = event.GetEventObject()
		new_target_id = int(field.GetValue())

		new_choices = []
		for c in self.current_slide.choices:
			if c == choice:
				new_choices.append((c[0], new_target_id))
			else:
				new_choices.append((c[0], c[1]))

		self.current_slide.choices = new_choices

		print choice[0], 'now leads to', new_target_id
		self.loadslide(new_target_id)

	def onTextSet(self, event, choice):
		field = event.GetEventObject()
		new_text = field.GetValue()

		new_choices = []
		for c in self.current_slide.choices:
			if c == choice:
				print 'here'
				new_choices.append((new_text, c[1]))
			else:
				new_choices.append((c[0], c[1]))

		self.current_slide.choices = new_choices
		self.loadslide(self.current_slide.slide_id)

	def onAddChoice(self, event):
		choice = (self.newOptionTextField.GetValue(), int(self.newOptionTargetField.GetValue()))
		self.current_slide.choices.append(choice)
		self.addChoice(choice)

	def set_image(self, img):
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
		self.slideSizer.Add(self.imageCtrl, 0, wx.ALL, 5)


	def createWidgets(self):
		img = wx.EmptyImage(240,240)
		self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
										 wx.BitmapFromImage(img))
		
 
 		self.editPanel = wx.Panel(self.panel, size=(300,500))
		self.editSizer = wx.BoxSizer(wx.VERTICAL)
		self.editPanel.SetSizer(self.editSizer)

		self.id_field = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
		self.id_field.Bind(wx.EVT_TEXT_ENTER, self.onEnterID)
		self.title_field = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, size = (300,-1))
		self.title_field.Bind(wx.EVT_TEXT, self.onTitleText)

		self.editSizer.Add(self.id_field)
		self.editSizer.Add(self.title_field)
		
		self.textbox = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE|wx.TE_RICH2, size = (300,100))
		self.textbox.Bind(wx.EVT_TEXT, self.onText)


		self.startCheckbox = wx.CheckBox(self.panel, label="Start")
		self.startCheckbox.Bind(wx.EVT_CHECKBOX, self.onStartCheck)
		
		self.finishCheckbox = wx.CheckBox(self.panel, label="Finish")
		self.finishCheckbox.Bind(wx.EVT_CHECKBOX, self.onFinishCheck)

		"""
		self.drawTextButton = wx.Button(self.panel, label = "Draw text")
		self.drawTextButton.Bind(wx.EVT_LEFT_UP, self.onDrawText)
		"""

		self.addSlideButton = wx.Button(self.panel, label = "Copy slide")
		self.addSlideButton.Bind(wx.EVT_LEFT_UP, self.onAddSlide)

		self.saveButton = wx.Button(self.panel, label = "Save CV")
		self.saveButton.Bind(wx.EVT_LEFT_UP, self.onSave)
		

		self.editSizer.Add(self.textbox)
		self.editSizer.Add(self.startCheckbox, 0, wx.ALL, 8)
		self.editSizer.Add(self.finishCheckbox, 0, wx.ALL, 8)
		#self.editSizer.Add(self.drawTextButton, 0, wx.ALL, 8)
		self.editSizer.Add(self.addSlideButton, 0, wx.ALL, 8)
		self.editSizer.Add(self.saveButton, 0, wx.ALL, 8)

		self.hSizer.Add(self.slideSizer)
		self.hSizer.Add(self.editSizer)
		self.hSizer.Layout()

		self.panel.SetSizer(self.hSizer)
		#self.mainSizer.Fit(self.frame)
 
		self.panel.Layout()

	def onFinishCheck(self, e):
		self.current_slide.finish = not self.current_slide.finish

	def onStartCheck(self, e):
		self.current_slide.start = not self.current_slide.start

	def onText(self, e):
		#print self.textbox.GetValue()
		self.current_slide.text = self.textbox.GetValue()

	def onEnterID(self,e):
		field = e.GetEventObject()
		self.loadslide(int(field.GetValue()))

	def onTitleText(self, e):
		field = e.GetEventObject()
		self.current_slide.title = field.GetValue()

	def onAddSlide(self, e):
		self.copy_slide(self.current_slide)

	# creates a new slide at the current position using the current id
	def copy_slide(self, slide):
		print 'copying...'

		# find the id of the last slide in the list (should be the highest value), and add one
		max_id = self.slides[-1].slide_id
		new_id = max_id + 1

		new_slide = Slide(new_id, self.img, self.cv_name)
		s = self.current_slide
		new_slide.text = ''
		new_slide.title = s.title + ' (copy)'
		new_slide.start = False
		new_slide.finish = False

		print 'created new slide with id %s' % new_id

		self.slides.append(new_slide)

		self.loadslide(new_id)

	def onSave(self, e):
		print 'saving to %s...' % self.savepath
		data = [(s.to_json()) for s in self.slides]
		with open(self.savepath, 'w') as outfile:
			json.dump(data, outfile)

	def onDrawText(self, e):
		s = self.current_slide
		image_path = s.image_path
		img = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
		bmp = wx.BitmapFromImage(img)
		dc = wx.MemoryDC()
		dc.SelectObject(bmp)
		dc.Clear()
		text = self.textbox.GetValue()
		w = bmp.GetWidth()
		h = bmp.GetHeight()
		tw, th = dc.GetTextExtent(text)
		dc.DrawText(text, (w-tw)/2,  (h-th)/2)
		dc.SelectObject(bmp)
		self.set_image(wx.StaticBitmap(self.panel, -1, bmp))
		self.panel.Layout()
		self.panel.Refresh()


	def onKey(self, event):
		keycode = event.GetKeyCode()
		shift_down = event.ShiftDown()
		command_down = event.CmdDown()
		if command_down:
			if keycode == 61: # plus
				self.copySlide()


