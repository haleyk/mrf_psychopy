"""Helper functions for latset game"""

#this goes first and makes sure that python2 can still do division
from __future__ import division

from psychopy import visual, core, event
import csv
import numpy as np
from pandas import DataFrame
from math import atan2, degrees

def block_name(bl):
	if bl == 1:
		return 'one'
	if bl == 2:
		return 'two'
	if bl == 3:
		return 'three'
	if bl == 4:
		return 'four'
	if bl == 5:
		return 'five'
	if bl == 6:
		return 'six'

def makeShape(shape, lat, win):
	"""Creates shape stimuli and associated opposite mask, given shape and lateralization."""
	shape = 'shapes/' + str(shape) + '.png'
	if lat == 'l':
		pos_shape = (-200,0) #TODO: check 200 is the right offset, if it's not change offset in mainLoop too
		pos_mask = (200, 0)
	elif lat == 'r':
		pos_shape = (200, 0)
		pos_mask = (-200, 0)
	else:
		print("you messed up")
		print(1/0)
	return visual.ImageStim(win=win, image=shape, units="pix", pos=pos_shape), visual.ImageStim(win=win, image='shapes/mask_col2.jpg', units="pix", pos=pos_mask)

def wait_for_click(win):
	m = event.Mouse(visible=False, win=win)
	m.clickReset()
	buttons = [0, 0, 0]
	while buttons == [0,0,0]:
		buttons = m.getPressed()
	return


def choice_screen(is_set, win,counterb):
	if counterb == 'A':
		set_pos = (-100,0)
		nset_pos = (100,0)
	if counterb == 'B':
		set_pos = (100,0)
		nset_pos = (-100,0)
	stim1 = visual.TextStim(win, 'set', wrapWidth=800, height=50,color='black',pos=set_pos)
	stim1.draw()
	stim2 = visual.TextStim(win, 'no set', wrapWidth=800, height=50,color='black',pos=nset_pos)
	stim2.draw()
	m = event.Mouse(visible=False, win=win)
	m.clickReset()
	win.flip()
	buttons = [0, 0, 0]
	timee = 10
	timer = core.CountdownTimer(10)
	while timee > 0 and buttons == [0, 0, 0]:
		buttons, times = m.getPressed(getTime=True)
		timee = timer.getTime()
	if buttons == [0,0,0]:
		choice = -1
		rt = -1
		cor = -1
	else:
		if buttons == [1, 0, 0] and counterb == 'A': #chose set
			choice = 'set'
			rt = 3 - timee
			cor = int(int(is_set) == True)
		elif buttons == [0, 0, 1] and counterb == 'A': #chose no set
			choice = 'no_set'
			rt = 3 - timee
			cor = int(int(is_set) == False)
		elif buttons == [1, 0, 0] and counterb == 'B': #chose no set
			choice = 'no_set'
			rt = 3 - timee
			cor = int(int(is_set) == False)
		elif buttons == [0, 0, 1] and counterb == 'B': #chose set
			choice = 'set'
			rt = 3 - timee
			cor = int(int(is_set) == True)
	return choice, rt, cor

