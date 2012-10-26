#
# Bug: 61315
# Title: [ yaim-wms ] CeForwardParameters should include several more parameters
# Link: https://savannah.cern.ch/bugs/?61315
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='61315'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    parameters=[
        'GlueHostMainMemoryVirtualSize',
        'GlueHostMainMemoryRAMSize',
        'GlueCEPolicyMaxCPUTime',
        'GlueCEPolicyMaxWallClockTime',
        'GlueCEPolicyMaxObtainableWallClockTime',
        'GlueCEPolicyMaxObtainableCPUTime'
    ]

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.ssh_get_file(ssh,"/etc/glite-wms/glite_wms.conf","%s/local"%(utils.get_tmp_dir()))

    utils.close_ssh(ssh)
    
    FILE=open("%s/local"%(utils.get_tmp_dir()))
    lines=FILE.readlines()
    FILE.close()

    logging.info("Check if CeForwardParameters variable at glite_wms.conf contains several more parameters")

    for line in lines:
        if line.find("CeForwardParameters")!=-1:
          CeForward=line
          break

    conf_params=CeForward.split("=")[1].strip(" \t\n{};").replace("\"","").split(",")

    for con in conf_params:
       conf_params[conf_params.index(con)]=con.strip(" \t\n")


    common=set(conf_params)&set(parameters)

    diff=set(parameters)-set(conf_params)

    if len(common)!=len(parameters):
        logging.error("Test failed, not all required parameters found in CeForwardParameters variable at glite_wms.conf")
        logging.error("Available parameters: %s "%(' , '.join(common)))
        logging.error("Missing parameters: %s"%(' , '.join(diff)))
        raise GeneralError("Check CeForwardParameters variable at glite_wms.conf","Test failed, not all required parameters found in CeForwardParameters variable at glite_wms.conf")
    
    
    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))

