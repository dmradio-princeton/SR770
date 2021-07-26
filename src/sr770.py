#!/usr/bin/env python3
import serial
import numpy as np
import sys, os
import matplotlib.pyplot as plt

class SR770:
	"""
	Class for serial communication with SR770
	"""
	port = "/dev/ttyUSB3"
	baud = 9600

	def __init__(self):
		self.serial = serial.Serial( #open the serial port
		SR770.port,
		SR770.baud,
		serial.EIGHTBITS,
		serial.PARITY_NONE
		)

	def initial(self):
		self.serial.write(f'OUTP 0\n'.encode()) #sets the output interface to RS232
		self.serial.write(f'*IDN?\n'.encode()) #queries the device identification

		c = ''
		s = ''
		while c !=b'\r':
			c = self.serial.read(1)
			s += c.decode()
		print(s)

	def measure_psd(self):
		data = np.empty((0,2))

		self.serial.write(b'SPAN 19\n') #set the entire frequency span = 100kHz
		self.serial.write(b'MEAS -1, 1\n') #set the measurement type to PSD
		self.serial.write(b'MBIN -1, 0\n') #move the trace marker region to i=0 bin
		for i in range(400):

			self.serial.write(f'BVAL? -1, {i}\n'.encode()) #measure marker X position
			c = ''
			s_x = ''
			while c !=b'\r':
				c = self.serial.read(1)
				s_x += c.decode()

			sys.stdout.write("{}".format(s_x))

			self.serial.write(f'SPEC? -1, {i}\n'.encode()) #measure marker Y position
			c = ''
			s_y = ''
			while c !=b'\r':
				c = self.serial.read(1)
				s_y += c.decode()


			new_data = np.array([[ float(str(s_x).rstrip()), float(str(s_y).rstrip()) ]])
			data = np.append(data, new_data, axis=0)

			self.serial.write(f'MBIN -1, {i}\n'.encode()) #move the trace marker region to i=0 bin


		dir_path = 'data'
		if not os.path.exists(dir_path):
				os.makedirs(dir_path)

		file_path = os.path.join(dir_path, 'spectrum.dat')

		file = open(file_path, 'w')

		#write the data to a file
		for i in range(400):
			file.write(str(data[i,0]) + " " + str(data[i,1]) + "\n")
		file.close()

		plt.plot(data[:,0], data[:,1])
		plt.yscale('log')
		plt.savefig('data.pdf')


if __name__ == '__main__':
	dev = SR770()
	dev.initial()
	dev.measure_psd()

	dev.serial.close() #close the serial port
