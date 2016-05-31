#!/usr/bin/env python3

import sys
import os
import runpy
import logging
import argparse

from sikuli import *

logging.captureWarnings(True)
logging.getLogger("sikuli").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("easyprocess").setLevel(logging.WARNING)
logging.getLogger("pyscreenshot").setLevel(logging.WARNING)


try:
    import pydevd
    import signal

    def handle_hup(signum, frame):
        pydevd.settrace(
            'localhost',
            port=1444,
            stdoutToServer=True,
            stderrToServer=True
        )
    signal.signal(signal.SIGHUP, handle_hup)
except ImportError:
    pass


def reload(module):
    logging.debug("Stub reload(%r)" % module)


def run(folder):
    folder = os.path.abspath(folder)
    module = os.path.basename(folder).replace(".sikuli", "")
    #print("Running %s from %s" % (module, folder))
    sys.path.append(folder)
    sys.path.append(os.path.dirname(folder))  # FIXME: adding parent is unofficial
    Settings.ImagePaths.append(folder)
    try:
        runpy._run_module_as_main(module)
        # mod = __import__(module)
    except KeyboardInterrupt:
        pass


def main():
    # FIXME: sikuli CLI compat
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', default=False, action='store_true')
    parser.add_argument('-s', '--scale', type=float, default=1.0)
    parser.add_argument('script')
    args = parser.parse_args()
    if args.debug:
        logging.getLogger("sikuli").setLevel(logging.DEBUG)
    Settings.Scale = args.scale
    run(args.script)
    return 0


if __name__ == "__main__":
    sys.exit(main())
