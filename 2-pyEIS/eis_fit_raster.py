
from eis_fit_deviates import mpfit_model, mpfit_deviates
from eis_scale_guess import scale_guess
from eis_fit_dictionary import fit_dictionary
from eis_mpfit import mpfit
from datetime import datetime
import numpy as np

class eis_fit_raster:

    def __init__(self, wave, ints, errs, template, parinfo):
        self.wave     = wave
        self.template = template
        self.parinfo  = parinfo
        self.n_wave   = np.shape(wave)[2]
        self.n_gauss  = template['n_gauss']
        self.n_poly   = template['n_poly']
        self.fit      = None

        # get fit structure
        ndata = ints.shape
        nx    = ndata[0]
        ny    = ndata[1]
        fit = fit_dictionary(nx,ny,self.n_wave,self.n_gauss,self.n_poly)
        fit['line_ids']  = template['line_ids']
        fit['n_gauss']   = self.n_gauss
        fit['n_poly']    = self.n_poly
        fit['component'] = template['component']
        peaks = np.arange(self.n_gauss)*3
        cents = np.arange(self.n_gauss)*3+1
        wdths = np.arange(self.n_gauss)*3+2
        backs = self.n_gauss*3

        # timer
        t1 = datetime.now()

        # loop over rasters and slit positions at each raster
        for ii in range(nx):
            for jj in range(ny):

                # get profile from raster
                wave_ij = wave[ii,jj,::]
                ints_ij = ints[ii,jj,::]
                errs_ij = errs[ii,jj,::]

                # only use good data
                good = np.where(errs_ij > 0)
                wave_ij = wave_ij[good]
                ints_ij = ints_ij[good]
                errs_ij = errs_ij[good]

                # scale guess parameters to data
                oldguess = template['fit']
                newguess = scale_guess(wave_ij,ints_ij,oldguess,self.n_gauss,self.n_poly)

                # plug in new guess values to parinfo
                for i in range(len(newguess)):
                    self.parinfo[i]['value'] = newguess[i]

                # extra args to pass to mpfit
                fa = {'x': wave_ij, 'y': ints_ij, 'error': errs_ij, \
                      'n_gauss': self.n_gauss, 'n_poly': self.n_poly}

                # fit the profile
                out = mpfit(mpfit_deviates, parinfo=parinfo, functkw=fa, \
                            xtol=1.0E-6, ftol=1.0E-6, gtol=1.0E-6, maxiter=2000, \
                            quiet=1)

                # compute intensity
                fpeaks = out.params[peaks]
                fwdths = out.params[wdths]
                epeaks = out.perror[peaks]
                ewdths = out.perror[wdths]
                int   = np.sqrt(2*np.pi)*fpeaks*fwdths
                e_int = np.zeros(self.n_gauss)
                for n in range(self.n_gauss):
                    if fpeaks[n] != 0 and fwdths[n] != 0:
                        e_int[n] = int[n]*np.sqrt((epeaks[n]/fpeaks[n])**2+ \
                                                  (ewdths[n]/fwdths[n])**2)
                    else:
                        e_int[n] = np.nan

                # check convergence status
                if out.status > 0:
                    # assemble fit structure
                    fit['status'][ii,jj]          = out.status
                    fit['chi2'][ii,jj]            = out.fnorm/out.dof
                    fit['wavelength'][ii,jj,::]   = self.wave[ii,jj,::]
                    fit['peak'][ii,jj,::]         = out.params[peaks]
                    fit['e_peak'][ii,jj,::]       = out.perror[peaks]
                    fit['centroid'][ii,jj,::]     = out.params[cents]
                    fit['e_centroid'][ii,jj,::]   = out.perror[cents]
                    fit['width'][ii,jj,::]        = out.params[wdths]
                    fit['e_width'][ii,jj,::]      = out.perror[wdths]
                    fit['background'][ii,jj,::]   = out.params[backs]
                    fit['e_background'][ii,jj,::] = out.perror[backs]
                    fit['params'][ii,jj,::]       = out.params
                    fit['perror'][ii,jj,::]       = out.perror
                    fit['int'][ii,jj,::]          = int
                    fit['e_int'][ii,jj,::]        = e_int
                else:
                    print(' ! fit did not converge!')
                    fit['status'][ii,jj]          = out.status

        self.fit = fit

        # print status
        print(' + fit completed!')

        # timer
        t2 = datetime.now()
        print(' + fit runtime : {}'.format(t2-t1))


if __name__ == '__main__':

    from eis_read_raster import eis_read_raster
    from eis_read_template import eis_read_template
    import matplotlib.pyplot as plt

    # input data and template files
    file_data = '../1-convert/data/eis_20190404_131513.data.h5'
    file_template = '../1-convert/eis_templates/fe_12_195_119.2c.template.h5'

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
    fits     = fit.fit
    fit      = fits['int'][::,::,(fits['component']-1)]
    range    = np.percentile(fit, (1, 99))
    range    = range[1]*np.array([1.0E-2, 1.0])
    scaled   = np.log10(np.clip(fit, range[0], range[1]))
    plt.subplot(122)
    plt.imshow(scaled, origin='lower', aspect=1/x_scale, cmap='gray')
    plt.title('Fit')
    plt.tight_layout()
    plt.show()
