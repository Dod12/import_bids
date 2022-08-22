import mne
import scipy as sp
import numpy as np


def setup_ideal_montage(standard_montage: str = None, template_path: str = None, location: str = None):

    if standard_montage is not None:
        montage = mne.channels.make_standard_montage(standard_montage)
    elif template_path is not None:
        montage = mne.channels.read_custom_montage(template_path)
    elif location is not None:
        elec = sp.io.loadmat(location)['elec']
        locs = np.array(elec[0,0][0])
        labels = np.array([str(label[0]) for label in np.squeeze(np.ravel(np.array(elec[0,0][1])))])
        montage = mne.channels.DigMontage(dig=locs, ch_names=np.flatten(labels))
    else:
        raise ValueError("One of the montage formats must be specified.")

    return montage
