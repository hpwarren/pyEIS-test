
from eis_fit_deviates import mpfit_model, mpfit_deviates
from eis_scale_guess import scale_guess
from eis_fit_dictionary import fit_dictionary
from eis_mpfit import mpfit
from datetime import datetime
import numpy as np

class eis_fit_profile:

    def __init__(self, wave, ints, errs, template, parinfo):
        self.wave     = wave
        self.template = template
        self.parinfo  = parinfo
        self.n_wave   = len(wave)
        self.n_gauss  = template['n_gauss']
        self.n_poly   = template['n_poly']
        self.fit      = None

        # get fit structure
        fit = fit_dictionary(1,1,self.n_wave,self.n_gauss,self.n_poly)
        fit['line_ids']  = template['line_ids']
        fit['n_gauss']   = self.n_gauss
        fit['n_poly']    = self.n_poly
        fit['component'] = template['component']
        peaks = np.arange(self.n_gauss)*3
        cents = np.arange(self.n_gauss)*3+1
        wdths = np.arange(self.n_gauss)*3+2
        backs = self.n_gauss*3

        # only use good data
        good = np.where(errs > 0)
        wave = wave[good]
        ints = ints[good]
        errs = errs[good]

        # timer
        t1 = datetime.now()

        # scale guess parameters to data
        oldguess = template['fit']
        newguess = scale_guess(wave,ints,oldguess,self.n_gauss,self.n_poly)

        # plug in new guess values to parinfo
        for i in range(len(newguess)):
            self.parinfo[i]['value'] = newguess[i]

        # extra args to pass to mpfit
        fa = {'x': wave, 'y': ints, 'error': errs, \
              'n_gauss': self.n_gauss, 'n_poly': self.n_poly}

        # fit the profile
        out = mpfit(mpfit_deviates, parinfo=parinfo, functkw=fa, \
                    xtol=1.0E-10, ftol=1.0E-10, gtol=1.0E-10, maxiter=2000, \
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
            print(' + fit converged!')
            # assemble fit structure
            fit['status'][0,0]          = out.status
            fit['chi2'][0,0]            = out.fnorm/out.dof
            fit['wavelength'][0,0,::]   = self.wave
            fit['peak'][0,0,::]         = out.params[peaks]
            fit['e_peak'][0,0,::]       = out.perror[peaks]
            fit['centroid'][0,0,::]     = out.params[cents]
            fit['e_centroid'][0,0,::]   = out.perror[cents]
            fit['width'][0,0,::]        = out.params[wdths]
            fit['e_width'][0,0,::]      = out.perror[wdths]
            fit['background'][0,0,::]   = out.params[backs]
            fit['e_background'][0,0,::] = out.perror[backs]
            fit['params'][0,0,::]       = out.params
            fit['perror'][0,0,::]       = out.perror
            fit['int'][0,0,::]          = int
            fit['e_int'][0,0,::]        = e_int
            # timer
            t2 = datetime.now()
            print(' + fit runtime : {}'.format(t2-t1))
        else:
            print(' ! fit did not converge!')
            fit['status'][0,0]          = out.status

        self.fit = fit


if __name__ == '__main__':

    from eis_read_raster import eis_read_raster
    from eis_read_template import eis_read_template
    import matplotlib.pyplot as plt

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
    plt.plot(wave, ints, 'k-o', label='Data')
    plt.plot(wave, fity, 'r-', label='Fit')
    plt.xlabel('Wavelength ($\AA$)')
    plt.ylabel('Intensity (counts)')
    plt.legend(loc='upper right')
    plt.text(min(wave), max(ints), '$\chi^2$='+str(chi2))
    plt.show()
