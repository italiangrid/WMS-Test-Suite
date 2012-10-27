#
# Bug:91078
# Title: ICE log verbosity should be reduced to 300
# Link: https://savannah.cern.ch/bugs/?91078
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='91078'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Search glite_wms.conf for ice_log_level value")

    ice_log_level=utils.execute_remote_cmd(ssh, "grep ice_log_level /etc/glite-wms/glite_wms.conf")

    ice_log_level=ice_log_level.split("=")[1].strip(" \t\n;")

    utils.close_ssh(ssh)

    logging.info("Check ice_log_level value")

    if ice_log_level=='300':
        logging.info("Log verbosity is 300 as expected")
    else:
        logging.error("Test failed, ICE log verbosity is not 300 as expected but %s"%(ice_log_level))
        raise GeneralError("Check ICE log verbosity","Test failed, ICE log verbosity is not 300 as expected but %s"%(ice_log_level))

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
