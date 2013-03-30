#
# Bug:35250
# Title: DAG: glite_wms_wmproxy_dirmanager does not extract links from tar.gz
# Link: https://savannah.cern.ch/bugs/?35250
#
#

from lib.Exceptions import *
from lib import Job_utils


def run(utils):

    bug='35250'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Submit the job and wait to finish")

    utils.use_external_jdl("%s.jdl"%(bug))

    utils.set_destination_ce(utils.get_jdl_file(),"2119/jobmanager")

    JOBID=Job_utils.submit_wait_finish(utils)

    utils.log_info("Check job's final status")

    utils.job_status(JOBID)

    if utils.JOBSTATUS.find('Done (Success)') == -1 :
        utils.log_info("ERROR: Job not finished successfully. Job final status is '%s' instead of 'Done (Success)'"%(utils.get_job_status()))
        raise GeneralError("Check job final status","Job not finished successfully. Job final status is '%s' instead of 'Done (Success)'"%(utils.get_job_status()))
    else:
         utils.log_info("Job finished successfully.")

    utils.log_info("TEST OK")
    
    utils.log_info("End of regression test for bug %s"%(bug))
