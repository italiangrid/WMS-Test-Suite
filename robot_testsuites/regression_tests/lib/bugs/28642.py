#
# Bug:28642
# Title: User environment breaks WMS wrapper
# Link: https://savannah.cern.ch/bugs/?28642
#
#


import os.path

from lib.Exceptions import *
from lib import Job_utils


def run(utils):

    bug='28642'

    utils.log_info("Start regression test for bug %s"%(bug))
    
    utils.log_info("Submit the job and wait to finish")

    utils.use_external_jdl("%s.jdl"%(bug))

    JOBID=Job_utils.submit_wait_finish(utils,"")

    Job_utils.output_normal_job(utils,JOBID)

    #Check job output
    utils.log_info("Check if the output files are correctly retrieved")

    if os.path.isfile("%s/input1.txt"%(utils.get_job_output_dir())) & os.path.isfile("%s/env.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/env.err"%(utils.get_job_output_dir())) :
          utils.log_info("Output files are collectly retrieved")
    else:
          utils.log_info("ERROR: Output files are not correctly retrieved")
          raise GeneralError("","Output files are not correctly retrieved")

    #Check the content of env.out file
    utils.log_info("Check the content of the env.out file")

    result=utils.run_command("cat %s/env.out"%(utils.get_job_output_dir()))

    if result.find("LD_LIBRARY_PATH=.") != -1 :
        utils.log_info("Environment variable LD_LIBRARY_PATH has value '.' as expected")
    else:
      utils.log_info("Error value of environment variable LD_LIBRARY_PATH")
      raise GeneralError("","Error !!! Error value of environment variable LD_LIBRARY_PATH")
       
    utils.log_info("End of regression test for bug %s",bug)
