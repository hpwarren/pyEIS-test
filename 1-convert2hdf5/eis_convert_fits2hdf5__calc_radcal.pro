
pro eis_convert_fits2hdf5::calc_radcal

  self.getProperty, eis_level1_data=eis_level1_data

  nwin = n_elements(eis_level1_data)
  radcal = ptrarr(nwin)
  for iwin=0, nwin-1 do begin
    d = *eis_level1_data[iwin]
    if iwin eq 0 then begin
      ;; some exposures may have bad times? filter then with median filter
      med_exp_time = median(d.exposure_time)
      slit_ind = d.hdr.slit_ind
    endif

    this_radcal = eis_throughput(d.wvl, ints_ph_d=replicate(1.0, d.nl), $
                                 exposure_time=med_exp_time,  slit=slit_ind, /per)

    radcal[iwin] = ptr_new(this_radcal)
  endfor

  self.setProperty, radcal=radcal
end