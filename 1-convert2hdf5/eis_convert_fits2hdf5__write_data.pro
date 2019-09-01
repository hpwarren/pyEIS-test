
pro eis_convert_fits2hdf5::write_data

  self.getProperty, eis_level0_data=eis_level0_data
  self.getProperty, eis_level1_data=eis_level1_data
  self.get_filenames, file_data, file_head

  if file_exist(file_data) then file_delete, file_data
  file_id = h5f_create(file_data)

  ;; +
  ;; write all of the level0 data to a group
  ;; -

  if keyword_set(write_level0) then begin
    group_id = H5G_CREATE(file_id, 'level0')
    print, '+ group name : level0'
    
    name = 'level0/intensity_units'
    eis_save_hdf_variable, 'DN', name, file_id, /verbose
    
    nwin = n_elements(eis_level0_data)
    for iwin=0, nwin-1 do begin
      d = *eis_level0_data[iwin]
      name = 'level0/win' + trim(iwin, '(i2.2)')
      eis_save_hdf_variable, d.int, name, file_id, /verbose
    endfor
    
    h5g_close, group_id    
  endif

  ;; +
  ;; write all of the level1 data to a group
  ;; -

  group_id = H5G_CREATE(file_id, 'level1')
  print, '+ group name : level1'  

  name = 'level1/intensity_units'
  eis_save_hdf_variable, 'Counts', name, file_id, /verbose  

  nwin = n_elements(eis_level1_data)
  for iwin=0, nwin-1 do begin
    d = *eis_level1_data[iwin]
    name = 'level1/win' + trim(iwin, '(i2.2)')
    eis_save_hdf_variable, d.int, name, file_id, /verbose
  endfor

  h5g_close, group_id

  h5f_close, file_id

end