def getInstructions(part, other=None):
	""" returns instructions for the task """
	if part == 'start1':
		return 'Welcome to the SET experiment!'
	if part == 'start2':
		return 'I will first explain the SET task to you.\nAfter that, there will be some practice, before we start the actual experiment.\nFeel free to ask me any questions you have along the way!'
	if part == 'start3':
		return 'The object of the game is to determine if 3 items for a SET or not.\nEach item has three features, which can vary as follows:'
	if part == 'start4':
		return "3 items form a SET when each of the items' features, looked at one by one, are the same on all items, or, are different on each item.\nAll features must satisfy this rule. In other words: shape must be the same or different on each of the 3 items; color must be either the same or different on each of the 3, etc."
	if part == 'start5':
		return 'A QUICK CHECK - Is it a SET?\n\n If 2 items are the same and the third is different in any feature, then it is not a SET. For example, if 2 items are red and 1 is blue, then it is not a SET. A SET much be either all the same or all different for each individual featre.'
	if part == 'start6':
		return 'This is a SET. All 3 items have the same shape, the same color, and the same fill.'
	if part == 'start7':
		return 'This is a SET. All 3 items have different shapes, different colors, and they all have the same fill.'
	if part == 'start8':
		return 'This is NOT a SET. Two of the items have the same shape, but the third is different. This is not a SET, even though all 3 items have the same color and different fill.'
	if part == 'start9':
		return 'During the experiment, the three items will appear one after another. \nYou will decide after the last item if they form a SET. (You will press the left mouse button for SET and the right for no SET; this will also be indicated on the screen.)\nIt is accurate work that counts.'
	if part == 'start10':
		return 'ATTENTION!\nYou will need to look at the FIXATION CROSS in the center of the screen AT ALL TIMES!\n\nNEVER move your eyes away from the center, even though some patterns will appear at the sides.'
	if part == 'start11':
		return 'Each trial will begin with a fixation cross inside a black box.\n\nYou can start the trial by fixating on the cross. The box will turn green when you are fixating and the trial will start.'
	if part == 'start12':
		return 'You will now get a few practice trials and receive feedback on your answers. (Press any mouse button to move on after the feedback.)\nFeel free to ask any questions during these trials.\nDuring the task, you will be periodically switching which hand controls the mouse.\nPlease start with the mouse in your '+ other +' hand.\nDo you have any questions?'
	if part == 'switch_hands':
		return 'Please move the mouse to your other hand.'
	if part == 'practice2':
		return "Good job!\nDo you have any questions so far?\n\nThe next round will be a little bit faster.Please move the mouse back to your other hand.\n Press any mouse button when you're ready to move on."
	if part == 'ready':
		return 'The experimental session will start now. You will no longer get feedback.\nThe session consists of 6 blocks and will take around 30 minutes to complete. There will be breaks in between.\nPlease remember to keep your eyes on the fixation cross!'
	if part == 'finish':
		return 'Thank you for participating! You have finished the experiment.'
	if part == 'interblock':
		return 'You finished ' + other + ' of six blocks!\nYou can take a break if you want. Feel free to stretch or stand up.\nPlease switch which hand you are using the mouse with.\nPress any key when you wish to go on with the task and we will calibrate your eyes again.'


def convert_to_psychopy(x,y):
	# take in pygaze, convert to psychopy
	new_x = x - 640
	new_y = -1 * (y - 512)
	return new_x, new_y

def euclidian_distance(x1,y1,x2,y2):
	return np.sqrt((x2-x1)**2 + (y2-y1)**2)

def wait_for_center_fix(win,tracker):
	event.clearEvents()
	frame_black = visual.Rect(win, width=100, height=100, units='pix', lineColor='black',pos=(0,0),lineWidth=1.5)
	frame_green = visual.Rect(win, width=100, height=100, units='pix', lineColor='green',pos=(0,0),lineWidth=1.5)
	fixation = visual.ShapeStim(win, vertices=((0, -15), (0, 15), (0,0), (-15,0), (15, 0)),lineWidth=5,closeShape=False,lineColor="black")
	threshold = 1
	c = None
	pixel_distance_from_cross = 50
	threshold_met = False
	no_keypress_k = True #completely kill the script
	no_keypress_s = True #move past fixation -- if can't catch eyes
	tracker.log('stim_waitFix')
	while not threshold_met and no_keypress_k and no_keypress_s:
		no_keypress_k = len(event.getKeys(keyList=['k'])) == 0
		no_keypress_s = len(event.getKeys(keyList=['space'])) == 0
		x, y = tracker.sample()
		x,y = convert_to_psychopy(x,y)
		if euclidian_distance(x,y,0,0) <= pixel_distance_from_cross:
			if not c:
				c = core.Clock()
			else:
				threshold_met = c.getTime() >= threshold
			frame_green.draw()
		else:
			c = None
			frame_black.draw()
		fixation.draw()
		win.flip()
	if not no_keypress_k:
		#want to kill the script, only do this if you really have to
		print(1/0)
	if not no_keypress_s:
		tracker.log('manual_start')

