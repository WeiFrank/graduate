import  subprocess
import  signal
import  time
import  os
import  errno
def _exec_pipe(cmd, retry = 3, p = False, timeout = 0, is_raise=False):
    env = {"LANG" : "en_US", "LC_ALL" : "en_US", "PATH" : os.getenv("PATH")}
    #cmd = self.lich_inspect + " --movechunk '%s' %s  --async" % (k, loc)
    _retry = 0
    cmd1 = ''
    for i in cmd:
        cmd1 = cmd1 + i + ' '
    if (p):
        LOG.info(cmd1)
    while (1):
        p = None
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env = env)
        except Exception, e:
            raise Exception(e)

        if timeout != 0:
            signal.signal(signal.SIGALRM, alarm_handler)
            signal.alarm(timeout)
        try:
            stdout, stderr = p.communicate()
            signal.alarm(0)
            ret = p.returncode
            if (ret == 0):
                return ret, stdout, stderr
            elif (ret == errno.EAGAIN and _retry < retry):
                _retry = _retry + 1
                time.sleep(1)
                continue
            else:
                if is_raise:
                    raise Exception(stderr)
                return ret, stdout, stderr

        except KeyboardInterrupt as err:
            p.kill()
            raise Exception(err)
