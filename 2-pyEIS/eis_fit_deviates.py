
import numpy as np
import sys

# -----------------------------------------------------------------
# model for fitting EIS line profiles using mpfit.py
# -----------------------------------------------------------------

# series of Guassian model functions with polynomial background
def mpfit_model(param,x,n_gauss,n_poly):
    # ---------------------------------------------
    # x       = wavelengths (independent variable)
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

    # check inputs
    n_param = len(param)
    if n_param != 3*n_gauss+n_poly:
        print(' ! input parameter sizes do not match ... stopping')
        sys.exit()

    # compute Gaussians
    nx = len(x)
    f  = np.zeros(nx)
    for n in range(n_gauss):
        p   = param[3*n:3*n+3]
        arg = ((x-p[1])/p[2])**2
        f   = f + p[0]*np.exp(-arg/2.0)

    # compute polynomial background
    if n_poly > 0:
        p = param[3*n_gauss::]
        f = f + np.polyval(p,x)

    return f

# -----------------------------------------------------------------
# deviates for fitting EIS line profiles using mpfit.py
# -----------------------------------------------------------------

# computes deviates between fit model and data
def mpfit_deviates(param,x=None,y=None,error=None,n_gauss=None,n_poly=None,fjac=None):
    # ---------------------------------------------
    # x       = wavelengths (independent variable)
    # param   = model fit parameters (3*n_gauss+n_poly)
    #           param[0] = peak
    #           param[1] = centroid
    #           param[2] = width
    # n_gauss = number of Gaussians
    # n_poly  = degree of background polynomial
    #           0 = no background
    #           1 = constant
    #           2 = linear
    # y       = measurements
    # error   = measurement errors
    # ---------------------------------------------

    # check inputs
    n_param = param.shape[0]
    if n_param != 3*n_gauss+n_poly:
        print(' ! input parameter sizes do not match ... stopping')
        sys.exit()

    # compute model function
    model = mpfit_model(param,x,n_gauss,n_poly)

    # check data
    match, = np.where(error < 0.0)
    nbad  = len(match)
    ndata = len(y)
    if nbad == ndata:
        print(' ! no good data ... stopping')
        sys.exit()

    # compute deviates
    if nbad == 0:
        deviates = (y-model)/error
    else:
        error[match] = 1.0
        deviates = (y-model)/error
        deviates[match] = 0.0

    status = 0

    return [status, deviates]
