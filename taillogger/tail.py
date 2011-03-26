import time
import threading
import syslog

from os import stat
from os.path import abspath
from stat import ST_SIZE

class TailThread(threading.Thread):
    def __init__(self, log, opts):
        threading.Thread.__init__(self)
        self.log = abspath(log)
        self.opts = opts
        self.done = False
        
        try:
            self.f = open(self.log, "r")
            file_len = stat(self.log)[ST_SIZE]
            self.f.seek(file_len)
            self.pos = self.f.tell()
            
            self.dorun = True
        except:
            self.dorun = False
        
    def _reset(self):
        self.f.close()
        self.f = open(self.log, "r")
        self.pos = self.f.tell()
    
    def run(self):
        if self.dorun:
            while True:
                self.pos = self.f.tell()
                line = self.f.readlines()

                if not line:
                    if stat(self.log)[ST_SIZE] < self.pos:
                        self._reset()
                    else:
                        time.sleep(5)
                        self.f.seek(self.pos)
                else:
                    #
                    # send to syslog
                    #
                    for l in line:
                        syslog.syslog(syslog.LOG_LOCAL2, l)
                
                if self.done:
                    break
