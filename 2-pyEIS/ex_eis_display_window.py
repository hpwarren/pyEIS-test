
import matplotlib.pyplot as plt
import numpy as np
import sys

from eis_read_raster import eis_read_raster
from matplotlib.widgets import Button, RadioButtons

widget_color = 'lightgoldenrodyellow'

# read the data
filename = 'data/eis_20190404_131513.data.h5'
wave = 195.119
eis = eis_read_raster(filename, wave)

# setup the raster
data = eis.data['data']
radcal = eis.data['radcal']
wave = eis.data['wave']
cal_status = 'counts'

raster = np.sum(data, axis=2)
range = np.percentile(raster, (1, 99))
range = range[1]*np.array([1.0E-2, 1.0])
print(range)
scaled = np.clip(raster, range[0], range[1])
scaled = np.log10(raster)
x_scale = eis.data['pointing']['x_scale']

def exit_widget(event):
    sys.exit()

def set_cal_status(label):
    global cal_status
    cal_status = label

def onclick(event):
    # get calibration data based on pixel location and update plot
    if event.xdata is None or event.ydata is None: return
    ix, iy = int(event.xdata), int(event.ydata)
    if ix <= 0 or ix > data.shape[1]: return
    if iy <= 0 or iy > data.shape[0]: return
    spec = data[iy,ix]
    if cal_status == 'ergs': spec *= radcal

    spectrum.set_xdata(wave)
    spectrum.set_ydata(spec)
    ax2.set_xlim(np.min(wave), np.max(wave))
    ax2.set_ylim(0, 1.25*np.max(spec))
    ax2.set_ylabel('Intensity (' + cal_status + ')')

    ax1.clear()
    ax1.imshow(scaled, origin='lower', aspect=1/x_scale, cmap='gray')
    ax1.scatter([ix], [iy], marker='+')

    fig.canvas.draw_idle()

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 8))
fig.canvas.mpl_connect('button_press_event', onclick)

ax1.imshow(scaled, origin='lower', aspect=1/x_scale, cmap='gray')
ax1.set_xlabel('Solar X (pixels)')
ax1.set_ylabel('Solar Y (pixels)')

spectrum, = ax2.step([], [])
ax2.set_xlabel('Wavelength ($\AA$)')
ax2.set_ylabel('Intensity (counts)')

ax = plt.axes([0.05, 0.925, 0.1, 0.05], facecolor=widget_color)
button = Button(ax, 'Quit', color=widget_color)
button.on_clicked(exit_widget)

ax = plt.axes([0.2, 0.925, 0.1, 0.05], facecolor=widget_color)
radio = RadioButtons(ax, ('counts', 'ergs'))
radio.on_clicked(set_cal_status)

plt.show()
