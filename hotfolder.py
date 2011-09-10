import os.path
import os
import sys
import shutil
import time

# NOTES
# recursive dir vs static folder.
# check for a specific version of python
# convert copy and delete to move
# add logging
# add a cli interpreter class?

class Hotfolder(object):
    
  def __init__(self, source_path, dest_path, cycles, wait, label):
    print 20*"*"
    print "Starting hotfolder - " + label + "...."
    self._source_path = source_path
    self._dest_path = dest_path
    self._cycles = cycles
    self._wait = wait
    self._os = sys.platform
    self._file_hash = {}
    self._delete_source = False
    self._scan_tree = False
    self._scan_folder = True
    self._dest_tree = False
    self._dest_folder = True
    self._name = label
    self.print_configuration()
    self.validate_configuration()
    print "Initialization complete."

  def print_configuration(self):
    print "Hotfolder configuration:"
    print "Source: " + str(self._source_path)
    print "Destination: " + str(self._dest_path)
    print "Stable cycles: " + str(self._cycles)
    print "Wait between cycles: " + str(self._wait) + " seconds"
    print "System Platform: " + sys.platform + " - " + sys.version
    print "Hotfolder name: " + str(self._name)
    print "Delete source: " + str(self._delete_source)
    print 20*"*" 

  def set_delete_source(self, val):
    self._delete_source = val

  def set_scan_tree(self, val):
    self._scan_tree = val
    self._scan_folder = not val

  def set_scan_folder(self, val):
    self._scan_tree = not val
    self._scan_folder = val

  def set_destination_tree(self, val):
    self._dest_tree = val
    self._dest_folder = not val

  def set_destination_folder(self, val):
    self._dest_tree = not val
    self._dest_folder = val

  def validate_configuration(self):
    if self._source_path == self._dest_path:
      print "Configuration error: The source and destination can't be the same."
      exit(0)
    if (not os.path.exists(self._source_path) or not os.path.isdir(self._source_path)):
      print "Configuration error: The source directory is not valid."
      exit(0)
    if (not os.path.exists(self._dest_path) or not os.path.isdir(self._dest_path)):
      print "Configuration error: The destination directory is not valid."
      exit(1)
    if (self._source_path == "" or self._dest_path == ""):
      print "Configuration error: The paths are invalid"
      exit(0)

  def scan_fs(self):
    if self._scan_tree:
      os.path.walk(self._source_path, self.load_files, "")
    else:
      entries = os.listdir(self._source_path)
      for entry in entries:
        print entry
        if os.path.isfile(os.path.join(self._source_path, entry)):
          if self.is_stable(os.path.join(self._source_path, entry)):
            self.copy_file(os.path.join(self._source_path, entry), os.path.join(self._dest_path, entry))
            del self._file_hash[os.path.join(self._source_path, entry)]
            
  def load_files(self, arg, dir, files):
    if self._dest_tree:
      for file in files:
        if self.is_stable(os.path.join(dir, file)):
          des_dir = dir.replace(self._source_path, self._dest_path)
          self.copy_file( os.path.join(dir, file), os.path.join(des_dir, file) )
          del self._file_hash[ os.path.join(dir, file) ]
    else:
      for file in files:
        if self.is_stable(os.path.join(dir, file)):
          self.copy_file( os.path.join(dir, file), os.path.join(self._dest_path, file) )
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

