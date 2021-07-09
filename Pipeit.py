from moabb.pipelines.utils import FilterBank

import Filterbankremake

from mne.decoding import CSP

from sklearn.svm import SVC as SVM
from sklearn.pipeline import make_pipeline

def Pipeit(filters=[[7,15],[16,23],[24,31],[32,39],[40,48]]):
    ''' Creates the pipeleines and paradigms for the classification when reading a new file'''
    pipelines_fb = {}
    pipelines_fb['FBCSP + SVM'] = make_pipeline(FilterBank(CSP(n_components=4)),SVM())
    pipelines_fb['FBCSP'] = make_pipeline(FilterBank(CSP(n_components=8)))
    pipelines_fb['SVM'] = make_pipeline(SVM())
    paradigm = Filterbankremake.FilterBankMotorImageryD(filters=filters,n_classes=4)
    return paradigm,filters,pipelines_fb