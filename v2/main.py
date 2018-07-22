#Based in part on Pianoputer by Zulko
#https://github.com/Zulko/pianoputer
#http://zulko.github.io/blog/2014/03/29/soundstretching-and-pitch-shifting-in-python/
#Also Cowbell by dr_ex and Lysenthia
#https://github.com/Dr-Ex/Cowbell

#!/usr/local/bin/python3

import serial
# import Queue
# import threading
from scipy.io import wavfile
import argparse
import numpy as np
import pygame
from pygame.locals import *
import sys
import warnings
import os

# serialinterface = "COM3"
serialinterface = "/dev/tty.wchusbserial1430"

tonelist = ['0B5', '0B6', '0B7',
            '0C0', '0C1', '0C2', '0C3', '0C4', '0C5', '0C6', '0C7',
            '0C#0', '0C#1', '0C#2', '0C#3', '0C#4', '0C#5', '0C#6', '0C#7',
            '0D0', '0D1', '0D2', '0D3', '0D4', '0D5', '0D6', '0D7',
            '0D#0', '0D#1', '0D#2', '0D#3', '0D#4', '0D#5', '0D#6', '0D#7',
            '0E0', '0E1', '0E2', '0E3', '0E4', '0E5', '0E6', '0E7',
            '0F0', '0F1', '0F2', '0F3', '0F4', '0F5', '0F6', '0F7',
            '0F#0', '0F#1', '0F#2', '0F#3', '0F#4', '0F#5', '0F#6', '0F#7',
            '0G0', '0G1', '0G2', '0G3', '0G4', '0G5', '0G6', '0G7',
            '0G#0', '0G#1', '0G#2', '0G#3', '0G#4', '0G#5', '0G#6', '0G#7',
            '1A0', '1A1', '1A2', '1A3', '1A4', '1A5', '1A6', '1A7',
            '1A#0', '1A#1', '1A#2', '1A#3', '1A#4', '1A#5', '1A#6', '1A#7',
            '1B0', '1B1', '1B2', '1B3', '1B4', '1B5', '1B6', '1B7',
            '1C0', '1C1', '1C2', '1C3', '1C4']

def parse_arguments():
	description = ('Computer connection program to the Microtonal Synth')

	parser = argparse.ArgumentParser(description=description)
	parser.add_argument(
		'--verbose', '-v',
		action='store_true',
		help='verbose mode')
	parser.add_argument(
		'--serialdebug', '-s',
		action='store_true',
		help='Check the arduino connection')

	return (parser.parse_args(), parser)

def serial_read(s):
	while True:
		line = s.readline()
		queue.put(line)

def main():
	ser = serial.Serial(serialinterface, 9600)

	# Parse command line arguments
	(args, parser) = parse_arguments()

	# ARDUINO CONNECTION DEBUGGING
	if args.serialdebug:
		ser = serial.Serial(serialinterface, 9600)
		while True:
			line = (ser.readline()).decode('utf-8')
			if line[0] == "i":

				buttonCount = line[1]
				print("{} buttons registered.".format(buttonCount))
			if line[0] == "n":
				line = line[1:].split()
				board = line[0]
				note = line[1]
				value = int(line[2])
				print("Board {} Note {} {}".format(board, note, "On" if value==1 else "Off"))

	# Enable warnings from scipy if requested
	if not args.verbose:
		warnings.simplefilter('ignore')

	# fps, sound = wavfile.read(args.wav.name)
	while True:
		line = (ser.readline()).decode('utf-8')
		if line[0] == "i":
			buttonCount = int(line[1])
			print("{} buttons registered.".format(buttonCount))
			break

	# So flexible ;)
	pygame.mixer.init(44100, -16, 1, 2048)
	# For the focus
	screen = pygame.display.set_mode((150, 150))

	tonedir = "tones/"
	notes = {}
	print("Registering notes...")

	# for file in os.listdir(tonedir):
	# 	if os.path.isfile(os.path.join(tonedir, file)) and file[-4:] == ".wav":
	# 		note = file[:-4]
	# 		# print(note)
	# 		# print(tonedir)
	# 		# print(file)
	# 		# fps, tone = wavfile.read("{}{}".format(tonedir, file))
	# 		soundID = pygame.mixer.Sound(tonedir + file)
	# 		notes[note] = soundID
	# 	if len(notes) == buttonCount:
	# 		break

	for i in range(len(tonelist)):
		note = tonelist[i]
		soundID = pygame.mixer.Sound(tonedir + note + ".wav")
		notes[note] = soundID
		if len(notes) == buttonCount:
			break
			
	print("{} notes registered".format(len(notes)))

	keys = []
	for i in range(buttonCount):
		keys.append(i)
	# sounds = map(pygame.sndarray.make_sound, transposed_sounds)
	key_sound = dict(zip(keys, notes))
	is_playing = {k: False for k in keys}

	print("Ready")

	while True:
		line = (ser.readline()).decode('utf-8')

		if line[0] == "e":
			raise KeyboardInterrupt

		if line[0] == "n":
			line = line[1:].split()
			board = int(line[0])
			key = int(line[1])
			value = int(line[2])


			# The notes turn on but then it doesnt register key offs eek
			# Also the notes are out of order too
			if value == 1:
				if (key in key_sound.keys()) and (not is_playing[key]):
					# pygame.mixer.Sound(notes[key_sound[key]]).play(fade_ms=50)
					notes[key_sound[key]].play(fade_ms=50)
					is_playing[key] = True
					print("Key {} {}".format(key, "On"))
			if value == 0:
				if (key in key_sound.keys()) and (is_playing[key]):
					# pygame.mixer.Sound(notes[key_sound[key]]).fadeout(50)
					notes[key_sound[key]].fadeout(200)
					is_playing[key] = False
					print("Key {} {}".format(key, "Off"))


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('Goodbye')
