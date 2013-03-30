#
# Bug:73192
# Title: Submission failed due to a credential problem
# Link: https://savannah.cern.ch/bugs/?73192
#
#

from lib.Exceptions import *

def run(utils):

    bug='73192'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_deep_jdl(utils.get_jdl_file())

    utils.log_info("Submit the job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Submission was successful.")

    utils.log_info("Cancel the submitted job")

    utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))
     
    utils.log_info("End of regression test for bug %s"%(bug))
