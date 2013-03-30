#
# Bug:91078
# Title: ICE log verbosity should be reduced to 300
# Link: https://savannah.cern.ch/bugs/?91078
#
#

from lib.Exceptions import *


def run(utils):

    bug='91078'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Search glite_wms.conf for ice_log_level value")

    ice_log_level=utils.execute_remote_cmd(ssh, "grep ice_log_level /etc/glite-wms/glite_wms.conf")

    ice_log_level=ice_log_level.split("=")[1].strip(" \t\n;")

    utils.close_ssh(ssh)

    utils.log_info("Check ice_log_level value")

    if ice_log_level=='300':
        utils.log_info("Log verbosity is 300 as expected")
    else:
        utils.log_info("ERROR: Test failed, ICE log verbosity is not 300 as expected but %s"%(ice_log_level))
        raise GeneralError("Check ICE log verbosity","Test failed, ICE log verbosity is not 300 as expected but %s"%(ice_log_level))

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))
