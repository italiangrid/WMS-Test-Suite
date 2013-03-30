#
# Bug: 97319
# Title: Set asyncjobstart=false to avoid lost jobs
# Link: https://savannah.cern.ch/bugs/?97319
#
#


from lib.Exceptions import *


def run(utils):

    bug='97319'

    utils.log_info("Start regression test for bug %s"%(bug))
  
    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())
  
    utils.log_info("Check wms configuration file for asyncjobstart option")
 
    output=utils.execute_remote_cmd(ssh,"grep -i asyncjobstart /etc/glite-wms/glite_wms.conf")

    utils.close_ssh(ssh)

    output=output.strip(" \n\t;")

    value=output.split("=")[1]

    if value.find("false")==-1:
        utils.log_info("ERROR: asyncjobstart option hasn't value 'false' as expected")
        raise GeneralError("Check asyncjobstart option at wms configuration file","asyncjobstart option hasn't value 'false' as expected")
    else:
        utils.log_info("asyncjobstart options has value 'false' as expected")

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))

