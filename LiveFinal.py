import mne_realtime
from mne_realtime import client
import pylsl
import mne
import scipy
import pandas as pd
import joblib
import numpy as np
# import queue
from threading import Thread,Lock
# import threading

# import FilterbankremakeD
# import Classify
from Connext2 import Connext2
a='myuid323458'
streams=pylsl.resolve_streams()
inlet=pylsl.StreamInlet(streams[0])
info=mne.create_info(inlet.info().channel_count(),inlet.info().nominal_srate())

#import CLF and FBCSP

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
            Connext2([y_pred,ERD])

ThreadLive(info,a)