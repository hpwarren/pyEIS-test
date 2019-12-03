
pro convert_template

  template_file = 'eis_templates/fe_12_195_119.2c.template.genx'
  restgen, parinfo, template, file=template_file

  help,/str, parinfo, template

  opf = str_replace(template_file, '.genx', '.h5')

  if file_exist(opf) then file_delete, opf
  file_id = h5f_create(opf)

  subgroup_id = H5G_CREATE(file_id, 'parinfo')
  print, '+ group name : parinfo'
  stc = parinfo
  names = tag_names(stc)
  for n=0, n_elements(names)-1 do begin
    this_name = strlowcase(names[n])
    this_var  = stc.(n)
    if datatype(this_var) eq 'STR' then begin
      maxstr = max(strlen(this_var))
      for s=0, n_elements(this_var)-1 do this_var[s] = strpad(this_var[s],maxstr,/after)
    endif
    eis_save_hdf_variable, this_var, this_name, subgroup_id, /verbose
  endfor
  h5g_close, subgroup_id

  subgroup_id = H5G_CREATE(file_id, 'template')
  print, '+ group name : template'
  stc = template
  names = tag_names(stc)
  for n=0, n_elements(names)-1 do begin
    this_name = strlowcase(names[n])
    this_var  = stc.(n)
    if datatype(this_var) eq 'STR' then begin
      maxstr = max(strlen(this_var))
      for s=0, n_elements(this_var)-1 do this_var[s] = strpad(this_var[s],maxstr,/after)
    endif
    eis_save_hdf_variable, this_var, this_name, subgroup_id, /verbose
  endfor
  h5g_close, subgroup_id

  h5f_close, file_id

  print, ' + wrote ' + opf

end
