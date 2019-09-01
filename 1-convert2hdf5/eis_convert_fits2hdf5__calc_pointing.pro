
pro eis_convert_fits2hdf5::calc_pointing

  self.getProperty, eis_level1_data=eis_level1_data

  ;; +
  ;; each solar y accounts for the ccd offset for that wind, reverse that and create a single array
  ;; corresponding to the He II wavelength
  ;; -
  nwin = n_elements(eis_level1_data)
  for iwin=0, nwin-1 do begin
    d = *eis_level1_data[iwin]
    if iwin eq 0 then solar_y = fltarr(nwin, d.ny)
    solar_y[iwin, *] = d.solar_y + (eis_ccd_offset(median(d.wvl)))[0]
  endfor
  solar_y = median(solar_y, dimension=1)

  scale = float(d.scale)
  offsets = float(eis_aia_offsets(d.hdr.date_obs))
  solar_x = float(d.solar_x)

  fovx = float(d.hdr.nraster*d.scale[0])
  fovy = float(d.ny)
  ycen = float(median(solar_y))
  xcen = float(solar_x[-1] - d.hdr.nraster*d.scale[0]/2.)
  
  pointing = {x_scale: scale[0], $
              y_scale: scale[1], $
              offset_x: offsets[0], $
              offset_y: offsets[1], $              
              solar_x: solar_x, $
              solar_y: solar_y, $
              fovx: fovx, $
              fovy: fovy, $
              xcen: xcen, $
              ycen: ycen, $
              ref_time: d.hdr.date_obs}
  
  self.setProperty, pointing=pointing

end