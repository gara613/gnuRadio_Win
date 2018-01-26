"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
	"""Embedded Python Block example - a simple multiply const"""

	def __init__(self, N=32,thr=1e-12,fun='cal'):  # only default arguments here
		"""arguments to this function show up as parameters in GRC"""
		self.N = N
		self.thr = thr
		self.fun = fun # 'cal' to enter the calibration mode, 'meas' to enter the measurement mode

		gr.sync_block.__init__(
			self,
			name='Embedded Python Block',   # will show up in GRC
			in_sig=[(np.complex64,self.N)],
			out_sig=[np.float32,np.float32,np.float32]
		)
		# if an attribute with the same name as a parameter is found, a callback is registered (properties work, too).

	def work(self, input_items, output_items):
		"""Energy and thresholding spetrum sensing"""
		# energy is calculated for each row in the input matrix and then averaged, due to the size of the input block in terms of pagesize shape(input)=[pagesize/N,N] 
		if self.fun == 'cal':
			output_items[0][:] = 10*np.log10(np.mean(np.var(input_items[0],axis=1,ddof=0))) # ddof=0 is used in the divisor: N-ddof
			output_items[1][:] = 10*np.log10(np.mean(np.var(np.real(input_items[0]),axis=1,ddof=0)+np.var(np.imag(input_items[0]),axis=1,ddof=0))) # this assumes noise is circularly symmetric complex Gaussian
			output_items[2][:] = 10*np.log10(np.mean(np.sum(np.absolute(input_items[0])**2,axis=1)/np.shape(input_items[0])[1])) # signal power

		elif self.fun == 'meas':
			output_items[0][:] = np.sum(np.sum(np.absolute(input_items[0])**2,axis=1) > self.thr) 
			output_items[1][:] = float(np.shape(input_items[0])[0]) 
			output_items[2][:] = self.thr
		return len(output_items[0])