# like r, you need to tell the interpreter what packages you're going to use
# unlike r, if youre going to use multiple functions from a package and want to not import them all individually
# you need to use the package name every time - which is why you could use shorthand for common ones like np and pd
# also, you need to have what you want to use installed
from psychopy import visual, monitors
from psychopy.visual import Window
from psychopy import core, event
import csv
import numpy as np
import pandas as pd

# window and pixels. if you make one that isn't the right size, it will tell you in warnings in the terminal
full_scr = input('full screen? 1 (yes) or 0 (no)')
if full_scr:
	# 1440 x 900 is size of my mac
	win = win = visual.Window([1440,900], color='black', fullscr=0)
else:
	win = visual.Window([600,400], color='black', fullscr=0)

# basic text
ready_text = visual.TextStim(win, text='hello world!')
# drawing draws "behind the screen"
ready_text.draw()
# flipping the window is how to show things - you can get whatever ready you want in the background in the mean time
win.flip()
core.wait(2) # this literally pauses the script, so its best typically avoided for something more specific
win.flip()
# I like using print(1/0) as a catch all exception that kills my python scripts while I'm testing them
# strictly speaking this is bad coding practice and you should throw an exception
# print(1/0)

# move to the middle and change color
ready_text = visual.TextStim(win, text='hello world!', pos=(450, 0), color='red', units='pix')
ready_text.draw()
win.flip()
core.wait(2)
win.flip()

# same for an image or two
dog1 = visual.ImageStim(win=win, image='dog_cat/im0.jpeg', units="pix", pos=(-300,0))
dog2 = visual.ImageStim(win=win, image='dog_cat/im2.jpeg', units="pix", pos=(300,0))
dog1.draw()
dog2.draw()
win.flip()
core.wait(2)



# lets make a trial
# show an image, get a response, 3 times
responses = []
rts = []
for t in range(3): # python counts from 0!
	im = 'dog_cat/im' + str(t) + '.jpeg'
	dog = visual.ImageStim(win=win, image=im, units="pix", pos=(0,0))
	dog.draw()
	win.flip()
	# core.wait(.5)
	tup = event.waitKeys(maxWait=3, keyList=['1', '2'], clearEvents=True, timeStamped=True)
	# timer = core.Clock()
	# tup = event.waitKeys(maxWait=3, keyList=['1', '2'], clearEvents=True, timeStamped=timer)
	print(tup[0]) # this wont work for null responses!! build in check
	key = tup[0][0]
	print(key)
	responses.append(key)
	time = tup[0][1]
	print(time)
	rts.append(time)
	win.flip()

# i want to build in saving for error trials
responses = []
rts = []
for t in range(3): # python counts from 0!
	im = 'dog_cat/im' + str(t) + '.jpeg'
	dog = visual.ImageStim(win=win, image=im, units="pix", pos=(0,0))
	dog.draw()
	win.flip()
	tup = event.waitKeys(maxWait=3, keyList=['1', '2'], clearEvents=True, timeStamped=core.Clock())
	if tup:
		responses.append(tup[0][0])
		rts.append(tup[0][1])
	else:
		responses.append('NA')
		rts.append(np.nan)
	win.flip()


# we made those response lists, but we didn't do anything to save them, so they're just gone :(
# lets write them to a dataframe and save that as a csv
df = pd.DataFrame({'responses': responses, 'rts': rts})
df.to_csv('data.csv')


# we want to show the same trials to a bunch of subjects - how to read in?
# pandas again
# also, introduce kill switch and try catch
counterbalance = pd.read_csv('counters/counterbalance0.csv')
fixation_cross = visual.ShapeStim(win, vertices=((0, -20), (0, 20), (0,0), (-20,0), (20, 0)),lineWidth=5,closeShape=False,lineColor="white",units="pix")
# # print(counterbalance.head()) # shape1, shape2, shape3
num_trials = len(counterbalance)
responses = []
rts = []
try:
	for index, row in counterbalance.iterrows():
	# for index in range(3):
		row = counterbalance.loc[counterbalance.index == index]
		# print(row['shape1'].values[0])
		s1 = visual.ImageStim(win=win, image='shapes/' + row['shape1'].values[0] + '.png', units="pix", pos=(0,0))
		s2 = visual.ImageStim(win=win, image='shapes/' + row['shape2'].values[0] + '.png', units="pix", pos=(0,0))
		s3 = visual.ImageStim(win=win, image='shapes/' + row['shape3'].values[0] + '.png', units="pix", pos=(0,0))
		s1.draw()
		win.flip()
		core.wait(.5)
		s2.draw()
		win.flip()
		core.wait(.5)
		s3.draw()
		win.flip()
		core.wait(.5)
		win.flip()
		fixation_cross.draw()
		win.flip()
		# wait for a response or a kill command
		response_window = 2
		timer = core.CountdownTimer(response_window) # give 2 seconds to respond
		no_response = True
		timee = response_window
		rt = np.nan
		choice = np.nan
		while no_response and timee > 0:
			timee = timer.getTime()
			for key in event.getKeys():
				if key in ['1', '2']:
					no_response = False
					rt = response_window - timee
					choice = int(key)
				if key in ['k']:
					# killing the game
					# NOTE - DONT HAVE THIS WITHOUT A WAY TO SAVE YOUR DATA, aka a try/except
					print('you elected to kill the game.')
					print(1/0) # just a short hand, lots of ways to do this
		# show feedback
		responses.append(choice)
		rts.append(rt)
		if choice == 1:
			# correct
			t = 'correct'
			c = 'green'
		elif choice == 2:
			# incorrect
			t = 'incorrect'
			c = 'red'
		else:
			# please respond
			t = 'please respond faster'
			c = 'white'
		feedback = visual.TextStim(win, text=t, pos=(450, 0), color=c, units='pix')
		feedback.draw()
		win.flip()
		core.wait(1)
except Exception as e: # this will catch our exception and any other errors
	print(e)
	print('something went wrong :( ')
	print('saving your work...')
finally:
	df = pd.DataFrame({'responses': responses, 'rts': rts})
	df.to_csv('data.csv')









# finish
win.close()


















# eof
