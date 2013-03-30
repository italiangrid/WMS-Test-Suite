#
# Bug: 99017
# Title: wmproxy init script 'status' does not return error when service is not running
# Link: https://savannah.cern.ch/bugs/?99017
#
#


from lib.Exceptions import *


def run(utils):

    bug='99017'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())
  
    utils.log_info("Stop wmproxy service")
 
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy stop")

    utils.log_info("Check status of wmproxy service")

    output=utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy status")

    if output.find("is not running")==-1:
        utils.close_ssh(ssh)
        utils.log_info("ERROR: wmproxy service is not stopped as expected")
        raise GeneralError("Check status of wmproxy service","wmproxy service is not stopped as expected")
    else:
        utils.log_info("Wmproxy service is stopped as expected")

    utils.log_info("Check return value of wmproxy init script")

    return_value=utils.execute_remote_cmd(ssh,"echo $?").strip(" \t\n")

    utils.close_ssh(ssh)

    if int(return_value)==1:
        utils.log_info("Return value of wmproxy init script is 1 as expected")
    else:
        utils.log_info("ERROR: Return value of wmproxy init script is %s instead of 1 as expected"%(return_value))
        raise GeneralError("Check return value of wmproxy init script","Return value of wmproxy init script is %s instead of 1 as expected"%(return_value))

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))

