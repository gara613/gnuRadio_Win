"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, sample_rate=32000.0, freq_to_add=300.0, signal_amp=1.0, factor=1.0):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.factor = factor
        self.sample_rate=sample_rate
        self.freq_to_add=freq_to_add
        self.signal_amp=signal_amp
        
    def work(self, input_items, output_items):	
        f_m = 300.0
        f_c = 4000.0
        Dp = 10.0
        # output_items[0][:] = np.sin(2*np.pi*f_m*input_items[0]) * np.sin(2*np.pi*f_c*input_items[0]) #self.factor
        # output_items[0][:] = np.cos(2*np.pi*f_c*input_items[0] + Dp*np.sin(2*np.pi*f_m*input_items[0])) #self.factor

        input_in_fft = np.fft.fftshift(np.fft.fft(input_items[0][:], len(output_items[0][:])))
        freq2mod = int(len(output_items[0][:]) * 0.5 * (1 + 2*self.freq_to_add/self.sample_rate)) # add to the upper half vector
        input_in_fft[freq2mod] = (self.signal_amp)*len(output_items[0][:])        
        freq2mod = int(len(output_items[0][:]) * 0.5 *(1 - 2*self.freq_to_add/self.sample_rate)) # add to the lower half vector         
        input_in_fft[freq2mod] = (self.signal_amp)*len(output_items[0][:])

        output_items[0][:] = np.fft.ifft(np.fft.ifftshift(input_in_fft), len(output_items[0]))

        return len(output_items[0])