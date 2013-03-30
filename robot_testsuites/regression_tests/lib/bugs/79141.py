#
# Bug:79141
# Title: various bugs about parametric jobs
# Link: https://savannah.cern.ch/bugs/?79141
#
#

import os.path

from lib.Exceptions import *
from lib import Job_utils


def run(utils):

    bug='79141'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Submit a parametric job and wait until finish")

    utils.use_external_jdl("%s.jdl"%(bug))
    
    JOBID=Job_utils.submit_wait_finish(utils,"")
    
    jdl=utils.run_command("glite-wms-job-info --jdl %s"%(JOBID))
    
    if (jdl.find("input/Makefile") == -1 or jdl.find("input/Test0") == -1):
        utils.log_info("ERROR: Final submitted jdl (%s) is not correct"%(jdl))
        raise GeneralError("Check submitted jdl","Final submitted jdl (%s) is not correct"%(jdl))         

    utils.log_info("Check job output")

    utils.job_status(JOBID)

    if utils.JOBSTATUS.find('Done (Success)') != -1 :

        # Check job output
        DIR=Job_utils.output_parametric_job(utils,JOBID)
    
        if os.path.isdir(DIR):
            utils.log_info("Basic output directory exists")
        else:
            utils.log_info("ERROR: Basic output directory does not exist")
            raise GeneralError("Check output files","Basic output directory does not exist")
    
        utils.log_info("Check if node directory is correctly created")

        if os.path.isdir("%s/Node_0"%(DIR)) :
            utils.log_info("Node directory is collectly created")
        else:
            utils.log_info("ERROR: Node directory is not collectly created")
            raise GeneralError("Check output files","Node directories are not correctly created")
               
        utils.log_info("Check if the output files are correctly retrieved")

        if os.path.isfile("%s/Node_0/output.txt"%(DIR)) :
            utils.log_info("Output files are collectly retrieved")    
        else:
            utils.log_info("ERROR: Output files are not collectly retrieved")
            raise GeneralError("Check output files","Output files are not collectly retrieved")

        utils.log_info("Check for files Makefile and Test0 at output.txt")

        outfile=open("%s/Node_0/output.txt"%(DIR), "r")
    
        line=outfile.read()
    
        outfile.close()

        if line.find("Makefile") != 1 and line.find("Test0"):
            utils.log_info("Both files are listed at output.txt")
        else:
            utils.log_info("ERROR: Not both files are listed at output.txt")
            raise GeneralError("Check output file","Not both files are listed at output.txt")
    
    else:
        utils.log_info("ERROR: Job not finished successfully. Retry the test.")
        raise RetryError("Check job final status","Job not finished successfully.")


    utils.log_info("End of regression test for bug %s"%(bug))

