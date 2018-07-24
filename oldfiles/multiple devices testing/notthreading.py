import serial
import queue
import threading

queue = queue.Queue(1000)

def serial_read(s):
	while True:
		line = s.readline()
		queue.put(line)

serial0 = serial.Serial('/dev/tty.usbmodem141441')
serial1 = serial.Serial('/dev/tty.wchusbserial141430')

thread1 = threading.Thread(target=serial_read, args=(serial0,),).start()
thread2 = threading.Thread(target=serial_read, args=(serial1,),).start()

while True:
	if queue.empty():
		pass
	else:
		line = queue.get(True, 1)
		print(line.decode('utf-8'))