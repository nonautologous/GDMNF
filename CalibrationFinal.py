import mne
from mne.io import pick
import numpy as np
import scipy
import joblib

from moabb.pipelines.utils import FilterBank
from mne.decoding import CSP
from sklearn.svm import SVC as SVM
from sklearn.pipeline import make_pipeline

import FilterbankremakeD

from sklearn.pipeline import Pipeline as pipe
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.model_selection import (cross_val_score, LeaveOneGroupOut,StratifiedKFold)
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection._validation import _fit_and_predict
from sklearn.metrics import get_scorer
from sklearn.base import clone
import sklearn.metrics
import pandas as pd

def Classify(paradigm,data,pipelines_fb):
    results=pd.DataFrame()
    X,y,metadata=paradigm.get_data(data,[0])
    le=LabelEncoder()
    y=le.fit_transform(y)
    groups=metadata.session.values
    FBCSP=pipelines_fb['FBCSP']
    X_n=FBCSP.fit_transform(X,y)
    clf=pipelines_fb['SVM']
    cv=LeaveOneGroupOut()
    train,test=cv.split(X_n,y,groups)
    clf.fit(X_n[train[0]],y[train[0]])
    y_pred=clf.predict(X_n[test[0]])
    Kappa=sklearn.metrics.cohen_kappa_score(y[test[0]],y_pred)

    result=pd.DataFrame({'Subject':'1','Kappa': Kappa,'n_samples': len(train),'n_channels': X.shape[1]},index=[0])
    print(result)
    results=results.append(result)
    return clf,results,FBCSP


def Pipeit(filters=[[7,15],[16,23],[24,31],[32,39],[40,48],[49,55]]):
	''' Creates the pipeleines and paradigms for the classification when reading a new file'''
	pipelines_fb = {}
	pipelines_fb['FBCSP + SVM'] = make_pipeline(FilterBank(CSP(n_components=4)),SVM())
	pipelines_fb['FBCSP'] = make_pipeline(FilterBank(CSP(n_components=8)))
	pipelines_fb['SVM'] = make_pipeline(SVM())
	paradigm = FilterbankremakeD.FilterBankMotorImageryD(filters=filters,n_classes=3)
	return paradigm,filters,pipelines_fb

import pyxdf
# select file
from tkinter import Tk 
from tkinter.filedialog import askopenfilename
Tk().withdraw()
filename = askopenfilename() 
print(filename)

streams,header=pyxdf.load_xdf(filename)
data=streams[0]["time_series"].T
info=mne.create_info(streams[0]['info']['channel_count'],streams[0]['nominal_srate'])
raw = mne.io.RawArray(data, info)
# import into raw and find events from stim
event_id=dict(null=0,left=1,right=2)

tmin, tmax = -1., 4.
events=mne.find_events(raw)
picks = mne.io.pick._picks_to_idx(info, None, picks='all', exclude=())

epoch= mne.epochs.EpochsArray(data[picks][np.newaxis], info, events)
filters=[[7,15],[16,23],[24,31],[32,39],[40,48],[49,55]]
X=[]

for bandpass in filters:
    fmin,fmax=bandpass
    epochf=epoch.copy().filter(7,15,method='iir',picks=picks,verbose=False)
    epochfd=epochf.get_data()
    X=np.concatenate([X,epochfd])
X=np.expand_dims(X,axis=0)
pipeline=Pipeit(filters)
clf,results,FBCSP=Classify(pipeline[0],X,pipeline[2])
pd.results.to_csv(index=False)
joblib.dump(clf,'savedcalibration.sav')
joblib.dump(clf,'savedFBCSP.sav')
#run through classification and save