#### pyEIS-test

This is proof-of-concept python software for analyzing EIS data. The basic idea is to (1) process the
level-0 files to level-1 in IDL, accumulate all of the information needed to analyze the data, and
write everything to an HDF5 file, (2) write routines in Python for reading these HDF5 files, and
(3) provide a document describing basic analysis procedures.

There are currently three subdirectories

* 1-convert2hdf5: this is the IDL software used to read the level-1 file and write it to HDF5. If
  you're interested in how the HDF5 file was created, look here. Note that we haven't yet included
  all of the files you'd need to run this software.
  
* 2-pyEIS: this directory contains an example HDF5 file and some software routines for reading and
  displaying the data. Routines for fitting the data using a port of MPFIT to python are also
  here. Anaconda and Python 3.7 is assumed.
  
* 3-EAG: a very early attempt at writing a coherent set of documentation for these python routines.  

It is important to remember that this is "minimum viable example" python software. The primary goal
is to get feedback.
