#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: ROC curves energy detector
# Author: GAR
# Description: ROC curves generator for energy detector
# Generated: Wed Aug  2 13:07:12 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import ROC_energy_block
import sip
import sys
from gnuradio import qtgui
from gnuradio import uhd
import numpy as np
from scipy import special as scpsp
import scipy
from time import sleep 

class ROC_enDet(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "ROC curves energy detector")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("ROC curves energy detector")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "ROC_enDet")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ####################################################################################################
        # Variables
        ####################################################################################################
        self.samp_rate = samp_rate = 320000 # nimimum USRP sample rate (when used with CBx daughterboards) is around 200kHz
        self.N = N = 32 # number of samples (page size greatly limits this value, min page size seems to be the default 4096, then the buffer is formed in chunks of size [pagesize/N,N])
        self.thr = thr = 0
        self.center_freq = center_freq = 1.7e9
        self.RF_gain = RF_gain = 0.0

        ####################################################################################################
        # Blocks
        ####################################################################################################
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)

        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, N)
        self.uhd_usrp_source_0 = uhd.usrp_source(",".join(("", "")), uhd.stream_args(cpu_format="fc32",channels=range(1)))
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(center_freq , 0)
        self.uhd_usrp_source_0.set_gain(RF_gain, 0)

        self.ROC_energy_block = ROC_energy_block.blk(N=N, thr=thr,fun='cal')

        self.null_source_0=blocks.null_source(gr.sizeof_float*1)

        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, 'C:\\Users\\usuario\\Documents\\gnuRadio\\Misc\\SpectrumSensing\\N_det_exp.dat', False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_float*1, 'C:\\Users\\usuario\\Documents\\gnuRadio\\Misc\\SpectrumSensing\\N_inD_exp.dat', False)
        self.blocks_file_sink_1.set_unbuffered(True) # information on second sink could be irrelevant... if thr gives the correct number
        self.blocks_file_sink_2 = blocks.file_sink(gr.sizeof_float*1, 'C:\\Users\\usuario\\Documents\\gnuRadio\\Misc\\SpectrumSensing\\Thr_exp.dat', False)
        self.blocks_file_sink_2.set_unbuffered(True)
        self.blocks_file_sink_3 = blocks.file_sink(gr.sizeof_float*1, 'C:\\Users\\usuario\\Documents\\gnuRadio\\Misc\\SpectrumSensing\\P_var_exp.dat', False)
        self.blocks_file_sink_3.set_unbuffered(True)
        self.blocks_file_sink_4 = blocks.file_sink(gr.sizeof_float*1, 'C:\\Users\\usuario\\Documents\\gnuRadio\\Misc\\SpectrumSensing\\P_var_reim_exp.dat', False)
        self.blocks_file_sink_4.set_unbuffered(True) 
        self.blocks_file_sink_5 = blocks.file_sink(gr.sizeof_float*1, 'C:\\Users\\usuario\\Documents\\gnuRadio\\Misc\\SpectrumSensing\\P_absSq_exp.dat', False)
        self.blocks_file_sink_5.set_unbuffered(True)
        
        ####################################################################################################
        # Connections
        ####################################################################################################
        self.connect((self.ROC_energy_block, 0), (self.blocks_file_sink_3, 0))
        self.connect((self.ROC_energy_block, 1), (self.blocks_file_sink_4, 0))
        self.connect((self.ROC_energy_block, 2), (self.blocks_file_sink_5, 0))
        self.connect((self.null_source_0,0), (self.blocks_file_sink_0, 0))
        self.connect((self.null_source_0,0), (self.blocks_file_sink_1, 0))
        self.connect((self.null_source_0,0), (self.blocks_file_sink_2, 0))

        self.connect((self.ROC_energy_block, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0,0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.ROC_energy_block, 0))

    ####################################################################################################
    # Class methods
    ####################################################################################################

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ROC_enDet")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def set_fun(self, fun):
        self.fun = fun
        self.ROC_energy_block.fun = self.fun

    def get_thr(self):
        return self.thr

    def set_thr(self, thr):
        self.thr = thr
        self.ROC_energy_block.thr = self.thr

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N
        self.ROC_energy_block.N = self.N

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq 
        self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)        

    def set_antenna(self):
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)

    def set_RF_gain(self):
        self.RF_gain = RF_gain
        self.uhd_usrp_source_0.set_gain(RF_gain, 0)


