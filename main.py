#! /usr/bin/env python

import os

import gunicorn
from gunicorn.app.wsgiapp import WSGIApplication

from game.utils import get_port
from sites.qmail import app as qmail
from sites.school import app as school
from sites.wife import app as wife
from sites.bank import app as bank

SITES = {
    ("qmail", qmail, get_port("qmail")),
    ("school", school, get_port("school")),
    # ("wife", wife, get_port("wife")),
    # ("bank", bank, get_port("bank"))
}

def daemonize(func):
    if not os.fork():
        os.setsid()
        os.closerange(0, 3)
        fd_null = os.open(os.devnull, os.O_RDWR)
        if fd_null != 0:
            os.dup2(fd_null, 0)
        os.dup2(fd_null, 1)
        os.dup2(fd_null, 2)
        func()

def main():
    if [fn for fn in os.listdir("run") if fn.endswith(".pid")]:
        print "-> Killing old Gunicorn processes"
        os.system("cat run/*.pid | xargs kill")
    template = "-> Started Gunicorn {0} for {1} on {2} (http://localhost:{2})."
    for name, mod, port in SITES:
        class Application(WSGIApplication):
            def init(self, parser, opts, args):
                self.cfg.set("bind", ["0.0.0.0:" + str(port)])
                self.cfg.set("daemon", True)
                self.cfg.set("workers", 4)
                self.cfg.set("loglevel", "info")
                self.cfg.set("proc_name", "gunicorn-" + name)
                self.cfg.set("pidfile", "run/" + name + ".pid")
                self.cfg.set("errorlog", "run/" + name + ".error.log")
            def load_wsgiapp(self):
                self.chdir()
                return getattr(mod, "app")
        daemonize(Application().run)
        print template.format(gunicorn.__version__, name, port)
    print "Stop all with: `cat run/*.pid | xargs kill`"

if __name__ == "__main__":
    main()
