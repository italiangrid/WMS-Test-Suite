#
# Bug:90129
# Title: yaim-wms creates wms.proxy in wrong path
# Link: https://savannah.cern.ch/bugs/?90129
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='90129'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Check that ${WMS_LOCATION_VAR}/glite directory contains wms.proxy file as expected")

    utils.execute_remote_cmd(ssh,"ls -l ${WMS_LOCATION_VAR}/glite/wms.proxy")

    logging.info("Check ok , find wms.proxy file at ${WMS_LOCATION_VAR}/glite")

    logging.info("Check ${WMS_LOCATION_VAR} for wms.proxy file")

    out=utils.execute_remote_cmd_fail(ssh,"ls -l ${WMS_LOCATION_VAR}/wms.proxy")

    utils.close_ssh(ssh)

    if out.find("wms.proxy: No such file or directory")!=-1:
        logging.info("Not find wms.proxy file at ${WMS_LOCATION_VAR} as expected")
    else:
        logging.error("Test failed, find wms.proxy file at ${WMS_LOCATION_VAR} directory")
        raise GeneralError("Check ${WMS_LOCATION_VAR} for wms.proxy file","Test failed, find wms.proxy file at ${WMS_LOCATION_VAR} directory")

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
