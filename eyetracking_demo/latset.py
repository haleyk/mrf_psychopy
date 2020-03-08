from __future__ import print_function
from __future__ import division

import sys, getopt
from psychopy import visual, monitors
from psychopy.visual import Window
from psychopy import core, event
from pandas import DataFrame
import csv
from math import atan2, degrees
import pygaze
from pygaze.display import Display
from pygaze.eyetracker import EyeTracker

from supportFunctions import *

if __name__ == "__main__":
	subjnum = int(sys.argv[1:][0])

which_monitor = "haley_small"
testing = True #make this true to run a short version of the game

seconds_tostartup = core.getTime()
print("Seconds to startup: ", seconds_tostartup)

#Settings
repeatInstructions = True #want to read instructions at least once
train = 8
blockLen = 32
numBlocks = 6
nT = (blockLen * numBlocks) +  train

#start data holders
responses = []
rts = []
correct = []
allTrials = []
hands = []

rand = int(subjnum)
rand5 = int(subjnum) % 5
with open('counters/counterbalance' + str(rand5) +'.csv') as csvfile:
# with open('task_permutations/lat_permuts' + str(rand5) + '.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		allTrials.append(row)
print("Subject Number: " + str(subjnum))

LOGFILENAME = 'textlog_subject_' + str(subjnum)
# LOGFILENAME = 'subject_0'
LOGFILE = 'eyetracking_logs/' + LOGFILENAME

version = int(subjnum) % 4
if version < 2:
	counter = 'A' # set - no set
if version > 1:
	counter = 'B' # no set - set
if version % 2 == 0:
	hand_pattern = 'RLRLRLRL' #two practice + 6 blocks
if version % 2 == 1:
	hand_pattern = 'LRLRLRLR'

if testing:
	allTrials = allTrials[0:8]
	blockLen = 2
	nT = 14
	train = 2

# if which_monitor == "eyetracker":
	# win = visual.Window([1280,1024], monitor="tobii", units="deg",color='white',fullscr=False)
# elif which_monitor == "haley_small":
	# win = visual.Window([1080, 675], monitor="haleys", units="deg",color='white',fullscr=False)

# Initialise a new Display instance
disp = Display(disptype='psychopy', dispsize=(1280,1024),bgc=(255,255,255,255))

# Initialise a new EyeTracker instance
tracker = EyeTracker(disp, trackertype='tobii')
tracker.fixtresh = 1.5
tracker.calibrate()

win = pygaze.expdisplay
win.mouseVisible = False

fixation = visual.ShapeStim(win, vertices=((0, -15), (0, 15), (0,0), (-15,0), (15, 0)),lineWidth=5,closeShape=False,lineColor="black")

tracker.start_recording()

