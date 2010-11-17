import os.path
import sys
import shutil
import time

# NOTES
# recursive dir vs static folder.
# check for a specific version of python

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
    self._name = label
    self.print_configuration()
    self.validate_configuration()
    print "Initialization complete."

  def print_configuration(self):
    print "Hotfolder configuration:"
    print "Source: " + str(source_path)
    print "Destination: " + str(dest_path)
    print "Stable cycles: " + str(cycles)
    print "Wait between cycles: " + str(wait) + " seconds"
    print "System Platform: " + sys.platform + " - " + sys.version
    print "Hotfolder name: " + str(label)
    print "Delete source: " + str(self._delete_source)
    print 20*"*" 

  def validate_configuration(self):
    # Check file paths
    if self._source_path == self._dest_path:
      print "Configuration error: The source and destination can't be the same."
      exit(0)
    if (not os.path.exists(self._source_path) or not os.path.isdir(self._source_path)):
      print not os.path.exists(self._source_path)
      print "Configuration error: The source directory is not valid."
      exit(0)
    if (not os.path.exists(self._dest_path) or not os.path.isdir(self._dest_path)):
      print "Configuration error: The destination directory is not valid."
      exit(1)
    print "\"%s\"" % (self._source_path)
    if (self._source_path == "" or self._dest_path == ""):
      print "Configuration error: The paths are invalid"
      exit(0)

  def set_delete_source(self, val):
    self._delete_source = val

  def scan_fs(self):
    os.path.walk(self._source_path, self.load_files, "")
        
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

src = ""
dst = ""

if __name__ == '__main__':
  try:
    test = Hotfolder(src, dst, 3, 5, "Test Hotfolder")
    test.set_delete_source(True)
    test.process_continuous()
  except (KeyboardInterrupt, SystemExit):
    print "\nApplication terminated"












