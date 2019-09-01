
import numpy as np

# function to hold the fit parameters
def fit_dictionary(nx,ny,n_wave,n_gauss,n_poly):
    # ---------------------------------------------
    # nx      = x-dimension (eg: pixels along the slit)
    # ny      = y-dimension (eg: raster positions)
    # n_wave  = number of wavelength points
    # n_gauss = number of Gaussians
    # n_poly  = degree of background polynomial
    # ---------------------------------------------

    n_param = 3*n_gauss+n_poly

    struct = {'line_ids':      np.chararray(n_gauss),     \
              'n_gauss':       n_gauss,                   \
              'n_poly':        n_poly,                    \
              'component':     0,                         \
              'status':        np.zeros((nx,ny)),         \
              'chi2':          np.zeros((nx,ny)),         \
              'wavelength':    np.zeros((nx,ny,n_wave)),  \
              'int':           np.zeros((nx,ny,n_gauss)), \
              'e_int':         np.zeros((nx,ny,n_gauss)), \
              'peak':          np.zeros((nx,ny,n_gauss)), \
              'e_peak':        np.zeros((nx,ny,n_gauss)), \
              'centroid':      np.zeros((nx,ny,n_gauss)), \
              'e_centroid':    np.zeros((nx,ny,n_gauss)), \
              'width':         np.zeros((nx,ny,n_gauss)), \
              'e_width':       np.zeros((nx,ny,n_gauss)), \
              'background':    np.zeros((nx,ny,n_poly)),  \
              'e_background':  np.zeros((nx,ny,n_poly)),  \
              'params':        np.zeros((nx,ny,n_param)), \
              'perror':        np.zeros((nx,ny,n_param))  }

    return struct
