import sys
import getopt

import time
from random import random as rand

from pylsl import StreamInfo, StreamOutlet, local_clock


def Connext2(sample):
    srate = 100
    name = 'Classifier'
    type = 'Parm'
    n_channels = 2
    # first create a new stream info (here we set the name to BioSemi,
    # the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
    # last value would be the serial number of the device or some other more or
    # less locally unique identifier for the stream as far as available (you
    # could also omit it but interrupted connections wouldn't auto-recover)
    info = StreamInfo(name, type, n_channels, srate, 'float32', 'myuid34234')

    # next make an outlet
    outlet = StreamOutlet(info)

    print("now sending data...")
    # start_time = local_clock()
    # sent_samples = 0
    # elapsed_time = local_clock() - start_time
    # required_samples = int(srate * elapsed_time) - sent_samples
    outlet.push_sample(sample)
    # sent_samples += required_samples
    # now send it and wait for a bit before trying again.
    time.sleep(0.5)
