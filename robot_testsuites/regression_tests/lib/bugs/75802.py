#
# Bug: 75802
# Title: Too much flexibility in JDL syntax
# Link: https://savannah.cern.ch/bugs/?75802
#
#

from lib.Exceptions import *


def run(utils):

    bug='75802'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Prepare jdl file for submission")

    utils.use_external_jdl("%s.jdl"%(bug))

    utils.log_info("Submit the job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))
    
    ##check registered jdl
    utils.log_info("Check the registered jdl")
     
    output=utils.run_command("glite-wms-job-info --jdl %s"%(JOBID))
    
    if output.find("Environment = { \"FOO=bar\" };")!=-1:
        utils.log_info("Check ok , Environment = \"FOO=bar\";  has been managed as Environment = { \"FOO=bar\" }; ")
    else:
        utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))
        utils.log_info("ERROR: Test failed , Environment = \"FOO=bar\";  has not been managed as Environment = { \"FOO=bar\" };")
        raise GeneralError("Check registered jdl","Test failed Environment = \"FOO=bar\";  has been managed as Environment = { \"FOO=bar\" };")
    
    utils.log_info("Wait until job finishes")

    utils.wait_until_job_finishes (JOBID)

    utils.log_info("Try to get the output of job %s"%(JOBID))

    utils.job_status(JOBID)

    if utils.get_job_status().find("Done (Success)") != -1 :
         utils.log_info("Retrieve the output")
         utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s"%(utils.get_job_output_dir(),JOBID))

    else:
         utils.log_info("ERROR: Job finishes with status %s cannont retrieve output"%(utils.get_job_status()))
         raise GeneralError("","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))

    env_output=utils.run_command("cat %s/env.out"%(utils.get_job_output_dir()))
    
    utils.log_info("Search for Foo=bar")

    if env_output.find("FOO=bar")!=-1:
         utils.log_info("Check ok, found FOO=bar")
    else:
         utils.log_info("ERROR: Unable to find Foo=bar at env.out")
         raise GeneralError("Check /bin/env output","Unable to find Foo=bar at env.out")
   
    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))
