
pro eis_convert_fits2hdf5::read_eis

  ;; +
  ;; to speed up testing, save results to a file
  ;; -

  self.get_filenames, file_data, file_head  
  temp_file = str_replace(file_data, '.data.h5', '') + '.sav'
  print, temp_file
  
  if file_exist(temp_file) then begin
    restore, temp_file
    self.setProperty, index=index
    self.setProperty, wininfo=wininfo
    self.setProperty, eis_level0_data=eis_level0_data
    self.setProperty, eis_level1_data=eis_level1_data
    self.setProperty, exposure_times=exposure_times
    return
  endif

  ;; +
  ;; for now these are local files, in the end we will get the files from the archives
  ;; -
  self.getProperty, eis_level0_filename=eis_level0_filename

  ;; +
  ;; index is primary header
  ;; -
  mreadfits, eis_level0_filename, index, /nodata

  ;; +
  ;; eis_get_wininfo is useful for getting all of the window information from the header
  ;; -
  wininfo = eis_get_wininfo(eis_level0_filename, nwin=nwin)

  ;; +
  ;; now loop over all of the level0 data, so slow!
  ;; don't compute wavelength correction here
  ;; -
  eis_level0_data = ptrarr(nwin)
  for iwin=0, nwin-1 do begin
    hpw_progress_hash, iwin, nwin-1
    d = eis_getwindata(eis_level0_filename, iwin, /no_wave_corr)
    eis_level0_data[iwin] = ptr_new(d)
  endfor

  ;; +
  ;; now loop over all of the level1 data, so slow!
  ;; get wavelength correction
  ;; replace missing pixels (need a mask for this)
  ;; -   
  eis_level1_filename = str_replace(eis_level0_filename, '_l0_', '_l1_')
  eis_level1_data = ptrarr(nwin)
  for iwin=0, nwin-1 do begin
    hpw_progress_hash, iwin, nwin-1    
    d = eis_getwindata(eis_level1_filename, iwin, /replace_missing, /quiet)
    eis_level1_data[iwin] = ptr_new(d)
  endfor

  ;; +
  ;; get exposure times from last window
  ;; -
  exposure_times=d.exposure_time

  self.setProperty, wininfo=wininfo, index=index, exposure_times=exposure_times
  self.setProperty, eis_level0_data=eis_level0_data
  self.setProperty, eis_level1_data=eis_level1_data

  ;; --- to speed up testing . . .
  save, wininfo, index, eis_level0_data, eis_level1_data, exposure_times, file=temp_file, /compress

end