#!/usr/bin/env python
 
import os
import sys
import yaml

#
# ignore warnings
#
import warnings
warnings.filterwarnings("ignore")

from daemon import Daemon
from tail import TailThread

class MyDaemon(Daemon):
    
    def run(self, debug=False):
        if os.path.exists("/etc/taillogger.yml"):
            f = open('/etc/taillogger.yml')
        elif os.path.exists("./taillogger.yml"):
            f = open('./taillogger.yml')
        else:
            print "Cannot find the config file at /etc/taillogger.yml"
            sys.exit()
        
        data = yaml.load(f)
        f.close()

        for log,opts in data['logs'].items():
            #
            # launch off a new tail client
            #
            thread = TailThread(log, opts)
            thread.start()


def main():
    daemon = MyDaemon('/var/run/taillogger.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'debug' == sys.argv[1]:
            daemon.run(debug = True)
        elif 'setup' == sys.argv[1]:
            setup()
        elif 'status' == sys.argv[1]:
            print
            print "need to do this"
            print
        else:
            print "Unknown command"
            sys.exit(2)
        
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart|status|debug" % sys.argv[0]
        sys.exit(2)
        
#
# should never get called
#
if __name__ == "__main__":
    main()