def mainloop(win, trial, fixation, counter, fb=False, fixationTime=.03, stimTime=.180, maskTime=.03, memDelay=.5,tracker=None,trialNum=0):
	static_r = visual.ImageStim(win=win, image='shapes/mask_col2.jpg', units="pix", pos=(200,0))
	static_l = visual.ImageStim(win=win, image='shapes/mask_col2.jpg', units="pix", pos=(-200,0))
	def jitter(minn, maxx):
		minn = minn * 1000 #turn into ms
		maxx = maxx * 1000
		a = np.random.randint(minn, maxx)
		return a / 1000 #turn back into seconds for psychopy
	win.mouseVisible = False
	tracker.log('trial_' + str(trialNum))
	fixation.draw()
	tracker.log('stim_fixation')
	win.flip()
	wait_for_center_fix(win,tracker)
	#draw first shape
	shape1, mask1 = makeShape(trial['shape1'], trial['presentation'][0], win)
	shape1.draw()
	mask1.draw()
	fixation.draw()
	tracker.log('stim_shape1')
	win.flip()
	core.wait(stimTime)
	static_r.draw()
	static_l.draw()
	fixation.draw()
	tracker.log('stim_static')
	win.flip()
	core.wait(maskTime)
	#draw second shape
	fixation.draw()
	tracker.log('stim_fixation')
	win.flip()
	core.wait(fixationTime)
	shape2, mask2 = makeShape(trial['shape2'], trial['presentation'][1], win)
	shape2.draw()
	mask2.draw()
	fixation.draw()
	tracker.log('stim_shape2')
	win.flip()
	core.wait(stimTime)
	static_r.draw()
	static_l.draw()
	fixation.draw()
	tracker.log('stim_static')
	win.flip()
	core.wait(maskTime)
	#draw third shape
	fixation.draw()
	tracker.log('stim_fixation')
	win.flip()
	core.wait(fixationTime)
	shape3, mask3 = makeShape(trial['shape3'], trial['presentation'][2], win)
	shape3.draw()
	mask3.draw()
	fixation.draw()
	tracker.log('stim_shape3')
	win.flip()
	core.wait(stimTime)
	static_r.draw()
	static_l.draw()
	fixation.draw()
	tracker.log('stim_static')
	win.flip()
	core.wait(maskTime)
	fixation.draw()
	tracker.log('stim_fixation')
	win.flip()
	core.wait(memDelay)
	#call sliders
	win.flip()
	choice, rt, cor, = choice_screen(trial['is_set'],win,counter)
	win.flip()

	#show feedback if needed
	if fb:
		tracker.log('stim_feedback')
		if cor == 1:
			string = '' if int(trial['is_set']) else 'not '
			stimtype = visual.TextStim(win, 'Correct! This is ' + string + 'a set.', pos=(0,100), color='black',height=30)
			stimtype.draw()
			visual.ImageStim(win=win, image='shapes/' + str(trial['shape1']) + '.png', units="pix", pos=(-200,-100)).draw()
			visual.ImageStim(win=win, image='shapes/' + str(trial['shape2']) + '.png', units="pix", pos=(0,-100)).draw()
			visual.ImageStim(win=win, image='shapes/' + str(trial['shape3']) + '.png', units="pix", pos=(200,-100)).draw()
			win.flip()
			wait_for_click(win)
		elif cor == 0:
			string = '' if int(trial['is_set']) else 'not '
			stimtype = visual.TextStim(win, 'Incorrect. This is ' + string + 'a set.', pos=(0,100), color='black',height=30)
			stimtype.draw()
			visual.ImageStim(win=win, image='shapes/' + str(trial['shape1']) + '.png', units="pix", pos=(-200,-100)).draw()
			visual.ImageStim(win=win, image='shapes/' + str(trial['shape2']) + '.png', units="pix", pos=(0,-100)).draw()
			visual.ImageStim(win=win, image='shapes/' + str(trial['shape3']) + '.png', units="pix", pos=(200,-100)).draw()
			win.flip()
			wait_for_click(win)
		elif cor == -1:
			stimtype = visual.TextStim(win, "Please respond faster next time.", pos= (0,0), color='black')
			stimtype.draw()
			win.flip()
			wait_for_click(win)

	#record response to global
	return choice, rt, cor

