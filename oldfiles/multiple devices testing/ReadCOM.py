import sys
import serial

ser = serial.Serial(port=sys.argv[1],baudrate=int(sys.argv[2]))
while True:  # The program never ends... will be killed when master is over.
    # sys.stdin.readline()

    ser.write('serial command here\n') # send command to serial port
    output = ser.readline() # read output

    sys.stdout.write(output) # write output to stdout
    sys.stdout.flush()