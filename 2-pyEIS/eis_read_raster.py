
import numpy as np
import h5py
import sys
import os

class eis_read_raster:

    def __init__(self, input_filename=None, input_iwin=0):
        self.status = False
        self.filename_data = None
        self.filename_head = None
        self.input_iwin = input_iwin
        self.iwin = None
        self.iwin_str = None
        self.wininfo = None
        self.data = {}

        if input_filename is not None:
            # check for the files
            self.check_input_filename(input_filename)
            # read the wininfo so we can find the window
            self.read_wininfo()
            self.find_window()
            # read everything
            self.read_data()
            self.read_index()
            self.read_pointing()
            self.read_cal()
            self.read_wave_corr()

    def check_input_filename(self, input_filename):
        filename_data = input_filename.replace('.head.h5', '.data.h5')
        filename_head = input_filename.replace('.data.h5', '.head.h5')

        # exit if the data or head file does not exist
        if not os.path.isfile(filename_data):
            print(' ! data file does not exist ' + filename_data)
            sys.exit()
        else:
            self.filename_data = filename_data
            print(' + data file = ' + filename_data)
        if not os.path.isfile(filename_head):
            print(' ! head file does not exist ' + filename_head)
            sys.exit()
        else:
            self.filename_head = filename_head
            print(' + head file = ' + filename_head)

    def read_wininfo(self):
        # Read in min and max wavelength for each window, for searching
        f_head = h5py.File(self.filename_head, 'r')
        nwin, = f_head['/wininfo/nwin']
        dt = np.dtype([('line_id', 'U64'), ('wvl_min', 'f'), ('wvl_max','f')])
        wininfo = np.zeros((nwin,), dtype=dt)
        wininfo = wininfo.view(np.recarray)
        for iwin in range(nwin):
            line_id, = f_head[f'/wininfo/win{iwin:02d}/line_id']
            wvl_min, = f_head[f'/wininfo/win{iwin:02d}/wvl_min']
            wvl_max, = f_head[f'/wininfo/win{iwin:02d}/wvl_max']
            wininfo[iwin].line_id = line_id.decode('utf-8')
            wininfo[iwin].wvl_min = wvl_min
            wininfo[iwin].wvl_max = wvl_max
        f_head.close()
        self.wininfo = wininfo

    def find_window(self):
        # exit if desired window does not exist
        if int(self.input_iwin) < 25:
            # input is < 25, interpret as window number
            if self.input_iwin >=0 and self.input_iwin < len(self.wininfo):
                self.iwin = self.input_iwin
                self.iwin_str = f'win{self.iwin:02d}'
                print(f' + found window {self.iwin}')
                return
            else:
                print(' ! window not found, input = {self.input_iwin}')
                sys.exit()
        else:
            # interpret input as wavelength
            wvl = float(self.input_iwin)
            p = (self.wininfo.wvl_max - wvl)*(wvl - self.wininfo.wvl_min)
            iwin, = np.where(p >= 0)
            if len(iwin) == 1:
                self.iwin = iwin[0]
                self.iwin_str = f'win{self.iwin:02d}'
                print(f' + found {wvl:.2f} in window {self.iwin}')
                return
            else:
                print(f' ! wavelength not found, input = {self.input_iwin}')
                sys.exit()

    def read_data(self):
        f_data = h5py.File(self.filename_data, 'r')
        self.data['data'] = np.array(f_data['level1/'+self.iwin_str])
        f_data.close()

    def read_index(self):
        f_head = h5py.File(self.filename_head, 'r')
        index = {}
        for key in f_head['index']:
            val = (f_head['index/'+key])[0]
            if type(val) == np.bytes_:
                val = val.decode('utf-8') # convert bytes to unicode
            index[key] = val
        f_head.close()
        self.data['index'] = index

    def read_pointing(self):
        f_head = h5py.File(self.filename_head, 'r')
        pointing = {}
        for key in f_head['pointing']:
            val = (f_head['pointing/'+key])[0]
            if type(val) == np.bytes_:
                val = val.decode('utf-8') # convert bytes to unicode
            pointing[key] = val
        f_head.close()
        self.data['pointing'] = pointing

    def read_cal(self):
        f_head = h5py.File(self.filename_head, 'r')
        self.data['wave'] = np.array(f_head['wavelength/'+self.iwin_str])
        self.data['radcal'] = np.array(f_head['radcal/'+self.iwin_str+'_pre'])
        self.data['slit_width'] = np.array(f_head['instrumental_broadening/slit_width'])
        self.data['ccd_offset'] = np.array(f_head['ccd_offsets/'+self.iwin_str])
        f_head.close()

    def read_wave_corr(self):
        f_head = h5py.File(self.filename_head, 'r')
        self.data['wave_corr'] = np.array(f_head['wavelength/wave_corr'])
        f_head.close()


if __name__ == '__main__':

    filename = 'data/eis_20190404_131513.data.h5'
    wave = 195.119
    eis = eis_read_raster(filename, wave)

    print(f'date_obs = ' + eis.data['index']['date_obs'])
    shape = eis.data['data'].shape
    print(f'data shape = {shape}')
