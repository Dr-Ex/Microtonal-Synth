#!/usr/local/bin/python3
import math

notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
numbers = list('01234567')
tonelist = ['0B5', '0B6', '0B7']

# try:
#   totaloctaves = int(input("How many octaves to generate? "))
# except ValueError:
#   print("Enter an integer. Try again.")

totaloctaves = 1

octave = 0
while True:
	for i in range(len(notes)):
		workingNote = notes[i+3] if octave == 0 else notes[i]
		for j in range(len(numbers)):
			workingNumber = numbers[j]
			tonelist.append('{}{}{}'.format(octave, workingNote, workingNumber))
		if octave == 0 and notes[i+3] == "G#":
			octave += 1
			break
		if octave != 0 and notes[i] == "G#":
			octave += 1
			break
	if octave == totaloctaves:
		for i in range(len(notes)-8):
			workingNote = notes[i]
			for j in range(len(numbers) if workingNote != "C" else 5):
				workingNumber = numbers[j]
				tonelist.append('{}{}{}'.format(octave, workingNote, workingNumber))
		break

finaldict = {}
# tonelist = ['0B5', '0B6', '0B7',
#             '1C0', '1C1', '1C2', '1C3', '1C4', '1C5', '1C6', '1C7',
#             '1C#0', '1C#1', '1C#2', '1C#3', '1C#4', '1C#5', '1C#6', '1C#7',
#             '1D0', '1D1', '1D2', '1D3', '1D4', '1D5', '1D6', '1D7',
#             '1D#0', '1D#1', '1D#2', '1D#3', '1D#4', '1D#5', '1D#6', '1D#7',
#             '1E0', '1E1', '1E2', '1E3', '1E4', '1E5', '1E6', '1E7',
#             '1F0', '1F1', '1F2', '1F3', '1F4', '1F5', '1F6', '1F7',
#             '1F#0', '1F#1', '1F#2', '1F#3', '1F#4', '1F#5', '1F#6', '1F#7',
#             '1G0', '1G1', '1G2', '1G3', '1G4', '1G5', '1G6', '1G7',
#             '1G#0', '1G#1', '1G#2', '1G#3', '1G#4', '1G#5', '1G#6', '1G#7',
#             '1A0', '1A1', '1A2', '1A3', '1A4', '1A5', '1A6', '1A7',
#             '1A#0', '1A#1', '1A#2', '1A#3', '1A#4', '1A#5', '1A#6', '1A#7',
#             '1B0', '1B1', '1B2', '1B3', '1B4', '1B5', '1B6', '1B7',
#             '2C0', '2C1', '2C2', '2C3', '2C4']
aFreq = 440.0

currentFreq = aFreq
for i in range(len(tonelist)-29):
	# newFreq = round(currentFreq * (2 ** (-12.5/1200)), 2)
	newFreq = round(currentFreq*(2**(1/96)), 2)
	finaldict[tonelist[74-i]] = newFreq
	currentFreq = newFreq

currentFreq = aFreq
for i in range(len(tonelist)-75):
	# newFreq = round((2 ** ((12.5/1200) + math.log(currentFreq, 2))), 2)
	newFreq = round(currentFreq/(2**(1/96)))
	finaldict[tonelist[i+75]] = currentFreq
	currentFreq += 12.5
print(finaldict)
