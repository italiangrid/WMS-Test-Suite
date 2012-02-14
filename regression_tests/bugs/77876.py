#
# Bug:77876
# Title: While purging DAGs/Collections the CLEAR event is only logged for the parent node
# Link: https://savannah.cern.ch/bugs/?77876
#
#

import logging
import commands

from libutils.Exceptions import *
from libutils import Job_utils


def run(utils):

    bug='77876'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Submit job collection")

    utils.use_utils_jdl()

    Job_utils.prepare_collection_job(utils,utils.get_jdl_file(),"")
    
    JOBID=Job_utils.submit_collection_wait_finish(utils,"")

    utils.job_status(JOBID)
    
    if utils.get_job_status().find('Done') != -1 :
    
        logging.info("Get job output")

        # Get output
        utils.run_command_continue_on_error ("glite-wms-job-output --noint --dir %s %s "%(utils.get_job_output_dir(),JOBID))

        logging.info("Check job status")

        res=utils.run_command_continue_on_error("glite-wms-job-status -v 0 %s"%(JOBID))

        num=res.count("Current Status:     Cleared")

        if num == 4 :
            logging.info("All nodes have CLEARED status")
        else:
            logging.error("Not all nodes have CLEARED status. Get %s expected 4"%(num))
            raise GeneralError("Count Cleared status","Not all nodes have CLEARED status. Get %s expected 4"%(num))
        
    else:
        logging.error("Job not finished successfully. Retry the test.")
        raise RetryError("Check job final status","Job not finished successfully.")

   
    logging.info("End of regression test for bug %s"%(bug))

