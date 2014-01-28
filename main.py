#! /usr/bin/env python

from game.utils import get_port
from sites.qmail import app as qmail
from sites.school import app as school
from sites.wife import app as wife
from sites.bank import app as bank

SITES = {
    (qmail, get_port("qmail")),
    # (school, get_port("school")),
    # (wife, get_port("wife")),
    # (bank, get_port("bank"))
}

def main(debug=False):
    for package, port in SITES:
        app = getattr(package, "app")
        app.run(host="0.0.0.0", port=port, debug=debug)

if __name__ == "__main__":
    main(debug=True)
