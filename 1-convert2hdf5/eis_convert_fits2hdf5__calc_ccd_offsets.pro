
pro eis_convert_fits2hdf5::calc_ccd_offsets
  
  self.getProperty, eis_level1_data=eis_level1_data

  nwin = n_elements(eis_level1_data)
  ccd_offsets = ptrarr(nwin)

  for iwin=0, nwin-1 do begin
    d = *eis_level1_data[iwin]
    this_offset = eis_ccd_offset(d.wvl)
    ccd_offsets[iwin] = ptr_new(this_offset)
  endfor

  self.setProperty, ccd_offsets=ccd_offsets
    
end