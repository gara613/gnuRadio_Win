"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class blk(gr.sync_block): # other base classes are basic_block, decim_block, interp_block
    def __init__(self, inputPar=1.0):  # only default arguments here 
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block', # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.inputPar = inputPar
 
        self.set_history(4)  #Example: The comand set_history(4) appends the previous 4-1=3 items to the input buffer (input_items), while the 4'th item is the current value. Therefore,
            #input_items[0][3] is the beginning of the current input stream.
            #input_items[0][2] is one input older than the current input stream.
            #input_items[0][1] is one input older than input_items[0][2]
            #input_items[0][0] is one input older than input_items[0][1]
        self.outputbuffer = [0,0,0] #This is a local array defined to store old output values. This is needed since there is not a set_history function to access old outputs...
        self.feedforward_taps = 0.0736, 0.2208, 0.2208, 0.0736 #feedforward taps of IIR filter
        self.feedbacktaps = 1.0000, -0.9761, 0.8568, -0.2919 #feedback taps of IIR filter

    def work(self, input_items, output_items):
        #Create a new list called output_items_with_history, which appends the previous 3 items to the current output_items. The properties of this new list are as follows:
        #output_items_with_history[3] is the beginning of the current output stream.
        #output_items_with_history[2] is one output older than the current output stream.
        #output_items_with_history[1] is one output older than output_items_with_history[2]
        #output_items_with_history[0] is one input older than output_items_with_history[1]
        
        output_items_with_history=[0]
        output_items_with_history.extend(self.outputbuffer)
        output_items_with_history.extend(output_items[0][:])
        output_items_with_history=output_items_with_history[1:]

        #Implement IIR difference equation to filter. Keep in mind that output_items_with_history[3] is the beginning of the current output stream, and input_items[0][3] is the beginning of the current input stream.
        for i in range(0, len(output_items_with_history)-3):
            output_items_with_history[i+3]=input_items[0][i+3]*self.feedforward_taps[0]+input_items[0][i+2]*self.feedforward_taps[1]+input_items[0][i+1]*self.feedforward_taps[2]+input_items[0][i]*self.feedforward_taps[3]-output_items_with_history[i+2]*self.feedbacktaps[1]-output_items_with_history[i+1]*self.feedbacktaps[2]-output_items_with_history[i]*self.feedbacktaps[3]

        output_items[0][:]=output_items_with_history[3:] #Populate our output_items array
        
        end_of_the_road=len(output_items[0]) #length of output item vector
        self.outputbuffer[2]=output_items[0][end_of_the_road-1] #The last element of the outputbuffer is the last output item
        self.outputbuffer[1]=output_items[0][end_of_the_road-2]#The second to last element of the outputbuffer is the second to last output item
        self.outputbuffer[0]=output_items[0][end_of_the_road-3] #The third to last element of the outputbuffer is the third to last output item
        
        return len(output_items[0])