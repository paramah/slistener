#!/usr/bin/python

import sys
import os
import logging
import subprocess
import time


from supervisor.childutils import listener


def main(args):
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(filename)s: %(message)s')
    logger = logging.getLogger("supervisord-eventlistener")
    debug_mode = True if 'DEBUG' in os.environ else False
    
    if 'PROCESSNAME' in os.environ:
        processName = os.environ["PROCESSNAME"]
    else: 
        logger.critical("Set PROCESSNAME in environment!");
        exit(1)

    if 'EVENT' in os.environ:
        eventName = os.environ["EVENT"]
    else:
        logger.critical("Set EVENT in environment!")
        exit(1)

    if 'EXECUTE' in os.environ:
        executeCommand = os.environ["EXECUTE"].split(" ")
    else:
        logger.critical("Set EXECUTE in environment!")
        exit(1)

    if 'DELAY' in os.environ:
        sleepTime = int(os.environ["DELAY"])
    else:
        logger.critical("Set DELAY in environment!")
        exit(1)

    while True:
        headers, body = listener.wait(sys.stdin, sys.stdout)
        body = dict([pair.split(":") for pair in body.split(" ")])

        if debug_mode: 
            logger.debug("ENV: %r", repr(os.environ))
            logger.debug("Headers: %r", repr(headers))
            logger.debug("Body: %r", repr(body))
            logger.debug("Args: %r", repr(args))

        try:
            if headers["eventname"] == eventName and body["processname"] == processName:
                if debug_mode:
                    logger.debug("Process %s entered RUNNING state...", processName)
                time.sleep(sleepTime); 
                if debug_mode:
                    logger.debug("Execute %s after %s (sec)...", os.environ["EXECUTE"], os.environ["DELAY"])
                res = subprocess.call(executeCommand, stdout=sys.stderr)
        except Exception as e:
            logger.critical("Unexpected Exception: %s", str(e))
            listener.fail(sys.stdout)
            exit(1)
        else:
            listener.ok(sys.stdout)

if __name__ == '__main__':
    main(sys.argv[1:])
