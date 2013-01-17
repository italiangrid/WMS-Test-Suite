#
# Bug:92922
# Title: EMI-1 WMS does not propagate user job exit code
# Link: https://savannah.cern.ch/bugs/?92922
#
#

import logging

from libutils.Exceptions import *
from libutils import Job_utils

def run(utils):

    bug='92922'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Prepare jdl file for submission")

    utils.use_external_jdl("%s.jdl"%(bug))

    JOBID=Job_utils.submit_wait_finish(utils)

    logging.info("Check job's exit code")
    
    output=utils.run_command_continue_on_error("glite-wms-job-status %s"%(JOBID))
 
    exit_code=''
    status=''
    
    for line in output.split("\n"):

        if line.find("Exit code:")!=-1:
            exit_code=line.split(":")[1].strip(" \t\n")

        if line.find("Current Status:")!=-1:
            status=line.split(":")[1].strip(" \t\n")

    if status.find("Done(Exit Code !=0)")==-1:
        logging.error("Wrong final status. Get %s, while expected 'Done(Exit Code !=0)'"%(status))
        raise GeneralError("Check job's final status","Wrong final status. Get %s , while expected 'Done(Exit Code !=0)'"%(status))
    else:
        logging.info("Job's final status is 'Done(Exit Code !=0)' as expected")

    if int(exit_code)==0:
        logging.error("Wrong exit code. Found 0 , while expected != 0 ")
        raise GeneralError("Check job's exit code","Wrong exit code. Found 0, while expected != 0")
    else:
        logging.info("Job's exit code is not 0 as expected")

    logging.info("End of regression test for bug %s"%(bug))

