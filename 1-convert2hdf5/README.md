
#### Test Convert

`test_eis_convert.pro` : reads an EIS file and converts it to HDF5

```
eis_20190404_131513.data.h5 <- just the data (level0 and level1)
eis_20190404_131513.head.h5 <- header and calibration information
```

#### Test Read IDL

`test_read_eis.pro` : reads and displays data from a calibrated EIS file

#### Test Read python

`test_read_eis.py` : reads the same data from the HDF file. Note that there are small differences
in the calibration curves, so the numbers don't match exactly. 


####  Philosophy

The main idea is to prep the file, collect all of the information that the user would usually
derive from various IDL routines, and write all of it to an HDF5 file. This way the python user
doesn't need to worry about using IDL for any of the analysis. 

```
self.read_eis <- read eis level0 and level1 files, level1 is prepped to counts (not ergs)
self.calc_radcal <- compute the absolute calibration for each window
self.write_data <- write the data to X.data.h5
self.write_head <- write the header and calibration data to X.head.h5
```	

Progress on header file so far

```
write_wininfo, file_id, wininfo <- structure containing wavelength ranges for each window
write_structure, file_id, 'index', index <- the entire primary header (index)
write_wavelength, file_id, eis_level1_data <- wavelength array and correction for each window
write_radcal, file_id, radcal <- absolute calibration for each window
write_ccd_offsets, file_id, ccd_offsets <- ccd offsets as a function of wavelength
write_structure, file_id, 'pointing', pointing  <- pointing information, including EIS/AIA
write_slit_width, file_id, slit_width <- instrumental broadening as a function of slit position
```

To do

```
;; context information? EIT, AIA, and/or magentic field
;; make an X.fits.h5 file with some profile fits?
```