def mainloop_noeye(win, trial, fixation, counter, fb=False, fixationTime=.03, stimTime=.180, maskTime=.03, memDelay=.5,trialNum=0):
	static_r = visual.ImageStim(win=win, image='shapes/mask_col2.jpg', units="pix", pos=(200,0))
	static_l = visual.ImageStim(win=win, image='shapes/mask_col2.jpg', units="pix", pos=(-200,0))
	def jitter(minn, maxx):
		minn = minn * 1000 #turn into ms
		maxx = maxx * 1000
		a = np.random.randint(minn, maxx)
		return a / 1000 #turn back into seconds for psychopy
	win.mouseVisible = False
	fixation.draw()
	win.flip()
	core.wait(.5)
	#draw first shape
	shape1, mask1 = makeShape(trial['shape1'], trial['presentation'][0], win)
	shape1.draw()
	mask1.draw()
	fixation.draw()
	win.flip()
	core.wait(stimTime)
	static_r.draw()
	static_l.draw()
	fixation.draw()
	win.flip()
	core.wait(maskTime)
	#draw second shape
	fixation.draw()
	win.flip()
	core.wait(fixationTime)
	shape2, mask2 = makeShape(trial['shape2'], trial['presentation'][1], win)
	shape2.draw()
	mask2.draw()
	fixation.draw()
	win.flip()
	core.wait(stimTime)
	static_r.draw()
	static_l.draw()
	fixation.draw()
	win.flip()
	core.wait(maskTime)
	#draw third shape
	fixation.draw()
	win.flip()
	core.wait(fixationTime)
	shape3, mask3 = makeShape(trial['shape3'], trial['presentation'][2], win)
	shape3.draw()
	mask3.draw()
	fixation.draw()
	win.flip()
	core.wait(stimTime)
	static_r.draw()
	static_l.draw()
	fixation.draw()
	win.flip()
	core.wait(maskTime)
	fixation.draw()
	win.flip()
	core.wait(memDelay)
	#call sliders
	win.flip()
	choice, rt, cor, = choice_screen(trial['is_set'],win,counter)
	win.flip()

	#show feedback if needed
	if fb:
		if cor == 1:
			string = '' if int(trial['is_set']) else 'not '
			stimtype = visual.TextStim(win, 'Correct! This is ' + string + 'a set.', pos=(0,100), color='black',height=30)
			stimtype.draw()
			visual.ImageStim(win=win, image='shapes/' + str(trial['shape1']) + '.png', units="pix", pos=(-200,-100)).draw()
			visual.ImageStim(win=win, image='shapes/' + str(trial['shape2']) + '.png', units="pix", pos=(0,-100)).draw()
			visual.ImageStim(win=win, image='shapes/' + str(trial['shape3']) + '.png', units="pix", pos=(200,-100)).draw()
			win.flip()
			wait_for_click(win)
		elif cor == 0:
			string = '' if int(trial['is_set']) else 'not '
			stimtype = visual.TextStim(win, 'Incorrect. This is ' + string + 'a set.', pos=(0,100), color='black',height=30)
			stimtype.draw()
			visual.ImageStim(win=win, image='shapes/' + str(trial['shape1']) + '.png', units="pix", pos=(-200,-100)).draw()
			visual.ImageStim(win=win, image='shapes/' + str(trial['shape2']) + '.png', units="pix", pos=(0,-100)).draw()
			visual.ImageStim(win=win, image='shapes/' + str(trial['shape3']) + '.png', units="pix", pos=(200,-100)).draw()
			win.flip()
			wait_for_click(win)
		elif cor == -1:
			stimtype = visual.TextStim(win, "Please respond faster next time.", pos= (0,0), color='black')
			stimtype.draw()
			win.flip()
			wait_for_click(win)

	#record response to global
	return choice, rt, cor
