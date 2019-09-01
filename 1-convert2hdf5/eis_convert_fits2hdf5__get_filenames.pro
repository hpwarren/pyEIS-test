
pro eis_convert_fits2hdf5::get_filenames, file_data, file_head

  self.getProperty, eis_level0_filename=eis_level0_filename

  break_file, eis_level0_filename, disk, dir, name, ext

  name = str_replace(name, '_l0_', '_')

  file_data = name + '.data.h5'
  file_head = name + '.head.h5'

  file_data = concat_dir('data', file_data)
  file_head = concat_dir('data', file_head)
  
  print, file_data
  print, file_head

end