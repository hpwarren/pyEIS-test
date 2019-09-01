
from eis_read_raster import eis_read_raster
from eis_read_template import eis_read_template
from eis_fit_raster import eis_fit_raster
from eis_save_fit import save_fit
from eis_read_fit import read_fit
from eis_fit_deviates import mpfit_model
import numpy as np
import matplotlib.pyplot as plt

# input data and template files
file_data     = 'data/eis_20190404_131513.data.h5'
file_template = 'data/fe_12_195_119.2c.template.h5'

# read fit template
template = eis_read_template(file_template)

# get central wavelength
wmin = template.template['wmin']
wmax = template.template['wmax']
wave = wmin + (wmax-wmin)*0.5

# read raster
raster = eis_read_raster(file_data, wave)
ints   = raster.data['data']
wave   = raster.data['wave']
corr   = raster.data['wave_corr']

# get dimensions
ndata = ints.shape
nx    = ndata[0]
ny    = ndata[1]
nz    = ndata[2]

# bad data correction
bad = np.where(ints<0)
ints[bad] = 0.0

# compute error on counts
errs = np.sqrt(ints)

# wavelength correction
newwave = np.zeros(ndata)
for i in range(nx):
    for j in range(ny):
        newwave[i,j,::] = wave-corr[i,j]
wave = newwave

# fit profile
parinfo  = template.parinfo
template = template.template
fit      = eis_fit_raster(wave, ints, errs, template, parinfo)

# save fit output
fit = fit.fit
file_fit = save_fit(fit, file_data)

# read fit output back from file
fit = read_fit(file_fit[0])

# inspect what's in the fit output
for key in fit.keys():
    if np.size(fit[key]) > 1:
        print('{:12} {:12} {:12}'.format(key,str(fit[key].dtype),str(np.shape(fit[key]))))
    else:
        print('{:12} {:12} {:12}'.format(key,str(fit[key].dtype),str(np.size(fit[key]))))

# hand select a few slit/raster positions for plotting line profiles
xpos = [302, 282, 272, 268]
ypos = [48, 58, 52, 68]

# plot window setup
x_scale  = raster.data['pointing']['x_scale']
date_obs = raster.data['index']['date_obs']
IMGnx    = x_scale*ints.shape[1]/50.0
IMGny    = ints.shape[0]/50.0
plt.rcParams.update({'font.size':14})
# plot raster
raster   = np.sum(ints, axis=2)
range    = np.percentile(raster, (1, 99))
range    = range[1]*np.array([1.0E-2, 1.0])
scaled   = np.log10(np.clip(raster, range[0], range[1]))
plt.figure(figsize=(IMGnx*4, IMGny))
plt.subplot(1,4,1)
plt.imshow(scaled, origin='lower', aspect=1/x_scale, cmap='gray')
plt.plot(ypos, xpos, 'r+', markersize=4)
plt.xlabel('Raster Step')
plt.ylabel('Slit Position')
plt.title('Data : '+date_obs)

# plot fit
gauss    = fit['component']-1
fitrast  = fit['int'][::,::,gauss]
range    = np.percentile(fitrast, (1, 99))
range    = range[1]*np.array([1.0E-2, 1.0])
scaled   = np.log10(np.clip(fitrast, range[0], range[1]))
plt.subplot(1,4,2)
plt.imshow(scaled, origin='lower', aspect=1/x_scale, cmap='gray')
plt.plot(ypos, xpos, 'r+', markersize=4)
plt.title('Fit : '+fit['line_ids'][gauss])
plt.xlabel('Raster Step')

# plot the hand-picked line profiles
nsubplt = [3, 4, 7, 8]
n_gauss = fit['n_gauss']
n_poly  = fit['n_poly']
for k in np.arange(4):
    # get the slit/raster position
    x      = xpos[k]
    y      = ypos[k]
    subplt = nsubplt[k]
    # get the data
    wave_ij = wave[x,y,::]
    line_ij = ints[x,y,::]
    # get the fit parameters
    params_ij  = fit['params'][x,y,::]
    fitwave_ij = fit['wavelength'][x,y,::]
    # use the fit model to compute the fit profile from the fit parameters
    fitline_ij = mpfit_model(params_ij, fitwave_ij, n_gauss, n_poly)
    chi2_ij    = round(fit['chi2'][x,y],1)
    # plot profiles
    plt.subplot(2,4,subplt)
    plt.plot(wave_ij, line_ij, 'k-o', label='Data')
    plt.plot(fitwave_ij, fitline_ij,'r-', label='Fit')
    if k == 2 or k == 3: plt.xlabel('Wavelength ($\AA$)')
    if k == 0 or k == 2: plt.ylabel('Intensity (counts)')
    plt.text(min(wave_ij), max(line_ij), '$\chi^2$='+str(chi2_ij))
    plt.title('['+str(y)+','+str(x)+']')
    if k == 0: plt.legend(loc='upper right')
plt.tight_layout()
plt.show()
