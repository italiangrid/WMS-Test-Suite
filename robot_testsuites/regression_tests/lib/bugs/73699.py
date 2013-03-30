#
# Bug:73699
# Title: Wrong retry count computation
# Link: https://savannah.cern.ch/bugs/?73699
#
#


from lib.Exceptions import *
from lib import Job_utils

def run(utils):

    bug='73699'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.use_external_jdl("%s.jdl"%(bug))

    JOBID=Job_utils.submit_wait_finish(utils,"")

    # Check for job status

    utils.log_info("Check job stauts")

    utils.job_status(JOBID)

    if utils.get_job_status()=="Aborted":
        utils.log_info("Job status is Aborted")
    else:
      utils.log_info("ERROR: Job status is not Aborted")
      raise GeneralError("Check job status","Job status is not 'Aborted' but %s"%(utils.get_job_status()))

    # Check the aborted reason
    
    reason=utils.get_StatusReason(JOBID)

    if reason != "hit job retry count (3)":
        utils.log_info("ERROR: Wrong reason: %s"%(reason))
        raise GeneralError("Check aborted reason","Wrong reason: %s"%(reason))
    else:
        utils.log_info("Retry count is 3 as expected")  

    # Check the number of resubmission events

    utils.log_info("Check the number of resubmission events")

    result=utils.run_command("glite-wms-job-logging-info -v 2 --event Resubmission  %s"%(JOBID)).count("WILLRESUB")

    if result == 7 :
        utils.log_info("Test PASS")
    else:
      utils.log_info("ERROR: Wrong number of resubmission events. Get %s expected 7"%(result))
      raise GeneralError("Check resubmission events","Wrong number of resubmission events. Get %s expected 7"%(result))
   
    utils.log_info("End of regression test for bug %s"%(bug))
