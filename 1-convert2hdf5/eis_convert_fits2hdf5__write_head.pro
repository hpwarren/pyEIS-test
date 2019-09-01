
;; +
;; a generic routine for looping over the variables in a structure and writing them to a group
;; -
pro write_structure, parent_id, group_name, stc
  subgroup_id = H5G_CREATE(parent_id, group_name)
  print, '+ group name : ' + group_name

  names = tag_names(stc)
  for n=0, n_elements(names)-1 do begin
    this_name = strlowcase(names[n])
    eis_save_hdf_variable, stc.(n), this_name, subgroup_id, /verbose
  endfor

  h5g_close, subgroup_id
end

;; +
;; write each element of wininfo structure
;; -
pro write_wininfo, parent_id, wininfo
  group_id = H5G_CREATE(parent_id, 'wininfo')
  print, '+ group name : wininfo'

  nwin = n_elements(wininfo)
  eis_save_hdf_variable, nwin, 'nwin', group_id, /verbose

  for iwin=0, nwin-1 do begin
    subgroup_name = 'win' + trim(iwin, '(i2.2)')
    write_structure, group_id, subgroup_name, wininfo[iwin]
  endfor

  h5g_close, group_id
end

;; +
;; write wavelength information for each window
;; -
pro write_wavelength, parent_id, eis_level1_data
  group_id = H5G_CREATE(parent_id, 'wavelength')
  print, '+ group_name : wavelength'

  nwin = n_elements(eis_level1_data)
  for iwin=0, nwin-1 do begin
    d = *eis_level1_data[iwin]
    if iwin eq 0 then begin
      eis_save_hdf_variable, d.wave_corr, 'wave_corr', group_id, /verbose
      eis_save_hdf_variable, d.wave_corr_tilt, 'wave_corr_tilt', group_id, /verbose
      eis_save_hdf_variable, d.wave_corr_t, 'wave_corr_t', group_id, /verbose
    endif
    eis_save_hdf_variable, d.wvl, 'win' + trim(iwin, '(i2.2)'), group_id, /verbose
  endfor

  h5g_close, group_id
end

;; +
;; write radiometric calibration information
;; -
pro write_radcal, parent_id, radcal
  group_id = H5G_CREATE(parent_id, 'radcal')
  print, '+ group_name : radcal'

  nwin = n_elements(radcal)
  for iwin=0, nwin-1 do begin
    ph2erg = (*radcal[iwin]).ints_erg
    eis_save_hdf_variable, ph2erg, 'win'+trim(iwin,'(i2.2)')+'_pre', group_id, /verbose
  endfor

  h5g_close, group_id
end

;; +
;; write ccd offsets for each window
;; -
pro write_ccd_offsets, parent_id, ccd_offsets
  group_id = H5G_CREATE(parent_id, 'ccd_offsets')
  print, '+ group_name : ccd_offsets'

  nwin = n_elements(ccd_offsets)
  for iwin=0, nwin-1 do begin
    offsets = *ccd_offsets[iwin]
    eis_save_hdf_variable, offsets, 'win'+trim(iwin,'(i2.2)'), group_id, /verbose
  endfor

  h5g_close, group_id
end

;; +
;; write the instrumental broadening as a function of position
;; -
pro write_slit_width, parent_id, slit_width
  group_id = H5G_CREATE(parent_id, 'instrumental_broadening')
  print, '+ group_name : instrumental_broadening'

  eis_save_hdf_variable, slit_width, 'slit_width', group_id, /verbose
  eis_save_hdf_variable, 'Angstroms', 'slit_width_units', group_id, /verbose

  h5g_close, group_id
end

;; +
;; write the instrumental broadening as a function of position
;; -
pro write_exposure_times, parent_id, exposure_times
  group_id = H5G_CREATE(parent_id, 'exposure_times')
  print, '+ group_name : exposure_times'

  eis_save_hdf_variable, exposure_times, 'duration', group_id, /verbose
  eis_save_hdf_variable, 'seconds', 'duration_units', group_id, /verbose

  h5g_close, group_id
end

;; +
;; write the head file
;; -
pro eis_convert_fits2hdf5::write_head

  self.getProperty, wininfo=wininfo, index=index, radcal=radcal, ccd_offsets=ccd_offsets
  self.getProperty, pointing=pointing, slit_width=slit_width, exposure_times=exposure_times
  self.getProperty, eis_level0_data=eis_level0_data
  self.getProperty, eis_level1_data=eis_level1_data

  self.get_filenames, file_data, file_head

  if file_exist(file_head) then file_delete, file_head
  file_id = h5f_create(file_head)

  write_wininfo, file_id, wininfo
  write_structure, file_id, 'index', index
  write_wavelength, file_id, eis_level1_data
  write_radcal, file_id, radcal
  write_ccd_offsets, file_id, ccd_offsets
  write_structure, file_id, 'pointing', pointing
  write_slit_width, file_id, slit_width
  write_exposure_times, file_id, exposure_times

  h5f_close, file_id

end