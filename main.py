# Multiple Microcontroller controller for MIDI Interface

# Useful resource
# http://www.elvenminstrel.com/music/tuning/reference/pitchbends.shtml

# /usr/local/bin/python3
#!env/bin/python3

import serial
import queue, threading
import argparse
# import pygame
# from pygame.locals import *
import sys
import warnings
import os
import logging
import time

# Local modules
from midioutwrapper import *
from midi_classes import *



# COM Ports of uCs
# TODO: uC port names through args
serialinterfaces = ["/dev/tty.wchusbserial141430", '/dev/tty.wchusbserial141420']


# Initialise Queue
q = queue.Queue(1000)

# TODO: Should a board class be created?
# class Board:
# 	def __init__(self, boardNo, buttonCount):
# 		self.boardNo = boardNo
# 		self.buttonCount = buttonCount



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

def serial_debug():
	""" Initialise uCs and print interpreted events """
	while True:
		if q.empty():
			pass
		else:
			# Get next line from queue
			line = (q.get(True, 1)).decode('utf-8')

			
			if line[0] == "i":
				# 'Initialise' signal received
				line = line[1:].split()
				buttonCount = line[0]
				board = line[1]
				print("{} buttons registered on Board {}.".format(buttonCount, board))
			
			
			if line[0] == "n":
				# Note event received
				line = line[1:].split()
				board = line[0]
				note = line[1]
				value = int(line[2])
				print("Board {} Note {} {}".format(board, note, "On" if value==1 else "Off"))

def init_boards():
	""" Wait for uCs to initialise and return button amounts """
	initialisedBoards = 0

	# TODO: Flexible board amount support
	board0buttons = 0
	board1buttons = 0

	while True:
		if q.empty():
			pass
		else:
			# Get next serial line from queue
			line = (q.get(True, 1)).decode('utf-8')

			# init signal received
			if line[0] == "i":
				line = line[1:].split()
				board = int(line[1])
				buttons = int(line[0])
				if board == 0:
					board0buttons = buttons
				if board == 1:
					board1buttons = buttons
				print("{} buttons registered on Board {}.".format(line[0], line[1]))
				initialisedBoards += 1
				# Only continue once two boards are initialised.
				# TODO: Add support for different board amounts through args.
				if initialisedBoards == 2:
					break

	return board0buttons, board1buttons



def serial_read(s):
	# Continuously read from serial devices
	# Used for threading
	while True:
		line = s.readline()
		q.put(line)


def main():

	# Initialise the two serial interfaces
	serial0 = serial.Serial(serialinterfaces[0])
	serial1 = serial.Serial(serialinterfaces[1])

	# Keep two threads adding incoming serial lines to the queue to parse
	thread1 = threading.Thread(target=serial_read, args=(serial0,),).start()
	thread2 = threading.Thread(target=serial_read, args=(serial1,),).start()

	# Parse command line arguments
	(args, parser) = parse_arguments()


	# Debug serial connection without initialising MIDI 
	if args.serialdebug:
		serial_debug()

	# Initialise uCs, and get the button amounts from each
	board0buttons, board1buttons = init_boards()

	buttonCount = board0buttons + board1buttons

	# TODO: Initialise note objects from csv file (from args)

	while True:
		if q.empty():
			pass
		else:
			# Get next serial line from queue
			line = (q.get(True, 1)).decode('utf-8')

			# Quit event
			if line[0] == "e":
				raise KeyboardInterrupt

			# Note event
			if line[0] == "n":
				line = line[1:].split()
				board, key, value = int(line[0]), int(line[1]), int(line[2])
				# If button is on board one, add the first boards buttons
				key += board * board0buttons

				# TODO: Map key to Note classes

				if value == 1:
					# Note on event
					pass
				else:
					# Note off event
					pass

				


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('Goodbye')

