import os.path
import shutil

class Hotfolder(object):
    
  def __init__(self, source_path, dest_path, cycles, wait, os):
    self._source_path = source_path
    self._dest_path = dest_path
    self._cycles = cycles
    self._wait = wait
    self._os = os
    self._file_hash = {}
      
  def scan_fs(self):
    os.path.walk(self._source_path, self.load_files, "foo")

  def load_files(self, arg, dir, files):
    for file in files:
      if os.path.join(dir, file) not in self._file_hash:
        self._file_hash[os.path.join(dir, file)] = os.path.getsize(os.path.join(dir, file))
        print os.path.join(dir, file)
      else:
        des_dir = dir.replace(self._source_path, self._dest_path)
        self.copy_file( os.path.join(dir, file), os.path.join(des_dir, file) )
        del self._file_hash[os.path.join(dir, file)]
        
  def process(self):
    self.scan_fs()
    self.scan_fs()

  def copy_file(self, source, destination):
    if not os.path.isdir(source):
      print "Source: " + source
      print "Dest: " + destination    
      if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination))
      shutil.copy(source, destination)
      os.remove(source)

