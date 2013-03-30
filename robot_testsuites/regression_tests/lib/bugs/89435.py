#
# Bug: 89435
# Title: GlueServiceStatusInfo: ??
# Link: https://savannah.cern.ch/bugs/?89435
#
#

from lib.Exceptions import *


def run(utils):

    bug='89435'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    output=utils.execute_remote_cmd(ssh, "/var/lib/bdii/gip/provider/glite-info-provider-service-wmproxy-wrapper")

    utils.close_ssh(ssh)
    
    utils.log_info("Check the GlueServiceStatusInfo parameter")

    status_info=''

    for line in output.split("\n"):
        if line.find("GlueServiceStatusInfo:")!=-1:
            status_info=line
            break

    
    if status_info=='':
       utils.log_info("ERROR: Check /var/lib/bdii/gip/provider/glite-info-provider-service-wmproxy-wrapper output: Unable to find GlueServiceStatusInfo parameter")
       raise GeneralError("Check /var/lib/bdii/gip/provider/glite-info-provider-service-wmproxy-wrapper","Unable to find GlueServiceStatusInfo parameter")


    if status_info.find("GlueServiceStatusInfo: ??")==-1:
         utils.log_info("Check OK. GlueServiceStatusInfo parameter contains: %s"%(status_info.split("GlueServiceStatusInfo:")[1]))
    else:
         utils.log_info("ERROR: Test failed, find GlueServiceStatusInfo: ??")
         raise GeneralError("Check GlueServiceStatusInfo parameter","Test failed, find GlueServiceStatusInfo: ??")
    
    
    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))

