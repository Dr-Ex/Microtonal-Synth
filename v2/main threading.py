#Based in part on Pianoputer by Zulko
#https://github.com/Zulko/pianoputer
#http://zulko.github.io/blog/2014/03/29/soundstretching-and-pitch-shifting-in-python/
#Also Cowbell by dr_ex and Lysenthia
#https://github.com/Dr-Ex/Cowbell

#!/usr/local/bin/python3

import serial
import queue, threading
from scipy.io import wavfile
import argparse
import numpy as np
import pygame
from pygame.locals import *
import sys
import warnings
import os

# serialinterface = "COM3"
serialinterface = "/dev/tty.wchusbserial141430"
serialinterfaces = ["/dev/tty.wchusbserial143430", '/dev/tty.usbmodem143441']

q = queue.Queue(1000)

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

class Board:
	def __init__(self, boardNo, buttonCount):
		self.boardNo = boardNo
		self.buttonCount = buttonCount

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
		q.put(line)

def main():
	serial0 = serial.Serial(serialinterfaces[0])
	serial1 = serial.Serial(serialinterfaces[1])

	thread1 = threading.Thread(target=serial_read, args=(serial0,),).start()
	thread2 = threading.Thread(target=serial_read, args=(serial1,),).start()

	# Parse command line arguments
	(args, parser) = parse_arguments()

	# ARDUINO CONNECTION DEBUGGING
	if args.serialdebug:
		# ser = serial.Serial(serialinterface, 9600)
		while True:
			if q.empty():
				pass
			else:
				line = (q.get(True, 1)).decode('utf-8')
				if line[0] == "i":
					line = line[1:].split()
					buttonCount = line[0]
					board = line[1]
					print("{} buttons registered on Board {}.".format(buttonCount, board))
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

	# while True:
	# 	line = (ser.readline()).decode('utf-8')
	# 	if line[0] == "i":
	# 		buttonCount = int(line[1])
	# 		print("{} buttons registered.".format(buttonCount))
	# 		break
	initiatedBoards = 0
	board0buttons = 0
	board1buttons = 0
	while True:
		if q.empty():
			pass
		else:
			line = (q.get(True, 1)).decode('utf-8')
			if line[0] == "i":
				line = line[1:].split()
				board = int(line[1])
				buttons = int(line[0])
				if board == 0:
					board0buttons = buttons
				if board == 1:
					board1buttons = buttons
				print("{} buttons registered on Board {}.".format(line[0], line[1]))
				initiatedBoards += 1
				if initiatedBoards == 2:
					break



	buttonCount = board0buttons + board1buttons
	# So flexible ;)
	pygame.mixer.init(44100, -16, 1, 2048)
	# For the focus
	screen = pygame.display.set_mode((150, 150))

	tonedir = "tones/"
	notes = {}
	print("Registering notes...")

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
		if q.empty():
			pass
		else:
			line = (q.get(True, 1)).decode('utf-8')

			if line[0] == "e":
				raise KeyboardInterrupt

			if line[0] == "n":
				line = line[1:].split()
				board = int(line[0])
				key = int(line[1])
				value = int(line[2])

				if board == 1:
					key += board0buttons

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
