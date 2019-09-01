
import numpy as np
import h5py
import sys
import os

class eis_read_template:

    def __init__(self, input_filename=None):
        self.status = False
        self.filename_temp = None
        self.template = None
        self.parinfo = None

        if input_filename is not None:
            self.check_input_filename(input_filename)
            self.read_template()
            self.read_parinfo()
            self.print_parinfo()

    def check_input_filename(self, input_filename):
        # exit if the template file does not exist
        if not os.path.isfile(input_filename):
            print(' ! template file does not exist ' + input_filename)
            sys.exit()
        else:
            self.filename_temp = input_filename
            print(' + template file = ' + input_filename)

    def read_template(self):
        # read template
        f_temp = h5py.File(self.filename_temp, 'r')
        template = {}
        for key in f_temp['template']:
            tag = f_temp['template/'+key]
            if len(tag) > 1:
                tag = np.array(tag)
                if key == 'line_ids':
                    tag = np.char.decode(tag) # convert bytes to unicode
            else:
                tag = tag[0]
            template[key] = tag
        f_temp.close()
        self.template = template

    def read_parinfo(self):
       # read parinfo
       f_temp = h5py.File(self.filename_temp, 'r')
       nstr = len(f_temp['parinfo/value'])
       parinfo = []
       for istr in range(nstr):
           temp = {}
           for key in f_temp['parinfo']:
               tag = f_temp['parinfo/'+key][istr]
               if key == 'tied':
                   tag = np.char.decode(tag) # convert bytes to unicode
               temp[key] = tag
           parinfo.append(temp)
       f_temp.close()
       self.parinfo = parinfo

    def print_parinfo(self):
        print(' *PARAMETER CONSTRAINTS* ')
        print('{:>1} {:>18} {:>10} {:>18} {:>22} {:>18}'.format(\
              ' *','Value','Fixed','Limited','Limits','Tied'))
        for i in range(len(self.parinfo)):
            p0 = 'p['+str(i)+']'
            p1 = self.parinfo[i]['value']
            p2 = self.parinfo[i]['fixed']
            p3 = self.parinfo[i]['limited'][0]
            p4 = self.parinfo[i]['limited'][1]
            p5 = self.parinfo[i]['limits'][0]
            p6 = self.parinfo[i]['limits'][1]
            p7 = self.parinfo[i]['tied']
            print('{:>6} {:14.4f} {:10d} {:10d} {:10d} {:12.4f} {:12.4f} {:>18}'.format(\
                  p0,p1,p2,p3,p4,p5,p6,p7))


if __name__ == '__main__':

    filename = 'data/fe_12_195_119.2c.template.h5'
    eis = eis_read_template(filename)

    print('template')
    print('---------')
    t = eis.template
    for key in t.keys():
        print('{:12} {:12} {:4d}'.format(key,str(t[key].dtype),np.size(t[key])))

    print('parinfo['+str(len(eis.parinfo))+']')
    print('---------')
    t = eis.parinfo[0]
    for key in t.keys():
        print('{:12} {:12} {:4d}'.format(key,str(t[key].dtype),np.size(t[key])))
