import os.path
import shutil
import time

class Hotfolder(object):
    
  def __init__(self, source_path, dest_path, cycles, wait, os, label):
    print "Starting hotfoler - " + label + "...."
    self._source_path = source_path
    self._dest_path = dest_path
    self._cycles = cycles
    self._wait = wait
    self._os = os
    self._file_hash = {}
    self._delete_source = False
    self._name = label
    # NOTES
    # Check all conditions on startup.
    # recursive dir vs static folder.
    # make it run via cli
    print "Initialization complete."

  def set_delete_source(self, val):
    self._delete_source = val

  # Remove foo
  def scan_fs(self):
    os.path.walk(self._source_path, self.load_files, "foo")
        
  def load_files(self, arg, dir, files):
    for file in files:
      if self.is_stable(os.path.join(dir, file)):
        des_dir = dir.replace(self._source_path, self._dest_path)
        self.copy_file( os.path.join(dir, file), os.path.join(des_dir, file) )
        del self._file_hash[ os.path.join(dir, file) ]

  def process_cycle(self):
    self.scan_fs()

  def process_continuous(self):
    while True:
      self.scan_fs()
      print "sleeping for " + str(self._wait) + " seconds."
      time.sleep(self._wait)

  def copy_file(self, source, destination):
    if not os.path.isdir(source):
      print "Source: " + source
      print "Dest: " + destination    
      if not os.path.exists(os.path.dirname(destination)):
        print "Creating directory: " + os.path.dirname(destination)
        os.makedirs(os.path.dirname(destination))
      shutil.copy(source, destination)
      if self._delete_source:
        print "Deleting: " + source 
        os.remove(source)
      
  def is_stable(self, file):
    size = str(os.path.getsize(file))
    if os.path.isfile(file):
      if self._file_hash.has_key(file):
        print "Updating " + file + " in hash with size: " + str(size)
        self._file_hash[file].append(size)
        if self._file_hash[file].count(size) == self._cycles + 1:
          print "file is stable"
          return True
        else:
          print "file is not stable"
          return False
      else:
        print "Adding " + file + " to hash with size: " + str(size)
        self._file_hash[file] = [size]
        return False

