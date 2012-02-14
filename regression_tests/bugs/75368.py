#
# Bug:75368
# Title: ICE should log a DONE_FAILED to LB every time the job is going to be resubmitted
# Link: https://savannah.cern.ch/bugs/?75368
#
#


import logging

from libutils.Exceptions import *
from libutils import Job_utils

def run(utils):

    bug='75368'

    CE="this.ce.not.exists:8443/cream-pbs-queue"

    logging.info("Start regression test for bug %s"%(bug))
    
    logging.info("Test requires job submission to a failure Cream CE. Target CE is %s"%(CE))

    utils.use_utils_jdl()
    utils.set_shallow_jdl(utils.get_jdl_file())

    JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg -r %s %s"%(utils.get_delegation_options(),utils.get_config_file(),CE,utils.get_jdl_file()))
    
    utils.wait_until_job_finishes (JOBID)

    utils.job_status(JOBID)

    # Check for Done Failed status

    logging.info("Check for Done Failed job status")

    result=utils.run_command_continue_on_error("glite-wms-job-logging-info -v 2 --event Done %s"%(JOBID))

    if result.count("Status code                =    FAILED") == 3:
        logging.info("Events 'Done Failed' are logged as expected. Test OK")
    else:
        logging.error("Events 'Done Failed' are not logged")
        raise GeneralError("Check Done Failed events","Events 'Done Failed' are not logged")
      
    logging.info("End of regression test for bug %s",bug)
