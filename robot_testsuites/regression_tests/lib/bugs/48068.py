#
# Bug: 48068
# Title: [wms] GlueServiceStatusInfo content is ugly
# Link: https://savannah.cern.ch/bugs/?48068
#
#


from lib.Exceptions import *


def run(utils):

    bug='48068'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    messages=[
        '/usr/bin/glite_wms_wmproxy_server is running...',
        '/usr/bin/glite_wms_wmproxy_server is not running'
    ]

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Check command's /etc/init.d/glite-wms-wmproxy status output")

    output=utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy status").strip(" \n\t")

    utils.close_ssh(ssh)
    
    find=0

    for message in messages:
        
        if output==message :
            find=1
            break

    if find==1:
        utils.log_info("Check OK, command's output was as expected")
    else:
        utils.log_info("ERROR: Test failed, command's output wasn't as expected")
        utils.log_info("ERROR: Output: %s"%(output))
        raise GeneralError("Check command's /etc/init.d/glite-wms-wmproxy status output","Test failed, command's output wasn't as expected")

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))
