#
# Bug:   83062
# Title: [yaim-wms] A different template should be used for glue2 publication
# Link:  https://savannah.cern.ch/bugs/?83062
#
#

import os

from lib.Exceptions import *

def run(utils):

    bug='83062'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Query the resource BDII on the WMS for Glue2 format")

    glue2=utils.run_command("ldapsearch -x -h %s -p 2170 -b \"o=glue\""%(utils.get_WMS())).split("\n")

    utils.log_info("Check the result status of publication")

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
       utils.log_info("ERROR: Result for publication in glue2 format is not '0 Success'")
       raise GeneralError("Error","Result for publication in glue2 format is not '0 Success'")
    else:
       utils.log_info("Check ok , result for publication in glue2 format is '0 Success'")

    if glue2service==0:
       utils.log_info("ERROR: Didn't find a GLUE2ServiceType objectclass with 'GLUE2ServiceType: org.glite.wms.WMProxy'")
       raise GeneralError("Error","Didn't find a GLUE2ServiceType objectclass with 'GLUE2ServiceType: org.glite.wms.WMProxy'")
    else:
       utils.log_info("Check ok, find a GLUE2ServiceType objectclass with 'GLUE2ServiceType: org.glite.wms.WMProxy'")

    if glue2endpoint==0:
       utils.log_info("ERROR: Didn't find a GLUE2Endpoint objectclass with 'GLUE2EndpointInterfaceName: org.glite.wms.WMProxy'")
       raise GeneralError("Error","Didn't find a GLUE2Endpoint objectclass with 'GLUE2EndpointInterfaceName: org.glite.wms.WMProxy'")
    else:
       utils.log_info("Check ok, find a GLUE2Endpoint objectclass with 'GLUE2EndpointInterfaceName: org.glite.wms.WMProxy'")

    utils.log_info("Prepare directory to checkout GLUE Validator")

    os.makedirs("%s/trunk"%(utils.get_tmp_dir()))

    utils.log_info("Checkout GLUE Validator")

    utils.run_command("svn co http://svnweb.cern.ch/guest/gridinfo/glue-validator/trunk %s/trunk"%(utils.get_tmp_dir()))

    utils.log_info("Execute GLUE Validator")

    os.putenv("PYTHONPATH","%s/trunk/lib"%(utils.get_tmp_dir()))

    utils.run_command("%s/trunk/bin/glue-validator -t glue2 -b \"o=glue\" -h %s -p 2170"%(utils.get_tmp_dir(),utils.get_WMS()))

    utils.log_info("Test OK")

    utils.log_info("End of regression test for bug %s"%(bug))
