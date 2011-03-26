from tail import TailThread

import threading
import os
import sys
import yaml

class Poller:
    def __init__(self, debug=False):
        self.config = {}
#        self.debug = debug

        #
        # load up the config
        #
        c = ConfigParser.ConfigParser()
    
        if os.path.exists("/etc/taillogger.yml"):
            c.read("/etc/taillogger.yml")
        else:
            print "Cannot find the config file at /etc/taillogger.yml"
            sys.exit()
    
        
        self.logs = []

        #
        # thread container
        #
        self.threads = []
        
    def runChecks(self, s, firstRun=False):
        for log in self.logs:
            #
            # launch off a new tail client
            #
            thread = TailThread(log)
            thread.start()
            self.threads.append(thread)

    def shutdown(self):
        for thread in self.threads:
            thread.done = True
