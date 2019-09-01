
from copy import deepcopy
import numpy as np
import sys

# function to scale parameters from a fit template to the data
def scale_guess(x,y,param,n_gauss,n_poly):
    # ---------------------------------------------
    # x       = wavelengths (independent variable)
    # y       = measurements
    # param   = model fit parameters (3*n_gauss+n_poly)
    #           param[0] = peak
    #           param[1] = centroid
    #           param[2] = width
    # n_gauss = number of Gaussians
    # n_poly  = degree of background polynomial
    #           0 = no background
    #           1 = constant
    #           2 = linear
    # ---------------------------------------------

    # copy param array
    newparam = deepcopy(param)

    # check inputs
    n_param = len(newparam)
    if n_param != 3*n_gauss+n_poly:
        print(' ! input parameter sizes do not match ... stopping')
        sys.exit()

    # get background from data
    bkg_data = np.mean(np.sort(y)[0:3])

    # get background from guess
    if n_poly > 0:
        bkg = newparam[3*n_gauss::]
        bkg_guess = np.median(np.sort(np.polyval(bkg,x))[0:3])
        # scale background
        scale = bkg_data/bkg_guess
        newparam[3*n_gauss::] = bkg*scale
        # compute new background
        bkg = newparam[3*n_gauss::]
        new_bkg = np.polyval(bkg,x)
    else:
        new_bkg = np.zeros(len(x))

    # compute new peaks
    for n in range(n_gauss):
        p = newparam[3*n:3*n+3]
        peak = p[0]
        cent = p[1]
        indx = np.abs(x-cent).argmin()
        new_peak = y[indx]-new_bkg[indx]
        if new_peak < 0: new_peak = 0.0
        newparam[3*n] = new_peak

    return newparam