def main(top_block_cls=ROC_enDet, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    # By default the ROC_energy block is called in the calibration mode which estimates the noise floor
#    tb.set_center_freq(tb.get_center_freq()+4*tb.get_samp_rate())
#    print(tb.get_center_freq())
    sleep(3)  # take 5 seconds of samples in the calibration mode

    # load the estimated noise value
    estN = scipy.fromfile(open("C:\Users\usuario\Documents\gnuRadio\Misc\SpectrumSensing\P_absSq_exp.dat"), dtype=scipy.float32) 
    estN=np.mean(estN[np.abs(estN)>=1e-15])
    yy = scipy.fromfile(open("C:\Users\usuario\Documents\gnuRadio\Misc\SpectrumSensing\P_var_reim_exp.dat"), dtype=scipy.float32) 
    yy=np.mean(yy[np.abs(yy)>=1e-15])
    zz = scipy.fromfile(open("C:\Users\usuario\Documents\gnuRadio\Misc\SpectrumSensing\P_var_exp.dat"), dtype=scipy.float32) 
    zz=np.mean(zz[np.abs(zz)>=1e-15])
 
    print('Estimated noise floor in dB: ', estN, yy, zz)
    
#    tb.set_center_freq(tb.get_center_freq()-4*tb.get_samp_rate())
    print('the center frequency is:', tb.get_center_freq())

    # Reconfigure flow-graph 
#    tb.lock()
    tb.stop()
    tb.wait()

    tb.disconnect((tb.ROC_energy_block, 0), (tb.blocks_file_sink_3, 0))
    tb.disconnect((tb.ROC_energy_block, 1), (tb.blocks_file_sink_4, 0))
    tb.disconnect((tb.ROC_energy_block, 2), (tb.blocks_file_sink_5, 0))
    tb.disconnect((tb.null_source_0,0), (tb.blocks_file_sink_0, 0))
    tb.disconnect((tb.null_source_0,0), (tb.blocks_file_sink_1, 0))
    tb.disconnect((tb.null_source_0,0), (tb.blocks_file_sink_2, 0))

    # Connect the other sink blocks and restart
    tb.connect((tb.ROC_energy_block, 0), (tb.blocks_file_sink_0, 0))
    tb.connect((tb.ROC_energy_block, 1), (tb.blocks_file_sink_1, 0))
    tb.connect((tb.ROC_energy_block, 2), (tb.blocks_file_sink_2, 0))
    tb.connect((tb.null_source_0,0), (tb.blocks_file_sink_3, 0))
    tb.connect((tb.null_source_0,0), (tb.blocks_file_sink_4, 0))
    tb.connect((tb.null_source_0,0), (tb.blocks_file_sink_5, 0))
#    tb.unlock()

    try: 
        tb.start()
    except ValueError: 
        print('Something went wrong')

    tb.set_fun('meas') # change to the 'measurement' mode 
    # sleep(0.1)

    i=0
    for targPf in np.logspace(-6,0,21): # data with the first value of threshold is invalidated due to the noise floor 
        new_thr = (10**(estN/10))*scpsp.gammainccinv(tb.get_N(), targPf) 
        tb.set_thr(new_thr) # change threshold
        sleep(0.1) # run the flowgraph (with current values) for 3 seconds   
        print(i, new_thr) 
        i=i+1

    tb.stop()
    tb.wait()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()