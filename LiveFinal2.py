import mne_realtime
from mne_realtime import client
import pylsl
import mne
import scipy
import pandas as pd
import joblib
import numpy as np
import queue
from threading import Thread,Lock
import threading
import sys
import getopt

import time
from random import random as rand

from pylsl import StreamInfo, StreamOutlet, local_clock
# import FilterbankremakeD
# import Classify
from Connext2 import Connext2
a='myuid323458'
streams=pylsl.resolve_streams()
inlet=pylsl.StreamInlet(streams[0])
info=mne.create_info(inlet.info().channel_count(),inlet.info().nominal_srate())

#import CLF and FBCSP
def Connextlive(info,a):
    srate = 500
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
    while True:
        with mne_realtime.LSLClient(info=info,host=a) as Client:
            Cinfor=Client.get_measurement_info()
            sfreq=int(Cinfor['sfreq'])
            Client.start()
            print('Working')        
            try:
                clf= joblib.load('clffile.sav')
            except:
                print('A Classifier Has Not Been Generated')
            try:
                FBCSP= joblib.load('FBCSPfile.sav')
            except:
                print('An FBCSP Has Not Been Generated')
            filters=[[7,15],[16,23],[24,31],[32,39],[40,48],[49,55]]
            sample=Client.iter_raw_buffers()
            epoch=Client.get_data_as_epoch(n_samples=sfreq)
            psd_rest=np.array([])
            if psd_rest.is_empty!=True:
                psd=scipy.signal.welch(sample,fs=sfreq)
                ERD=(psd-psd_rest/psd_rest*100)
            else:
                psd_rest=scipy.signal.welch(sample,fs=sfreq)
            X=[]
            for bandpass in filters:
                fmin,fmax=bandpass
                epochf=epoch.copy().filter(fmin, fmax, method='iir',verbose=False)
                epochfd=epochf.get_data()
                X=np.concatenate([X,epochfd])
            X=np.expand_dims(X,axis=0)
            X_L=FBCSP.transform(X)
            y_pred=clf.predict(X_L)
        outlet.push_sample([y_pred])
        time.sleep(.5)
        # sent_samples += required_samples
        # now send it and wait for a bit before trying again.

def ThreadLive(info,a):
    with mne_realtime.LSLClient(info=info,host=a) as Client:
        Cinfor=Client.get_measurement_info()
        sfreq=int(Cinfor['sfreq'])
        Client.start()
        print('Working')        
        try:
            clf= joblib.load('clffile.sav')
        except:
            print('A Classifier Has Not Been Generated')
        try:
            FBCSP= joblib.load('FBCSPfile.sav')
        except:
            print('An FBCSP Has Not Been Generated')
        filters=[[7,15],[16,23],[24,31],[32,39],[40,48],[49,55]]
        while True:
            sample=Client.iter_raw_buffers()
            epoch=Client.get_data_as_epoch(n_samples=sfreq)
            psd_rest=np.array([])
            if psd_rest.is_empty!=True:
                psd=scipy.signal.welch(sample,fs=sfreq)
                ERD=(psd-psd_rest/psd_rest*100)
            else:
                psd_rest=scipy.signal.welch(sample,fs=sfreq)
            X=[]
            for bandpass in filters:
                fmin,fmax=bandpass
                epochf=epoch.copy().filter(fmin, fmax, method='iir',verbose=False)
                epochfd=epochf.get_data()
                X=np.concatenate([X,epochfd])
            X=np.expand_dims(X,axis=0)
            X_L=FBCSP.transform(X)
            y_pred=clf.predict(X_L)

""" def runit():

    thread1=Thread(target=ThreadLive,args=(info,a)).start()
    thread2=Thread(target=Connext2,args=(sfreq,[p.get(),q.get()]).start() """

Connextlive(info,a)