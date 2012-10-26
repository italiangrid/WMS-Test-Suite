#
# Bug: 75802
# Title: Too much flexibility in JDL syntax
# Link: https://savannah.cern.ch/bugs/?75802
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='75802'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Prepare jdl file for submission")

    utils.use_external_jdl("%s.jdl"%(bug))

    logging.info("Submit the job")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)
    
    ##check registered jdl
    logging.info("Check the registered jdl")
     
    output=utils.run_command_continue_on_error("glite-wms-job-info --jdl %s"%(JOBID))
    
    if output.find("Environment = { \"FOO=bar\" };")!=-1:
        logging.info("Check ok , Environment = \"FOO=bar\";  has been managed as Environment = { \"FOO=bar\" }; ")
    else:
        utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))
        logging.error("Test failed , Environment = \"FOO=bar\";  has not been managed as Environment = { \"FOO=bar\" };")
        raise GeneralError("Check registered jdl","Test failed Environment = \"FOO=bar\";  has been managed as Environment = { \"FOO=bar\" };")
    
    logging.info("Wait until job finishes")

    utils.wait_until_job_finishes (JOBID)

    logging.info("Try to get the output of job %s"%(JOBID))

    utils.job_status(JOBID)

    if utils.get_job_status().find("Done (Success)") != -1 :
         logging.info("Retrieve the output")
         utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s"%(utils.get_job_output_dir(),JOBID))

    else:
         logging.error("Job finishes with status %s cannont retrieve output",utils.get_job_status())
         raise GeneralError("","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))

    env_output=utils.run_command_continue_on_error("cat %s/env.out"%(utils.get_job_output_dir()))
    
    logging.info("Search for Foo=bar")

    if env_output.find("FOO=bar")!=-1:
         logging.info("Check ok, found FOO=bar")
    else:
         logging.error("Unable to find Foo=bar at env.out")
         raise GeneralError("Check /bin/env output","Unable to find Foo=bar at env.out")
   
    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
