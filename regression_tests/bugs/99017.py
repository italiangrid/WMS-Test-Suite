#
# Bug: 99017
# Title: wmproxy init script 'status' does not return error when service is not running
# Link: https://savannah.cern.ch/bugs/?99017
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='99017'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())
  
    logging.info("Stop wmproxy service")
 
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy stop")

    logging.info("Check status of wmproxy service")

    output=utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy status")

    if output.find("is not running")==-1:
        utils.close_ssh(ssh)
        logging.error("wmproxy service is not stopped as expected")
        raise GeneralError("Check status of wmproxy service","wmproxy service is not stopped as expected")
    else:
        logging.info("Wmproxy service is stopped as expected")

    logging.info("Check return value of wmproxy init script")

    return_value=utils.execute_remote_cmd(ssh,"echo $?").strip(" \t\n")

    utils.close_ssh(ssh)

    if int(return_value)==1:
        logging.info("Return value of wmproxy init script is 1 as expected")
    else:
        logging.error("Return value of wmproxy init script is %s instead of 1 as expected"%(return_value))
        raise GeneralError("Check return value of wmproxy init script","Return value of wmproxy init script is %s instead of 1 as expected"%(return_value))

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))

