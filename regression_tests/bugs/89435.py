#
# Bug: 89435
# Title: GlueServiceStatusInfo: ??
# Link: https://savannah.cern.ch/bugs/?89435
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='89435'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    output=utils.execute_remote_cmd(ssh, "/var/lib/bdii/gip/provider/glite-info-provider-service-wmproxy-wrapper")

    utils.close_ssh(ssh)
    
    logging.info("Check the GlueServiceStatusInfo parameter")

    status_info=''

    for line in output.split("\n"):
        if line.find("GlueServiceStatusInfo:")!=-1:
            status_info=line
            break

    
    if status_info=='':
       logging.error("Check /var/lib/bdii/gip/provider/glite-info-provider-service-wmproxy-wrapper output: Unable to find GlueServiceStatusInfo parameter")
       raise GeneralError("Check /var/lib/bdii/gip/provider/glite-info-provider-service-wmproxy-wrapper","Unable to find GlueServiceStatusInfo parameter")


    if status_info.find("GlueServiceStatusInfo: ??")==-1:
         logging.info("Check OK. GlueServiceStatusInfo parameter contains: %s"%(status_info.split("GlueServiceStatusInfo:")[1]))
    else:
         logging.error("Test failed, find GlueServiceStatusInfo: ??")
         raise GeneralError("Check GlueServiceStatusInfo parameter","Test failed, find GlueServiceStatusInfo: ??")
    
    
    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))

