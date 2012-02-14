#
# Bug: 62211
# Title: [ yaim-wms ] Enable Glue 2.0 publishing
# Link: https://savannah.cern.ch/bugs/?62211
#
#

import logging
import os

from libutils.Exceptions import *

def run(utils):

    bug='62211'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Get the publication in glue1 format")

    glue1=utils.run_command_continue_on_error("ldapsearch -x -H ldap://%s:2170 -b mds-vo-name=resource,o=grid"%(utils.get_WMS())).split("\n")

    logging.info("Get the publication in glue2 format")

    glue2=utils.run_command_continue_on_error("ldapsearch -x -H ldap://%s:2170 -b o=glue"%(utils.get_WMS())).split("\n")

    logging.info("Check the result status of each publication")

    ok=0

    for line in glue1:
        if line.find("result: ")!=-1:
           if line.split("result: ")[1].find("0 Success")!=-1:
             ok=1

    if ok==0:
       logging.error("Error , Result for publication in glue1 format is not '0 Success'")
       raise GeneralError("Error","Result for publication in glue1 format is not '0 Success'")
    else:
       logging.info("Check ok , result for publication in glue1 format is '0 Success'")

    ok=0

    for line in glue2:
        if line.find("result: ")!=-1:
           if line.split("result: ")[1].find("0 Success")!=-1:
             ok=1

    if ok==0:
       logging.error("Error , Result for publication in glue2 format is not '0 Success'")
       raise GeneralError("Error","Result for publication in glue2 format is not '0 Success'")
    else:
       logging.info("Check ok , result for publication in glue2 format is '0 Success'")

    logging.info("Prepare directory to checkout GLUE Validator")

    os.makedirs("%s/trunk"%(utils.get_tmp_dir()))

    logging.info("Checkout GLUE Validator")

    utils.run_command_continue_on_error("svn co http://svnweb.cern.ch/guest/gridinfo/glue-validator/trunk %s/trunk"%(utils.get_tmp_dir()))

    logging.info("Execute GLUE Validator")

    os.putenv("PYTHONPATH","%s/trunk/lib"%(utils.get_tmp_dir()))

    utils.run_command_continue_on_error("%s/trunk/bin/glue-validator -t glue2 -b \"o=glue\" -h %s -p 2170"%(utils.get_tmp_dir(),utils.get_WMS()))

    logging.info("Test OK")

    logging.info("End of regression test for bug %s"%(bug))
