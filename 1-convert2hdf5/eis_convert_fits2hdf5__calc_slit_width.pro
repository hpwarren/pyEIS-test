
pro eis_convert_fits2hdf5::calc_slit_width

  self.getProperty, eis_level1_data=eis_level1_data

  d = *eis_level1_data[0]
  slit_ind = d.hdr.slit_ind  
  ypix = indgen(d.ny) + d.hdr.yws
  slit_width = eis_slit_width(ypix, slit_ind=slit_ind)

  self.setProperty, slit_width=slit_width

end