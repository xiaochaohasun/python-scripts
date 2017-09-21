#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pyinotify
 
WATCH_PATH = '/home/rsync_dir/' 
LOG_PATH='/home/rsync_dir.log'

class OnIOHandler(pyinotify.ProcessEvent):
  def process_IN_CREATE(self, event):
    print "create file: %s " % os.path.join(event.path,event.name)
    #rsync to hosts
 
  def process_IN_DELETE(self, event):
    print "delete file: %s " % os.path.join(event.path,event.name)
    #rsync to hosts
 
  def process_IN_MODIFY(self, event):
    print "modify file: %s " % os.path.join(event.path,event.name)
    #rsync to hosts

  def process_IN_CLOSE_WRITE(self,event):
    print "close_write file: %s " % os.path.join(event.path,event.name)
    #rsync to hosts

 
def monitor_rsync(path):
  wm = pyinotify.WatchManager()
  mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY | pyinotify.IN_CLOSE_WRITE
  notifier = pyinotify.ThreadedNotifier(wm, OnIOHandler())
  notifier.start()
  wm.add_watch(path, mask,rec = True,auto_add = True)
  print 'Start Watch','Start monitoring %s' % path
  while True:
    try:
      notifier.process_events()
      if notifier.check_events():
        notifier.read_events()
        write_Stdout_log
    except KeyboardInterrupt:
      notifier.stop()
      break
 
if __name__ == "__main__":
   monitor_rsync(WATCH_PATH)
