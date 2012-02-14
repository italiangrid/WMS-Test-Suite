#
# Bug:28642
# Title: User environment breaks WMS wrapper
# Link: https://savannah.cern.ch/bugs/?28642
#
#


import logging
import os.path

from libutils.Exceptions import *
from libutils import Job_utils

def run(utils):

    bug='28642'

    logging.info("Start regression test for bug %s"%(bug))
    
    logging.info("Submit the job and wait to finish")

    utils.use_external_jdl("%s.jdl"%(bug))

    JOBID=Job_utils.submit_wait_finish(utils,"")

    Job_utils.output_normal_job(utils,JOBID)

    #Check job output
    logging.info("Check if the output files are correctly retrieved")

    if os.path.isfile("%s/input1.txt"%(utils.get_job_output_dir())) & os.path.isfile("%s/env.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/env.err"%(utils.get_job_output_dir())) :
          logging.info("Output files are collectly retrieved")
    else:
          logging.error("Output files are not correctly retrieved")
          raise GeneralError("","Output files are not correctly retrieved")

    #Check the content of env.out file
    logging.info("Check the content of the env.out file")

    result=utils.run_command_continue_on_error("cat %s/env.out"%(utils.get_job_output_dir()))

    if result.find("LD_LIBRARY_PATH=.") != -1 :
        logging.info("Environment variable LD_LIBRARY_PATH has value '.' as expected")
    else:
      logging.error("Error value of environment variable LD_LIBRARY_PATH")
      raise GeneralError("","Error !!! Error value of environment variable LD_LIBRARY_PATH")
       
    logging.info("End of regression test for bug %s",bug)