#practice loop
while repeatInstructions:

	numTrialsCompleted = 0

	stim = visual.TextStim(win, getInstructions('start1'),  color='black',pos=(0,100),height=30,wrapWidth=800)
	stim.draw()
	win.flip()
	event.waitKeys(keyList=['space'])

	stim = visual.TextStim(win, getInstructions('start2'),  color='black',pos=(0,100),height=30,wrapWidth=800)
	stim.draw()
	win.flip()
	event.waitKeys(keyList=['space'])

	stim = visual.TextStim(win, getInstructions('start3'), color='black', pos=(0,200),height=30,wrapWidth=800)
	stim.draw()
	v = visual.ImageStim(win=win, image='instructions/in3.png', pos=(0,-200))
	v.draw()
	win.flip()
	event.waitKeys(keyList=['space'])

	stim = visual.TextStim(win, getInstructions('start4'), color='black',pos=(0,100),height=30,wrapWidth=800)
	stim.draw()
	win.flip()
	event.waitKeys(keyList=['space'])

	stim = visual.TextStim(win, getInstructions('start5'), color='black',height=30,wrapWidth=800,pos=(0,100))
	stim.draw()
	win.flip()
	event.waitKeys(keyList=['space'])

	stim = visual.TextStim(win, getInstructions('start6'), color='black',height=30,wrapWidth=800,pos=(0,100))
	stim.draw()
	v = visual.ImageStim(win=win, image='instructions/in6.png', pos=(0,-100))
	v.draw()
	win.flip()
	event.waitKeys(keyList=['space'])

	stim = visual.TextStim(win, getInstructions('start7'), color='black',height=30,wrapWidth=800,pos=(0,100))
	stim.draw()
	v = visual.ImageStim(win=win, image='instructions/in7.png', pos=(0,-100))
	v.draw()
	win.flip()
	event.waitKeys(keyList=['space'])

	stim = visual.TextStim(win, getInstructions('start8'), color='black',height=30,wrapWidth=800,pos=(0,100))
	stim.draw()
	v = visual.ImageStim(win=win, image='instructions/in8.png', pos=(0,-100))
	v.draw()
	win.flip()
	event.waitKeys(keyList=['space'])

	stim = visual.TextStim(win, getInstructions('start9'), color='black',height=30,wrapWidth=800,pos=(0,100))
	stim.draw()
	win.flip()
	event.waitKeys(keyList=['space'])

	stim = visual.TextStim(win, getInstructions('start10'), color='black',height=30,wrapWidth=800,pos=(0,200))
	stim.draw()
	v = visual.ImageStim(win=win, image='instructions/in10.png', pos=(0,-100))
	v.draw()
	win.flip()
	event.waitKeys(keyList=['space'])

	stim = visual.TextStim(win, getInstructions('start11'), color='black',height=30,wrapWidth=800,pos=(0,200))
	stim.draw()
	v = visual.ImageStim(win=win, image='instructions/in11.png', pos=(0,-100))
	v.draw()
	win.flip()
	event.waitKeys(keyList=['space'])

	hand_start = 'LEFT' if hand_pattern[0] == 'L' else 'RIGHT'
	stim = visual.TextStim(win, getInstructions('start12', other=hand_start), color='black',height=30,wrapWidth=800,pos=(0,100))
	stim.draw()
	win.flip()
	event.waitKeys(keyList=['space'])

	stim = visual.TextStim(win, getInstructions('practice'),color='black',height=30,wrapWidth=800,pos=(0,100))
	stim.draw()
	win.flip()
	event.waitKeys(keyList=['space'])

	for trial in allTrials[0:int(train/2)]:
		choice, rt, cor = mainloop(win, trial, fixation, counter, fb=True, fixationTime=.5, stimTime=.3,tracker=tracker,trialNum=numTrialsCompleted)
		responses.append(choice)
		rts.append(rt)
		correct.append(cor)
		hands.append(hand_pattern[0])
		numTrialsCompleted += 1

	stim = visual.TextStim(win, getInstructions('practice2'),color='black',height=30,wrapWidth=800,pos=(0,100))
	stim.draw()
	win.flip()
	wait_for_click(win)

	for trial in allTrials[int(train/2):train]:
		choice, rt, cor = mainloop(win, trial, fixation, counter, fb=True,tracker=tracker,trialNum=numTrialsCompleted)
		responses.append(choice)
		rts.append(rt)
		correct.append(cor)
		hands.append(hand_pattern[1])
		numTrialsCompleted += 1

	stim = visual.TextStim(win, getInstructions('ready'),color='black',height=30,wrapWidth=800,pos=(0,100))
	stim.draw()
	win.flip()
	keys = event.waitKeys(keyList=['r', 'space'])
	if 'r' in keys:
		repeatInstructions = True
		numTrialsCompleted = 0
	else:
		repeatInstructions = False

seconds_totesting = core.getTime()
print("Seconds to testing phase: ", seconds_totesting)

