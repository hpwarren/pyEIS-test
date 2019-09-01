
function eis_convert_fits2hdf5::init, eis_level0_filename
  compile_opt idl2

  self.d = hash()

  if keyword_set(eis_level0_filename) then begin
    self.setProperty, eis_level0_filename=eis_level0_filename
    self.read_eis
    self.calc_pointing
    self.calc_radcal
    self.calc_ccd_offsets
    self.calc_slit_width
    self.write_data
    self.write_head
  endif

return, obj_valid(self.d)
end

;+
; $Id:$
;-
pro eis_convert_fits2hdf5__define

  _ = {eis_convert_fits2hdf5,$
       INHERITS nrl_object}

end
