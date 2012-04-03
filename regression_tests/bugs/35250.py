#
# Bug:35250
# Title: DAG: glite_wms_wmproxy_dirmanager does not extract links from tar.gz
# Link: https://savannah.cern.ch/bugs/?35250
#
#

import logging

from libutils.Exceptions import *
from libutils import Job_utils


def run(utils):

    bug='35250'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Submit the job and wait to finish")

    utils.use_external_jdl("%s.jdl"%(bug))

    utils.set_destination_ce(utils.get_jdl_file(),"2119/jobmanager")

    JOBID=Job_utils.submit_wait_finish(utils)

    logging.info("Check job's final status")

    utils.job_status(JOBID)

    if utils.JOBSTATUS.find('Done (Success)') == -1 :
        logging.error("Job not finished successfully. Job final status is '%s' instead of 'Done (Success)'"%(utils.get_job_status()))
        raise GeneralError("Check job final status","Job not finished successfully. Job final status is '%s' instead of 'Done (Success)'"%(utils.get_job_status()))
    else:
         logging.info("Job finished successfully.")


    logging.info("TEST OK")
    
    logging.info("End of regression test for bug %s"%(bug))
