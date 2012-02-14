#! /usr/bin/python

import sys
import signal
import logging

from libutils import Regression_utils


def main():


    utils = Regression_utils.Regression_utils(sys.argv[0])

    utils.prepare(sys.argv[1:])

    logging.info("Execute regression tests for WMS component ")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    tests=utils.load_tests()

    for test in tests:

      utils.show_progress("Testing bug %s"%(test))
      logging.info("Testing bug %s"%(test))

      utils.execute_test(test)

 
    if utils.get_fails_number() > 0 :
      utils.exit_failure("%i test(s) failed: %s "%(utils.get_fails_number(), utils.get_fails_test()))
    else:
      utils.exit_success()

    

if __name__ == "__main__":
    main()
