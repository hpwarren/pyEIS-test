
from eis_read_raster import eis_read_raster
from eis_read_template import eis_read_template
from eis_fit_profile import eis_fit_profile
import matplotlib.pyplot as plt
import numpy as np
from eis_fit_deviates import mpfit_model, mpfit_deviates

# input data and template files
file_data = 'data/eis_20190404_131513.data.h5'
file_template = 'data/fe_12_195_119.2c.template.h5'

# read fit template
template = eis_read_template(file_template)

# get central wavelength
wmin = template.template['wmin']
wmax = template.template['wmax']
wave = wmin + (wmax-wmin)*0.5

# read raster
raster = eis_read_raster(file_data, wave)
data = raster.data['data']
wave = raster.data['wave']
corr = raster.data['wave_corr']

# select raster and pixel for line profile
ix   = 48
iy   = 326
ints = data[iy, ix, :]
corr = corr[iy, ix]

# bad data correction
bad = np.where(ints<0)
ints[bad] = 0.0

# compute error on counts
errs = np.sqrt(ints)

# wavelength correction
wave = wave - corr

# fit profile
parinfo  = template.parinfo
template = template.template
fit = eis_fit_profile(wave, ints, errs, template, parinfo)

# compute new line profile from fit parameters
fit     = fit.fit
param   = fit['params'][0,0,::]
wave    = fit['wavelength'][0,0,::]
n_gauss = fit['n_gauss']
n_poly  = fit['n_poly']
fity    = mpfit_model(param, wave, n_gauss, n_poly)

# get chi-squared
chi2 = round(fit['chi2'][0,0],2)

# plot data and fit
plt.figure()
plt.step(wave, ints, 'k-o', label='Data', where='mid')
plt.plot(wave, fity, 'r-', label='Fit')
plt.xlabel('Wavelength ($\AA$)')
plt.ylabel('Intensity (counts)')
plt.legend(loc='upper right')
plt.text(min(wave), max(ints), '$\chi^2$='+str(chi2))
plt.savefig('ex_eis_fit_profile.png')
plt.show()
