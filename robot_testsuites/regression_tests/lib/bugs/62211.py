#
# Bug: 62211
# Title: [ yaim-wms ] Enable Glue 2.0 publishing
# Link: https://savannah.cern.ch/bugs/?62211
#
#

import os

from lib.Exceptions import *

def run(utils):

    bug='62211'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Get the publication in glue1 format")

    glue1=utils.run_command("ldapsearch -x -H ldap://%s:2170 -b mds-vo-name=resource,o=grid"%(utils.get_WMS())).split("\n")

    utils.log_info("Get the publication in glue2 format")

    glue2=utils.run_command("ldapsearch -x -H ldap://%s:2170 -b o=glue"%(utils.get_WMS())).split("\n")

    utils.log_info("Check the result status of each publication")

    ok=0

    for line in glue1:
        if line.find("result: ")!=-1:
           if line.split("result: ")[1].find("0 Success")!=-1:
             ok=1

    if ok==0:
       utils.log_info("ERROR: Result for publication in glue1 format is not '0 Success'")
       raise GeneralError("Error","Result for publication in glue1 format is not '0 Success'")
    else:
       utils.log_info("Check ok , result for publication in glue1 format is '0 Success'")

    ok=0

    for line in glue2:
        if line.find("result: ")!=-1:
           if line.split("result: ")[1].find("0 Success")!=-1:
             ok=1

    if ok==0:
       utils.log_info("ERRO: Result for publication in glue2 format is not '0 Success'")
       raise GeneralError("Error","Result for publication in glue2 format is not '0 Success'")
    else:
       utils.log_info("Check ok , result for publication in glue2 format is '0 Success'")

    utils.log_info("Prepare directory to checkout GLUE Validator")

    os.makedirs("%s/trunk"%(utils.get_tmp_dir()))

    utils.log_info("Checkout GLUE Validator")

    utils.run_command("svn co http://svnweb.cern.ch/guest/gridinfo/glue-validator/trunk %s/trunk"%(utils.get_tmp_dir()))

    utils.log_info("Execute GLUE Validator")

    os.putenv("PYTHONPATH","%s/trunk/lib"%(utils.get_tmp_dir()))

    utils.run_command("%s/trunk/bin/glue-validator -t glue2 -b \"o=glue\" -h %s -p 2170"%(utils.get_tmp_dir(),utils.get_WMS()))

    utils.log_info("Test OK")

    utils.log_info("End of regression test for bug %s"%(bug))
