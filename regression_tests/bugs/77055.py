#
# Bug:77055
# Title: "MyProxyServer: wrong type caught for attribute" for parametric jobs
# Link: https://savannah.cern.ch/bugs/?77055
#
#

import logging
import re

from libutils.Exceptions import *


def run(utils):

    bug='77055'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Submit a parametric job")

    utils.use_external_jdl("%s.jdl"%(bug))

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

    logging.info("Check if myproxyserver attribute is set in submitted jdl")
    
    result=utils.run_command_continue_on_error("glite-wms-job-info --jdl %s"%(JOBID))
    
    if not re.match("myproxyserver", result, re.I):
        logging.info("Cancel submitted job")
        utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))
        logging.info("Test PASSED")
        
    else:
        logging.error("MyProxyServer has been set in the final submitted jdl")
        raise GeneralError("Check Myproxyserver attribute","MyProxyServer has been set in the final submitted jdl")

    logging.info("End of regression test for bug %s"%(bug))

