#!/usr/local/bin/python3
import math

# notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
# numbers = list('01234567')
# tonelist = ['0B5', '0B6', '0B7']

# # try:
# #   totaloctaves = int(input("How many octaves to generate? "))
# # except ValueError:
# #   print("Enter an integer. Try again.")

# totaloctaves = 1

# octave = 0
# while True:
# 	for i in range(len(notes)):
# 		workingNote = notes[i+3] if octave == 0 else notes[i]
# 		for j in range(len(numbers)):
# 			workingNumber = numbers[j]
# 			tonelist.append('{}{}{}'.format(octave, workingNote, workingNumber))
# 		if octave == 0 and notes[i+3] == "G#":
# 			octave += 1
# 			break
# 		if octave != 0 and notes[i] == "G#":
# 			octave += 1
# 			break
# 	if octave == totaloctaves:
# 		for i in range(len(notes)-8):
# 			workingNote = notes[i]
# 			for j in range(len(numbers) if workingNote != "C" else 5):
# 				workingNumber = numbers[j]
# 				tonelist.append('{}{}{}'.format(octave, workingNote, workingNumber))
# 		break

finaldict = {}
finallist = []
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
aFreq = 440.0

currentFreq = 

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
	# currentFreq += 12.5
print(finaldict)
