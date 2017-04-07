#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import getopt

from Ump import controller
from daemon import Daemon

class ServerDaemon(Daemon):
    def __init__(self, port=27000):
        self.port = int(port)
        self.pidfile = '/var/run/tsst_server.pid'
        self.name = 'tsst_server'
        self.prog_name = 'tsst_server'
        super(ServerDaemon, self).__init__(self.pidfile, name=self.name, prog_name=self.prog_name, port=self.port)

    def run(self):
        controller.main(self.port)

    def test(self):
        controller.main(self.port, is_log=False)


def usage():
    print ("usage:")
    name = 'ump-controller-server'
    print (name + " --start")
    print (name + " --stop")
    print (name + " --status")
    print (name + " --test")
    print (name)
    exit(1)


def main():
    op = ''
    ext = None
    try:
        opts, args = getopt.getopt(
                sys.argv[1:],
            'h', ['start', 'stop', 'help', 'test','status']
                )
        if not opts:
            usage()
    except getopt.GetoptError, err:
        usage()

    server_daemon = ServerDaemon()
    for o, a in opts:
        if o in ('--help'):
            usage()
            exit(0)
        elif (o == '--start'):
            op = o
            server_daemon.start()
            print ('%s is running' % (controller_daemon.name))
        elif (o == '--stop'):
            op = o
            res = controller_daemon.stop()
            if res:
                print ('%s is stopped' % (controller_daemon.name))
        elif (o == '--test'):
            controller_daemon.test()
        elif (o == '--status'):
            is_run,pid = controller_daemon.status()
            if is_run:
                print ('%s is running, pid is %s' %(controller_daemon.name, pid))
            else:
                print ('%s is stopped' % (controller_daemon.name))
        else:
            assert False, 'oops, unhandled option: %s, -h for help' % o
            exit(1)


if __name__ == '__main__':
    if (len(sys.argv) == 1):
        usage()
    else:
        main()
