import moabb.datasets.bnci as bnci
import moabb
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.svm import SVC as SVM
from sklearn.pipeline import make_pipeline

from mne.decoding import CSP

from moabb.paradigms import FilterBankMotorImagery
from moabb.evaluations import CrossSessionEvaluation,WithinSessionEvaluation
from moabb.pipelines.utils import FilterBank
import moabb.pipelines.utils as utils
import numpy as np
import mne.io
from sklearn.model_selection import (cross_val_score, LeaveOneGroupOut,StratifiedKFold)
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection._validation import _fit_and_predict
from sklearn.metrics import get_scorer
from sklearn.base import clone
import sklearn.metrics
import abc
from abc import ABCMeta, abstractproperty, abstractmethod, ABC
import logging
'''
Updating MOABB to use Raw instead of Dataset
Based on the literature, Only need to modify the Paradigms, not the pipeline

Technically all a paradigm does is a
SO the paradigm can be set into 4 levels
Base: apply the bandpass from the given filters, run mne.epochs, append the data to the X and labels
BaseMI:assign filters, channels and events
FBank: assign multiple filters
FBMI: determine if their are multiple classes 
'''
log=logging.getLogger()
class BaseParadigmD(metaclass=ABCMeta):
    def process_raw(self,epoch, return_epochs=True):
        # get events id
        picks = mne.pick_types(epoch.info, eeg=True, stim=False)
        # pick events, based on event_id
        events = mne.pick_events(epoch.events, include=list(epoch.event_id.values()))
        inv_events = {k: v for v, k in epoch.event_id.items()}
        labels = np.array([inv_events[e] for e in epoch.events[:, -1]])
        metadata = pd.DataFrame(index=range(len(labels)))
        return epoch, labels, metadata
    def get_data(self,raw,subjects=None):
        data = raw.get_data(subjects)
        
        X = []
        labels = []
        metadata = []
        proc = self.process_raw(raw)

        x, lbs, met = proc
        met['subject'] = 0
        met['session'] = 0
        met['run'] = 0
        metadata.append(met)

        # grow X and labels in a memory efficient way. can be slow
        if len(X) > 0:
            X = np.append(X, x, axis=0)
            labels = np.append(labels, lbs, axis=0)
        else:
            X = x
            labels = lbs

        metadata = pd.concat(metadata, ignore_index=True)
        return X, labels, metadata
class BaseMotorImageryD(BaseParadigmD):
    """Base Motor imagery paradigm.

    Please use one of the child classes

    Parameters
    ----------

    filters: list of list (defaults [[7, 35]])
        bank of bandpass filter to apply.

    events: List of str | None (default None)
        event to use for epoching. If None, default to all events defined in
        the dataset.

    tmin: float (default 0.0)
        Start time (in second) of the epoch, relative to the dataset specific
        task interval e.g. tmin = 1 would mean the epoch will start 1 second
        after the begining of the task as defined by the dataset.

    tmax: float | None, (default None)
        End time (in second) of the epoch, relative to the begining of the
        dataset specific task interval. tmax = 5 would mean the epoch will end
        5 second after the begining of the task as defined in the dataset. If
        None, use the dataset value.

    channels: list of str | None (default None)
        list of channel to select. If None, use all EEG channels available in
        the dataset.

    resample: float | None (default None)
        If not None, resample the eeg data with the sampling rate provided.
    """
    def __init__(self, filters=([7, 35],), events=None, tmin=0.0, tmax=None,
                 channels=None, resample=None):
        super().__init__()
        self.filters = filters
        self.channels = channels
        self.events = events
        self.resample = resample

        if (tmax is not None):
            if tmin >= tmax:
                raise(ValueError("tmax must be greater than tmin"))

        self.tmin = tmin
        self.tmax = tmax

    @abc.abstractmethod
    def used_events(self, dataset):
        pass

    @property
    def datasets(self):
        if self.tmax is None:
            interval = None
        else:
            interval = self.tmax - self.tmin
        return utils.dataset_search(paradigm='imagery',
                                    events=self.events,
                                    interval=interval,
                                    has_all_events=True)

    @property
    def scoring(self):
        return 'accuracy'
class FilterBankD(BaseMotorImageryD):
    """Filter Bank MI."""
    def __init__(self, filters=([8, 12], [12, 16], [16, 20], [20, 24],
                                [24, 28], [28, 32]), **kwargs):
        """init"""
        super().__init__(filters=filters, **kwargs)
class FilterBankMotorImageryD(FilterBankD):

    """
    Filter bank n-class motor imagery.

    Metric is 'roc-auc' if 2 classes and 'accuracy' if more

    Parameters
    -----------

    events: List of str
        event labels used to filter datasets (e.g. if only motor imagery is
        desired).

    n_classes: int,
        number of classes each dataset must have. If events is given,
        requires all imagery sorts to be within the events list.
    """

    def __init__(self, n_classes=2, **kwargs):
        "docstring"
        super().__init__(**kwargs)
        self.n_classes = n_classes

        if self.events is None:
            log.warning("Choosing from all possible events")
        else:
            assert n_classes <= len(
                self.events), 'More classes than events specified'
    
    def used_events(self, dataset):
        out = {}
        if self.events is None:
            for k, v in dataset.event_id.items():
                out[k] = v
                if len(out) == self.n_classes:
                    break
        else:
            for event in self.events:
                if event in dataset.event_id.keys():
                    out[event] = dataset.event_id[event]
                if len(out) == self.n_classes:
                    break
        if len(out) < self.n_classes:
            raise(ValueError(f"Dataset {dataset.code} did not have enough "
                             f"events in {self.events} to run analysis"))
        return out
    
    @property
    def scoring(self):
        if self.n_classes == 2:
            return 'roc_auc'
        else:
            return 'accuracy'
