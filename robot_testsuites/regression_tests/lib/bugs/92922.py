#
# Bug:92922
# Title: EMI-1 WMS does not propagate user job exit code
# Link: https://savannah.cern.ch/bugs/?92922
#
#

from lib.Exceptions import *
from lib import Job_utils

def run(utils):

    bug='92922'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Prepare jdl file for submission")

    utils.use_external_jdl("%s.jdl"%(bug))

    JOBID=Job_utils.submit_wait_finish(utils)

    utils.log_info("Check job's exit code")
    
    output=utils.run_command("glite-wms-job-status %s"%(JOBID))
 
    exit_code=''
    status=''
    
    for line in output.split("\n"):

        if line.find("Exit code:")!=-1:
            exit_code=line.split(":")[1].strip(" \t\n")

        if line.find("Current Status:")!=-1:
            status=line.split(":")[1].strip(" \t\n")

    if status.find("Done(Exit Code !=0)")==-1:
        utils.log_info("ERROR: Wrong final status. Get %s, while expected 'Done(Exit Code !=0)'"%(status))
        raise GeneralError("Check job's final status","Wrong final status. Get %s , while expected 'Done(Exit Code !=0)'"%(status))
    else:
        utils.log_info("Job's final status is 'Done(Exit Code !=0)' as expected")

    if int(exit_code)==0:
        utils.log_info("ERROR: Wrong exit code. Found 0 , while expected != 0")
        raise GeneralError("Check job's exit code","Wrong exit code. Found 0, while expected != 0")
    else:
        utils.log_info("Job's exit code is not 0 as expected")

    utils.log_info("End of regression test for bug %s"%(bug))

