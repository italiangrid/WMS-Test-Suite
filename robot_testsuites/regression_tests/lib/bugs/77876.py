#
# Bug:77876
# Title: While purging DAGs/Collections the CLEAR event is only logged for the parent node
# Link: https://savannah.cern.ch/bugs/?77876
#
#

import commands

from lib.Exceptions import *
from lib import Job_utils


def run(utils):

    bug='77876'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Submit job collection")

    utils.use_utils_jdl()

    Job_utils.prepare_collection_job(utils,utils.get_jdl_file(),"")
    
    JOBID=Job_utils.submit_collection_wait_finish(utils,"")

    utils.job_status(JOBID)
    
    if utils.get_job_status().find('Done') != -1 :
    
        utils.log_info("Get job output")

        # Get output
        utils.run_command("glite-wms-job-output --noint --dir %s %s "%(utils.get_job_output_dir(),JOBID))

        utils.log_info("Check job status")

        res=utils.run_command("glite-wms-job-status -v 0 %s"%(JOBID))

        num=res.count("Current Status:     Cleared")

        if num == 4 :
            utils.log_info("All nodes have CLEARED status")
        else:
            utils.log_info("ERROR: Not all nodes have CLEARED status. Get %s expected 4"%(num))
            raise GeneralError("Count Cleared status","Not all nodes have CLEARED status. Get %s expected 4"%(num))
        
    else:
        utils.log_info("ERROR: Job not finished successfully. Retry the test.")
        raise RetryError("Check job final status","Job not finished successfully.")

   
    utils.log_info("End of regression test for bug %s"%(bug))

