#
# Bug:90129
# Title: yaim-wms creates wms.proxy in wrong path
# Link: https://savannah.cern.ch/bugs/?90129
#
#

from lib.Exceptions import *

def run(utils):

    bug='90129'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Check that ${WMS_LOCATION_VAR}/glite directory contains wms.proxy file as expected")

    utils.execute_remote_cmd(ssh,"ls -l ${WMS_LOCATION_VAR}/glite/wms.proxy")

    utils.log_info("Check ok , find wms.proxy file at ${WMS_LOCATION_VAR}/glite")

    utils.log_info("Check ${WMS_LOCATION_VAR} for wms.proxy file")

    out=utils.execute_remote_cmd_fail(ssh,"ls -l ${WMS_LOCATION_VAR}/wms.proxy")

    utils.close_ssh(ssh)

    if out.find("wms.proxy: No such file or directory")!=-1:
        utils.log_info("Not find wms.proxy file at ${WMS_LOCATION_VAR} as expected")
    else:
        utils.log_info("ERROR: Test failed, find wms.proxy file at ${WMS_LOCATION_VAR} directory")
        raise GeneralError("Check ${WMS_LOCATION_VAR} for wms.proxy file","Test failed, find wms.proxy file at ${WMS_LOCATION_VAR} directory")

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))
