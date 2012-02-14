#
# Bug:79141
# Title: various bugs about parametric jobs
# Link: https://savannah.cern.ch/bugs/?79141
#
#

import logging
import os.path

from libutils.Exceptions import *
from libutils import Job_utils


def run(utils):

    bug='79141'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Submit a parametric job and wait until finish")

    utils.use_external_jdl("%s.jdl"%(bug))
    
    JOBID=Job_utils.submit_wait_finish(utils,"")
    
    jdl=utils.run_command_continue_on_error("glite-wms-job-info --jdl %s"%(JOBID))
    
    if (jdl.find("input/Makefile") == -1 or jdl.find("input/Test0") == -1):
        logging.error("Final submitted jdl (%s) is not correct"%(jdl))
        raise GeneralError("Check submitted jdl","Final submitted jdl (%s) is not correct"%(jdl))         

    logging.info("Check job output")

    utils.job_status(JOBID)

    if utils.JOBSTATUS.find('Done (Success)') != -1 :

        # Check job output
        DIR=Job_utils.output_parametric_job(utils,JOBID)
    
        if os.path.isdir(DIR):
            logging.info("Basic output directory exists")
        else:
            logging.error("Basic output directory does not exist")
            raise GeneralError("Check output files","Basic output directory does not exist")
    

        logging.info("Check if node directory is correctly created")

        if os.path.isdir("%s/Node_0"%(DIR)) :
            logging.info("Node directory is collectly created")
        else:
            logging.error("Node directory is not collectly created")
            raise GeneralError("Check output files","Node directories are not correctly created")
               

        logging.info("Check if the output files are correctly retrieved")

        if os.path.isfile("%s/Node_0/output.txt"%(DIR)) :
            logging.info("Output files are collectly retrieved")    
        else:
            logging.error("Output files are not collectly retrieved")
            raise GeneralError("Check output files","Output files are not collectly retrieved")


        logging.info("Check for files Makefile and Test0 at output.txt")

        outfile=open("%s/Node_0/output.txt"%(DIR), "r")
    
        line=outfile.read()
    
        outfile.close()

        if ( line.find("Makefile") != 1 and line.find("Test0")):
            logging.info("Both files are listed at output.txt")
        else:
            logging.error("Not both files are listed at output.txt")
            raise GeneralError("Check output file","Not both files are listed at output.txt")
    
    else:
        logging.error("Job not finished successfully. Retry the test.")
        raise RetryError("Check job final status","Job not finished successfully.")


    logging.info("End of regression test for bug %s"%(bug))
