#
# Bug: 48068
# Title: [wms] GlueServiceStatusInfo content is ugly
# Link: https://savannah.cern.ch/bugs/?48068
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='48068'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    messages=[
        '/usr/bin/glite_wms_wmproxy_server is running...',
        '/usr/bin/glite_wms_wmproxy_server is not running'
    ]

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Check command's /etc/init.d/glite-wms-wmproxy status output")

    output=utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy status").strip(" \n\t")

    utils.close_ssh(ssh)
    
    find=0

    for message in messages:
        
        if output==message :
            find=1
            break

    if find==1:
        logging.info("Check OK, command's output was as expected")
    else:
        logging.error("Test failed, command's output wasn't as expected")
        logging.error("Output: %s"%(output))
        raise GeneralError("Check command's /etc/init.d/glite-wms-wmproxy status output","Test failed, command's output wasn't as expected")

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