#main loop
curTrial = train
bl = 1
try:
	#while (curTrial + blockLen <= nT):
	while curTrial <= nT:
		tracker.log('block_' + str(bl))
		tracker.calibrate()
		tracker.start_recording()
		for trial in allTrials[curTrial:curTrial + blockLen]:
			choice, rt, cor = mainloop(win, trial, fixation, counter,tracker=tracker,trialNum=numTrialsCompleted)
			responses.append(choice)
			rts.append(rt)
			correct.append(cor)
			hands.append(hand_pattern[bl+1])
			numTrialsCompleted += 1
		if bl < 6:
			stim = visual.TextStim(win, getInstructions('interblock', block_name(bl)), color='black',height=30,wrapWidth=800)
			stim.draw()
			win.flip()
			event.waitKeys(keyList=['space'])
		curTrial += blockLen
		bl += 1

except Exception as e:
	print("something went wrong :( ")
	print(str(e))
finally:
	#write the data, regardless of when you end
	d = {'response': responses, 'rt': rts, 'correct': correct, 'block': [t['block'] for t in allTrials[0:numTrialsCompleted]], \
		'hand': hands, 'presentation': [t['presentation'] for t in allTrials[0:numTrialsCompleted]], \
		'shape1': [t['shape1'] for t in allTrials[0:numTrialsCompleted]], 'shape2': [t['shape2'] for t in allTrials[0:numTrialsCompleted]], \
		'shape3': [t['shape3'] for t in allTrials[0:numTrialsCompleted]], 'span': [t['span'] for t in allTrials[0:numTrialsCompleted]], \
		'is_set': [t['is_set'] for t in allTrials[0:numTrialsCompleted]], 'train_test': [t['train_test'] for t in allTrials[0:numTrialsCompleted]]}
	df = DataFrame(d)
	subjfile = 'log/subj' + str(subjnum) + '.xlsx'
	df.to_excel(subjfile, index=False)

seconds_elapsed = core.getTime()
print("Seconds Elapsed: ", seconds_elapsed) #prints number of seconds it took to complete task
print(" ")

total_time = (seconds_elapsed - seconds_tostartup) / 60
testing_time = (seconds_elapsed - seconds_totesting) / 60
print("Total Time in Minutes: ", total_time)
print("Testing Time in Minutes: ", testing_time)


stim = visual.TextStim(win, getInstructions('finish'), color='black',height=30,wrapWidth=800,pos=(0,100))
stim.draw()
win.flip()
event.waitKeys()


tracker.stop_recording()

# Close the connection to the EyeTracker
# (This will also close the log files.)
tracker.close()


all_rows_eye = []
with open('default_TOBII_output.tsv') as lena:
	reader = csv.DictReader(lena, delimiter='\t')
	for row in reader:
		all_rows_eye.append(row)


#start all of these as nonsense to make sure they get updated
time_stamp = 0
trial_num = -1 #these start at 0 but get a +1 each time so the first is 0
block_num = 0
current_stimulus = 'instructions'
subject_ID = subjnum
trial_span = 999
trial_shape_1 = 999
trial_shape_2 = 999
trial_shape_3 = 999
trial_reaction_time = 999
trial_lateralization = 999
current_stim_start_time = 999
trial_bad_eyetracking = 0
trial_correct = -1
trial_resp = 'none'
trial_trainTest = 'none'
trial_cresp = 'none'

def isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

