#
# Bug:77055
# Title: "MyProxyServer: wrong type caught for attribute" for parametric jobs
# Link: https://savannah.cern.ch/bugs/?77055
#
#

import re

from lib.Exceptions import *


def run(utils):

    bug='77055'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Submit a parametric job")

    utils.use_external_jdl("%s.jdl"%(bug))

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

    utils.log_info("Check if myproxyserver attribute is set in submitted jdl")
    
    result=utils.run_command("glite-wms-job-info --jdl %s"%(JOBID))
    
    if not re.match("myproxyserver", result, re.I):
        utils.log_info("Cancel submitted job")
        utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))
        utils.log_info("Test PASSED")
        
    else:
        utils.log_info("ERROR: MyProxyServer has been set in the final submitted jdl")
        raise GeneralError("Check Myproxyserver attribute","MyProxyServer has been set in the final submitted jdl")

    utils.log_info("End of regression test for bug %s"%(bug))

