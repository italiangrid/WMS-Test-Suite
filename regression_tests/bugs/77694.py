#
# Bug:77694
# Title: Resource BDII for WMS needs to be revisit
# Link: https://savannah.cern.ch/bugs/?77694
#
#


import logging

from libutils.Exceptions import *

def run(utils):

    bug='77694'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    file="/opt/glite/yaim/node-info.d/glite-wms"

    logging.info("Get file %s from remote host"%(file))

    utils.ssh_get_file(ssh,file,"%s/glite_wms_local"%(utils.get_tmp_dir()))

    logging.info("Check if function config_gip_only has been removed from node-info.d/glite-wms")

    F=open("%s/glite_wms_local"%(utils.get_tmp_dir()))
    lines=F.readlines()
    F.close()

    for line in lines:

      if line.find("config_gip_only")!=-1:
        logging.error("Test failed: function config_gip_only has not been removed as expected from node-info.d/glite-wms")
        raise GeneralError("Check for function config_gip_only at node-info.d/glite-wms","Error !!! Function config_gip_only has not been removed as expected from node-info.d/glite-wms")


    ssh.close()
    
    logging.info("End of regression test for bug %s",bug)
