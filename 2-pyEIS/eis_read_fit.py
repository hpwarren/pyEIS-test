
import numpy as np
import h5py
import sys
import os

# function to read fit dictionary
def read_fit(file_fit):
    # -------------------------------------------------
    # file_fit = filename of fit dictionary
   #             (eg: 'eis_20190404_131513.fe_12_195_179_2c.fit.h5')
    # -------------------------------------------------

    # check inputs
    if not os.path.isfile(file_fit):
        print(' ! fit file does not exist ' + file_fit)
        sys.exit()
    else:
        print(' + reading fit file = '+file_fit)

    # read fit file
    f_fit = h5py.File(file_fit, 'r')
    fit = {}
    # get data
    for key in f_fit.keys():
        fit[key] = np.array(f_fit.get(key))

    return fit


if __name__ == '__main__':

    filename = 'TEST/eis_test_fit.fe_12_195_119_1c.fit.h5'
    fit = read_fit(filename)

    for key in fit.keys():
        if np.size(fit[key]) > 1:
            print('{:12} {:12} {:12}'.format(key,str(fit[key].dtype),str(np.shape(fit[key]))))
        else:
            print('{:12} {:12} {:12}'.format(key,str(fit[key].dtype),str(np.size(fit[key]))))
