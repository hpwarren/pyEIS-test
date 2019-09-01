from eis_read_raster import eis_read_raster
from eis_read_template import eis_read_template
from eis_fit_raster import eis_fit_raster
import matplotlib.pyplot as plt
import numpy as np

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
ints = raster.data['data']
wave = raster.data['wave']
corr = raster.data['wave_corr']

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
fit = eis_fit_raster(wave, ints, errs, template, parinfo)
        
# plot raster and fit
x_scale  = raster.data['pointing']['x_scale']
date_obs = raster.data['index']['date_obs']
IMGnx    = x_scale*ints.shape[1]/50.
IMGny    = ints.shape[0]/50.
# raster
raster   = np.sum(ints, axis=2)
range    = np.percentile(raster, (1, 99))
range    = range[1]*np.array([1.0E-2, 1.0])
scaled   = np.log10(np.clip(raster, range[0], range[1]))

plt.figure(figsize=(IMGnx, IMGny))
plt.subplot(121)
plt.imshow(scaled, origin='lower', aspect=1/x_scale, cmap='gray')
plt.title(date_obs)
# fit
fits     = fit.fit
fit      = fits['int'][::,::,(fits['component']-1)]
range    = np.percentile(fit, (1, 99))
range    = range[1]*np.array([1.0E-2, 1.0])
scaled   = np.log10(np.clip(fit, range[0], range[1]))
plt.subplot(122)
plt.imshow(scaled, origin='lower', aspect=1/x_scale, cmap='gray')
plt.title('Fit')
plt.tight_layout()
plt.savefig('ex_eis_fit_raster.png')
plt.show()
