
import numpy as np
import h5py
import sys

# function to convert line ids to string name
def lineid_to_name(lineid,component):
    # get components of string
    split   = lineid.split(' ')
    element = split[0].lower()
    ion     = split[1]
    wave    = split[2].split('.')
    # fix element symbol
    if len(element) == 1: element = element[0]+'_'
    # convert roman numeral to integer
    roman = {'I':1, 'V':5, 'X':10, 'L':50}
    nion  = len(ion)
    numbr = 0
    for i in range(nion):
        if (i+1) == nion or roman[ion[i]] >= roman[ion[i+1]]:
            numbr += roman[ion[i]]
        else:
            numbr -= roman[ion[i]]
    # assemble string name
    name = element+'_'+str(numbr)+'_'+str(wave[0])+'_'+str(wave[1])+'_'+str(component)+'c'
    return name

# function to save fit dictionary
def save_fit(fit, file_data):
    # -------------------------------------------------
    # fit       = fit dictionary returned from fiting routine
    # file_data = filename of input data file
    #             (eg: 'eis_20190404_131513.data.h5')
    # -------------------------------------------------

    # check inputs
    try:
        keys  = fit.keys()
        nkeys = len(keys)
        if nkeys > 0: print(' + {:2} keys found in fit dictionary'.format(nkeys))
    except:
        print(' ! no keys found in fit dictionary ... stopping')
        sys.exit()

    # get file name string
    dname = file_data.split('/')[-1].split('.')[0]

    # list to collect file names
    fnames = []

    # save to hdf
    nlines = fit['n_gauss']
    for i in range(nlines):
        # get line id string
        lname = lineid_to_name(fit['line_ids'][i], i+1)
        fname = dname+'.'+lname+'.fit.h5'
        # write to hdf
        f_fit = h5py.File(fname, 'w')
        for key in keys:
            if key == 'component':
                f_fit.create_dataset(key,data=i+1)
            elif key == 'line_ids':
                lineids = fit[key].astype(h5py.special_dtype(vlen=str))
                f_fit.create_dataset(key,data=lineids)
            else:
                f_fit.create_dataset(key,data=fit[key])
        f_fit.close()
        fnames.append(fname)
        print(' + file saved = '+fname)

    return fnames


if __name__ == '__main__':

    from eis_fit_dictionary import fit_dictionary

    fit = fit_dictionary(512,87,24,2,1)
    fit['line_ids'] = np.array(['Fe XII 195.119', 'Fe XII 195.179'])

    filename = 'eis_test_fit.h5'
    file_fit = save_fit(fit, filename)
