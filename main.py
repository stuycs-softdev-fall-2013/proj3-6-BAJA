#! /usr/bin/env python

from sites.qmail import app as qmail
from sites.school import app as school
from sites.wife import app as wife
from sites.bank import app as bank

SITES = {
    (qmail, 6680),
    # (school, 6673),
    # (wife, 6691),
    # (bank, 6603)
}

def main(debug=False):
    for package, port in SITES:
        app = getattr(package, "app")
        app.run(host="0.0.0.0", port=port, debug=debug)

if __name__ == "__main__":
    main(debug=True)
