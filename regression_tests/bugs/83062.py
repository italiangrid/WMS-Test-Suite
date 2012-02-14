#
# Bug:   83062
# Title: [yaim-wms] A different template should be used for glue2 publication
# Link:  https://savannah.cern.ch/bugs/?83062
#
#

import logging
import os

from libutils.Exceptions import *

def run(utils):

    bug='83062'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Query the resource BDII on the WMS for Glue2 format")

    glue2=utils.run_command_continue_on_error("ldapsearch -x -h %s -p 2170 -b \"o=glue\""%(utils.get_WMS())).split("\n")

    logging.info("Check the result status of publication")

    status=0
    glue2service=0
    glue2endpoint=0
    
    for line in glue2:

        if line.find("result: ")!=-1:
           if line.split("result: ")[1].find("0 Success")!=-1:
              status=1

        if line.find("GLUE2ServiceType: ")!=-1:
           if line.split("GLUE2ServiceType: ")[1].find("org.glite.wms.WMProxy")!=-1:
              glue2service=1

        if line.find("GLUE2EndpointInterfaceName: ")!=-1:
           if line.split("GLUE2EndpointInterfaceName: ")[1].find("org.glite.wms.WMProxy")!=-1:
              glue2endpoint=1

    if status==0:
       logging.error("Error , Result for publication in glue2 format is not '0 Success'")
       raise GeneralError("Error","Result for publication in glue2 format is not '0 Success'")
    else:
       logging.info("Check ok , result for publication in glue2 format is '0 Success'")

    if glue2service==0:
       logging.error("Error , Didn't find a GLUE2ServiceType objectclass with 'GLUE2ServiceType: org.glite.wms.WMProxy'")
       raise GeneralError("Error","Didn't find a GLUE2ServiceType objectclass with 'GLUE2ServiceType: org.glite.wms.WMProxy'")
    else:
       logging.info("Check ok, find a GLUE2ServiceType objectclass with 'GLUE2ServiceType: org.glite.wms.WMProxy'")

    if glue2endpoint==0:
       logging.error("Error , Didn't find a GLUE2Endpoint objectclass with 'GLUE2EndpointInterfaceName: org.glite.wms.WMProxy'")
       raise GeneralError("Error","Didn't find a GLUE2Endpoint objectclass with 'GLUE2EndpointInterfaceName: org.glite.wms.WMProxy'")
    else:
       logging.info("Check ok, find a GLUE2Endpoint objectclass with 'GLUE2EndpointInterfaceName: org.glite.wms.WMProxy'")

    logging.info("Prepare directory to checkout GLUE Validator")

    os.makedirs("%s/trunk"%(utils.get_tmp_dir()))

    logging.info("Checkout GLUE Validator")

    utils.run_command_continue_on_error("svn co http://svnweb.cern.ch/guest/gridinfo/glue-validator/trunk %s/trunk"%(utils.get_tmp_dir()))

    logging.info("Execute GLUE Validator")

    os.putenv("PYTHONPATH","%s/trunk/lib"%(utils.get_tmp_dir()))

    utils.run_command_continue_on_error("%s/trunk/bin/glue-validator -t glue2 -b \"o=glue\" -h %s -p 2170"%(utils.get_tmp_dir(),utils.get_WMS()))

    logging.info("Test OK")

    logging.info("End of regression test for bug %s"%(bug))
