#Based in part on Pianoputer by Zulko
#https://github.com/Zulko/pianoputer
#http://zulko.github.io/blog/2014/03/29/soundstretching-and-pitch-shifting-in-python/

import serial
from scipy.io import wavfile
import argparse
import numpy as np
import pygame
from pygame.locals import *
import sys
import warnings

# serialinterface = "COM3"
serialinterface = "/dev/tty.usbmodem1431"

def speedx(snd_array, factor):
	""" Speeds up / slows down a sound, by some factor. """
	indices = np.round(np.arange(0, len(snd_array), factor))
	indices = indices[indices < len(snd_array)].astype(int)
	return snd_array[indices]


def stretch(snd_array, factor, window_size, h):
	""" Stretches/shortens a sound, by some factor. """
	phase = np.zeros(window_size)
	hanning_window = np.hanning(window_size)
	result = np.zeros(int(len(snd_array) / factor + window_size))

	for i in np.arange(0, len(snd_array) - (window_size + h), h*factor):
		i = int(i)
		# Two potentially overlapping subarrays
		a1 = snd_array[i: i + window_size]
		a2 = snd_array[i + h: i + window_size + h]

		# The spectra of these arrays
		s1 = np.fft.fft(hanning_window * a1)
		s2 = np.fft.fft(hanning_window * a2)

		# Rephase all frequencies
		phase = (phase + np.angle(s2/s1)) % 2*np.pi

		a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
		i2 = int(i/factor)
		result[i2: i2 + window_size] += hanning_window*a2_rephased.real

	# normalize (16bit)
	result = ((2**(16-4)) * result/result.max())

	return result.astype('int16')


def pitchshift(snd_array, n, window_size=2**13, h=2**11):
	""" Changes the pitch of a sound by ``n`` semitones. """
	factor = 2**(1.0 * n / 12.0)
	stretched = stretch(snd_array, 1.0/factor, window_size, h)
	return speedx(stretched[window_size:], factor)


def parse_arguments():
	description = ('Computer connection program to the Microtonal Synth')

	parser = argparse.ArgumentParser(description=description)
	parser.add_argument(
		'--wav', '-w',
		metavar='FILE',
		type=argparse.FileType('r'),
		default='sine.wav',
		help='WAV file (default: sine.wav)')
	# parser.add_argument(
	# 	'--keyboard', '-k',
	# 	metavar='FILE',
	# 	type=argparse.FileType('r'),
	# 	default='typewriter.kb',
	# 	help='keyboard file (default: typewriter.kb)')
	parser.add_argument(
		'--verbose', '-v',
		action='store_true',
		help='verbose mode')
	parser.add_argument(
		'--serialdebug', '-s',
		action='store_true',
		help='Check the arduino connection')

	return (parser.parse_args(), parser)




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

	fps, sound = wavfile.read(args.wav.name)
	while True:
		line = (ser.readline()).decode('utf-8')
		if line[0] == "i":
			buttonCount = int(line[1])
			print("{} buttons registered.".format(buttonCount))
			break
	tones = range((buttonCount//2)*-1, buttonCount//2)
	sys.stdout.write('Transponding sound file... ')
	sys.stdout.flush()
	transposed_sounds = [pitchshift(sound, n) for n in tones]
	print('DONE')

	# So flexible ;)
	pygame.mixer.init(fps, -16, 1, 2048)
	# For the focus
	screen = pygame.display.set_mode((150, 150))

	keys = []
	for i in range(buttonCount):
		keys.append(i)
	print(keys)
	sounds = map(pygame.sndarray.make_sound, transposed_sounds)
	key_sound = dict(zip(keys, sounds))
	is_playing = {k: False for k in keys}

	while True:
		line = (ser.readline()).decode('utf-8')

		if line[0] == "e":
			raise KeyboardInterrupt

		if line[0] == "n":
			line = line[1:].split()
			board = int(line[0])
			key = int(line[1])
			value = int(line[2])

			if value == 1:
				if (key in key_sound.keys()) and (not is_playing[key]):
					key_sound[key].play(fade_ms=50)
					is_playing[key] = True
					print("Key {} {}".format(key, "On"))
			if value == 0:
				key_sound[key].fadeout(200)
				is_playing[key] = False
				print("Key {} {}".format(key, "Off"))


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		ser.close()
		print('Goodbye')