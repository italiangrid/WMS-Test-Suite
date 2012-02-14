#
# Bug:73699
# Title: Wrong retry count computation
# Link: https://savannah.cern.ch/bugs/?73699
#
#


import logging

from libutils.Exceptions import *
from libutils import Job_utils

def run(utils):

    bug='73699'

    logging.info("Start regression test for bug %s"%(bug))

    utils.use_external_jdl("%s.jdl"%(bug))

    JOBID=Job_utils.submit_wait_finish(utils,"")

    # Check for job status

    logging.info("Check job stauts")

    utils.job_status(JOBID)


    if utils.get_job_status()=="Aborted":
        logging.info("Job status is Aborted")
    else:
      logging.error("Job status is not Aborted")
      raise GeneralError("Check job status","Job status is not 'Aborted' but %s"%(utils.get_job_status()))


    # Check the aborted reason
    
    reason=utils.get_StatusReason(JOBID)

    if reason != "hit job retry count (3)":
        logging.error("Wrong reason: %s"%(reason))
        raise GeneralError("Check aborted reason","Wrong reason: %s"%(reason))
    else:
        logging.info("Retry count is 3 as expected")  

    # Check the number of resubmission events

    logging.info("Check the number of resubmission events")

    result=utils.run_command_continue_on_error("glite-wms-job-logging-info -v 2 --event Resubmission  %s"%(JOBID)).count("WILLRESUB")

    if result == 7 :
        logging.info("Test PASS")
    else:
      logging.error("Wrong number of resubmission events. Get %s expected 7"%(result))
      raise GeneralError("Check resubmission events","Wrong number of resubmission events. Get %s expected 7"%(result))

   
    logging.info("End of regression test for bug %s",bug)
