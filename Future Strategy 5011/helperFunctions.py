import numpy as np
import h5py
import pandas as pd

# Returns all data of a given item
# Row -- 1 day
# numbers of days x 4
def generate_data_helper(data_list, asset):
    asset_open = np.array([array[asset, 0] for array in data_list])
    asset_high_price = np.array([array[asset, 1] for array in data_list])
    asset_low_price = np.array([array[asset, 2] for array in data_list])
    asset_close_price = np.array([array[asset, 3] for array in data_list])

    assetData = np.array([asset_open, asset_high_price, asset_low_price, asset_close_price]).T

    return assetData


# Returns the given few days of the dataset
# Given the number of past minutes
def get_past_data(data_input, numPastmins):
    if (numPastmins > data_input.shape[0]):
        raise ValueError ("number exceeds")
    else:
        return data_input[data_input.shape[0]-numPastmins:]



# Returns the average of the given dataset on each row
def compute_average(data_input):
     average = np.mean(data_input, axis=1)
     return average



# Update position matrix
# Given amount && index
def update_position(current_position, amount, index):
    return current_position[index] == amount

def read_h5(path):

        dicts = {}
        indexes = ['A.DCE', 'AG.SHF', 'AU.SHF', 'I.DCE', 'IC.CFE', 'IF.CFE',
                   'IH.CFE', 'J.DCE', 'JM.DCE', 'M.DCE', 'RB.SHF', 'Y.DCE', 'ZC.CZC']
        cols = ['open', 'high', 'low', 'close', 'volumn']

        if 'format1' in path:
            with h5py.File(path, 'r') as f:
                keys = list(f.keys())
            for i in range(len(keys)):
                dat = pd.read_hdf(path, key=keys[i])
                dicts[keys[i]] = dat

        else:
            with h5py.File(path, 'r') as f:
                keys = list(f.keys())
                for i in range(len(keys)):
                    dat = pd.DataFrame(f[keys[i]][:])
                    dat.index = indexes
                    dat.columns = cols
                    dicts[keys[i]] = dat
        return dicts

def addLabel(data):
    train_label = list()
    for i in range(0, len(data) - 1):
        if data[i + 1] > data[i]:
            train_label.append(1)
        else:
            train_label.append(0)
    return train_label