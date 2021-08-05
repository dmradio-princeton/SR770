#!/usr/bin/env python3
import os
import shutil

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import serial


class SR770:
	"""
	Class for serial communication with SR770
	"""
	port = "/dev/ttyUSB3"
	baud = 9600

	def __init__(self):
		self.serial = serial.Serial(  # open the serial port
			SR770.port,
			SR770.baud,
			serial.EIGHTBITS,
			serial.PARITY_NONE)

		self.freq_array = np.linspace(250, 100000, 400, dtype=float)

	def initial(self):
		self.serial.write(f'OUTP 0\n'.encode())  # sets the output interface to RS232
		self.serial.write(f'*IDN?\n'.encode())  # queries the device identification

		c = ''
		s = ''
		while c != b'\r':
			c = self.serial.read(1)
			s += c.decode()
		print(s)

	def clear(self):
		self.serial.write(f'*CLS\n'.encode())

	def measure_psd_full(self):
		self.serial.write(b'SPAN 19\n')  # set the entire frequency span = 100kHz
		self.serial.write(b'MEAS -1, 1\n')  # set the measurement type to PSD
		self.serial.write(b'MBIN -1, 0\n')  # move the trace marker region to i=0 bin

		self.serial.write(b'SPEC? -1')
		data = self.serial.read_until(b'\r').decode()
		data_list = list(data.split(","))[:-1]
		data_array = np.array(data_list, dtype=float)

		psd_full = np.vstack((self.freq_array, data_array)).T

		shutil.rmtree('output')
		os.makedirs('output')

		data_frame = pd.DataFrame(psd_full, columns=['Frequency, Hz', 'PSD, V_rms/sqrt(Hz)'])
		data_frame.to_csv('output/psd.csv')
		plt.plot(psd_full[:, 0], psd_full[:, 1])
		plt.yscale('log')
		plt.savefig('output/psd.pdf')

	def measure_psd_range(self, freq1, freq2):
		n1 = np.absolute(self.freq_array-freq1).argmin()
		n2 = np.absolute(self.freq_array-freq2).argmin()

		print(self.freq_array[n1])
		print(self.freq_array[n2])

		data_array = np.empty((0, 1), dtype=float)
		for i in range(n1, n2+1):
			self.serial.write(f'SPEC? -1, {i}\n'.encode())  # measure marker Y position
			c = ''
			s = ''
			while c != b'\r':
				c = self.serial.read(1)
				s += c.decode()

			data_array = np.append(data_array, float(str(s)))
			
			self.serial.write(f'MBIN -1, {i}\n'.encode())  # move the trace marker region to i=0 bin

		psd_range = np.vstack((self.freq_array[n1:n2+1], data_array)).T

		shutil.rmtree('output')
		os.makedirs('output')

		data_frame = pd.DataFrame(psd_range, columns=['Frequency, Hz', 'PSD, V_rms/sqrt(Hz)'])
		data_frame.to_csv('output/psd.csv')
		plt.plot(psd_range[:, 0], psd_range[:, 1])
		plt.yscale('log')
		plt.savefig('output/psd.pdf')


if __name__ == '__main__':
	dev = SR770()
	dev.clear()
	dev.measure_psd_range(0, 100000)
	dev.serial.close()  # close the serial port
