#
# Bug:91484
# Title: move lcmaps.log from /var/log/glite to WMS_LOCATION_LOG
# Link: https://savannah.cern.ch/bugs/?91484
#
#

from lib.Exceptions import *

def run(utils):

    bug='91484'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Check that ${WMS_LOCATION_LOG} directory contains lcmaps.log file as expected")

    utils.execute_remote_cmd(ssh,"ls -l ${WMS_LOCATION_LOG}/lcmaps.log")

    utils.log_info("Check ok , find lcmaps.log file at ${WMS_LOCATION_LOG}")

    utils.log_info("Check /var/log/glite for lcmaps.log file")

    out=utils.execute_remote_cmd_fail(ssh,"ls -l /var/log/glite/lcmaps.log")

    utils.close_ssh(ssh)

    if out.find("lcmaps.proxy: No such file or directory")!=-1:
        utils.log_info("Not find lcmaps.log file at /var/log/glite as expected")
    else:
        utils.log_info("ERROR: Test failed, find lcmaps.log file at directory /var/log/glite")
        raise GeneralError("Check /var/log/glite for lcmaps.log file","Test failed, find lcmaps.log file at directory /var/log/glite")

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))
