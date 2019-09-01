#### pyEIS-test

This is proof-of-concept python software for analyzing EIS data. The basic idea is to (1) process the
level-0 files to level-1 in IDL, accumulate all of the information needed to analyze the data, and
write everything to an HDF5 file, (2) write routines in Python for reading these HDF5 files, and
(3) provide a document describing basic analysis procedures.

There are currently three subdirectories

* 1-convert2hdf5: this is the IDL software used to read the level-1 file and write it to HDF5. If
  you're interested in how an HDF5 file is created, look here. Note that we haven't yet included
  all of the files you'd need to run this software. 
  
* 2-pyEIS: this directory contains an example HDF5 file and some software routines for reading and
  displaying the data. Routines for fitting the data using a port of MPFIT to python are also
  here. Anaconda and Python 3.7 is assumed.
  
  * pyEIS-test/2-pyEIS/data containes example files `eis_20190404_131513.data.h5.gz` and
    `eis_20190404_131513.head.h5`. Note that the data and header information are stored in
    different files. Remember to gunzip the data file. 
  * there are example routines (e.g., `ex_eis_display_window.py`)
  * `eis_read_raster.py`: is the routine for reading the HDF5 file
  * `eis_fit_raster.py`: fits an entire raster, very slow!
  * `eis_fit_profile.py`: fits a single spectrum
  * `eis_mpfit.py`: really mpfit.py by Sergey Koposov, which is based on IDL code by Craig
    Markwardt.
  
* 3-EAG: a very early attempt at writing a coherent set of documentation for these python routines.  

It is important to remember that this is "minimum viable example" python software. The primary goal
is to get feedback.