def parse(event_string):
	"""
	I'm assuming all event_strings will come in as 'something_like_this' and that I can split it at the _ parts and each word will be important information.
	For example, the first word will either be block, trial, or stimulus.
	And then if the first word is stimulus, the second word will be what type of stimulus it is
	But you can make them whatever logs you want as long as you can decode them uniquely!
	"""
	global time_stamp
	global trial_num
	global block_num
	global current_stimulus
	global trial_shape_1
	global trial_shape_2
	global trial_shape_3
	global trial_reaction_time
	global trial_lateralization
	global trial_bad_eyetracking
	global current_stim_start_time
	global allTrials
	global trial_correct
	global trial_resp
	global trial_trainTest
	global trial_cresp
	global trial_span

	event_tag = event_string.split('_')[0] #will split at each _ and choose the first word

	if event_tag == 'block':
		block_num += 1
	if event_tag == 'trial':
		trial_num += 1
		if trial_num >= len(correct):
			trial_correct = 'NA'
			trial_span = 'NA'
			trial_shape_1 = 'NA'
			trial_shape_2 = 'NA'
			trial_shape_3 = 'NA'
			trial_reaction_time = 'NA'
			trial_lateralization = 'NA'
			trial_resp = 'NA'
			trial_cresp = 'NA'
			trial_bad_eyetracking = 'NA'
			trial_trainTest = 'NA'
		else:
			trial_correct = correct[trial_num]
			trial_span = allTrials[trial_num]['span']
			trial_shape_1 = allTrials[trial_num]['shape1']
			trial_shape_2 = allTrials[trial_num]['shape2']
			trial_shape_3 = allTrials[trial_num]['shape3']
			trial_reaction_time = rts[trial_num]
			trial_lateralization = allTrials[trial_num]['lateralization']
			trial_resp = responses[trial_num]
			trial_cresp = 'set' if allTrials[trial_num]['is_set'] else 'no_set'
			trial_bad_eyetracking = 0
			trial_trainTest = allTrials[trial_num]['train_test']
	if event_tag == 'stim':
		current_stimulus = event_string.split('_')[1]
		current_stim_start_time = time_stamp
	if event_tag == 'manual':
		trial_bad_eyetracking = 1

print("nothing below here works yet")
print(1/0)

filename = 'eyetracking_logs/subj_' + str(subjnum) + '.csv'

calibration_info = {}
calibration_index = 0

with open(filename, 'wb') as myFile:
	writer = csv.writer(myFile)
	writer.writerow(['subject_ID', 'time_stamp', 'GazePointXLeft','GazePointYLeft','ValidityLeft', 'GazePointXRight', \
						'GazePointYRight','ValidityRight','GazePointX','GazePointY','PupilSizeLeft','PupilValidityLeft','PupilSizeRight','PupilValidityRight',
						'trial_num', \
						'trial_cresp', \
						'trial_resp', \
						'trial_correct', \
						'trial_reaction_time', 'trial_span',\
						'trial_trainTest', \
						'trial_lateralization', \
						'trial_shape_1', 'trial_shape_2', 'trial_shape_3', 'current_stimulus', 'block_num', \
						'current_stim_start_time', 'trial_bad_eyetracking'])
	for row in all_rows_eye: #for each row
		for j,k in row.items(): #there are 2 things, the time stamp and the row of either an event or eyetracking data
			if isinstance(k, str): #this is the time stamp OR a calibration report
				if isfloat(k): #its the timestamp
					time_stamp = k
				else: # it's part of a calibration
					calibration_info[calibration_index] = k
					calibration_index +=1
			elif isinstance(k, list) and len(k[0]): #is there an event?
				parse(k[0]) #update global values
			else: #there isn't an event -- lets write out the data with the globals we already have
				# need to make the list every time because the values are static and not pointers, python is weird
				list_of_globals = [trial_num, trial_cresp, trial_resp, trial_correct, trial_reaction_time, trial_span, \
									trial_trainTest, trial_lateralization, trial_shape_1, \
									trial_shape_2, trial_shape_3, current_stimulus, block_num, current_stim_start_time, trial_bad_eyetracking]
				whole_row = [subject_ID] + [time_stamp] + k[1:] + list_of_globals

				writer.writerow(whole_row)

filename_calib = 'eyetracking_logs/calib_' + str(subjnum) + '.txt'

file = open(filename_calib, 'w')
for key,val in calibration_info.items():
	file.write(str(val) + '\n')
file.close()

print('finished :)')

#cleanup
core.quit()

# Close the active Window
disp.close()
