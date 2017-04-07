#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import time
import atexit
import fcntl
import errno
import socket

from signal import SIGTERM

from Umpweb.common import log

LOG = log.get_log('entry.daemon')


def _lock_file(key, is_exp):
    key = os.path.abspath(key)
    parent = os.path.split(key)[0]
    os.system("mkdir -p " + parent)

    lock_fd = open(key, 'a')

    try:
        fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError as err:
        if is_exp:
            raise
        elif err.errno == errno.EAGAIN:
            #            sys.stderr.write("lock %s failed: %d (%s)\n" % (key, err.errno, err.strerror))
            raise
        # exit(err.errno)
        else:
            raise
    lock_fd.truncate(0)
    return lock_fd


def _try_lock_file(key):
    key = os.path.abspath(key)
    if not os.path.exists(key):
        raise Exp(errno.EPERM, key + ' not exist')

    lock_fd = open(key, 'a')

    fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)


def error_tip(tip):
    return "\033[1;31m%s\033[0m" % (tip)


def success_tip(tip):
    return "\033[1;32m%s\033[0m" % (tip)


class Daemon(object):
    def __init__(self, pidfile, name='noname', prog_name=None, port=None,
                 stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.name = name
        self.prog_name = prog_name
        self.port = port

    def _daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                # 退出父进程
                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)

        os.chdir("/")
        os.setsid()
        os.umask(0)

        # 创建子进程
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)

        # 重定向文件描述符
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        atexit.register(self.delpid)
        # 创建processid文件
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write('%s\n' % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self, is_exp=False):
        pid = self.get_pid()

        try:
            pid = _lock_file(self.pidfile, is_exp)
        except Exception, err:
            if err.errno == errno.EAGAIN:
                msg = '%s is already running, pid is %s\n' % (self.name, pid)
                sys.stderr.write(msg)
                exit(err.errno)

        # Start the daemon
        print 'start %s' % (self.name)
        self.check_port()

        self._daemonize()
        self.run()

    #        sys.stdout.write("%s is running"%self.name)

    def check_port(self):
        '''check the socket port is in use
        '''
        if not self.port:
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', self.port))
        if result == 0:
            err = error_tip('start %s failed, port %s is already in use\n' % (self.name, self.port))
            sys.stderr.write(err)
            sys.exit(1)
        return

    def get_pid(self):
        try:
            pf = file(self.pidfile, 'r')
            pid = pf.read().strip()
            pid = pid and pid.isdigit() and int(pid)
            pf.close()
        except IOError:
            pid = None
            pass
        return pid

    def stop(self, is_exp=False):
        """Stop the daemon
        :param is_exp: when progress except raise an exception if True
        :return whether execute kill progress with pid file
        """
        # Get the pid from the pidfile
        pid = self.get_pid()

        action_stop = False
        if not pid:
            if is_exp:
                raise Exp(errno.ENOINT, 'daemon not running')
            message = "%s is already stopped\n" % (self.name)
            sys.stderr.write(message)
        else:
            # Try killing the daemon process
            try:
                while 1:
                    os.kill(pid, SIGTERM)
                    time.sleep(0.1)
                action_stop = True
            except OSError, err:
                err = str(err)
                if err.find("No such process") > 0:
                    if os.path.exists(self.pidfile):
                        os.remove(self.pidfile)
                else:
                    sys.stderr.write(err)
                    sys.exit(1)
        self.ensure_stop()
        return action_stop

    def ensure_stop(self):
        if self.prog_name:
            os.popen("kill -9 `lsof -i:27000|grep -v PID|awk '{print $2}'` 2>&1 >/dev/null")
            #            kill_cmd = "kill -9 `ps -ef|grep %s|grep -v stop|grep Ump|awk '{ print $2 }'` 2>&1 >/dev/null" % (self.prog_name)
            #            stdout = os.popen(kill_cmd).read()

    def status(self):
        """
           Status of the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        if not os.path.exists(self.pidfile):
            return False, -1

        pid = self.get_pid()
        try:
            _try_lock_file(self.pidfile)
        except Exception, e:
            return True, pid

        return False, -1

    def restart(self):
        self.stop()
        self.start()

    def run(self):
        """
            You should override this method when you subclass Daemon. It will be called after the process has been
            daemonized by start() or restart().
        """


if __name__ == '__main__':
    pass
