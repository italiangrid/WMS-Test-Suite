#
# Bug:73192
# Title: Submission failed due to a credential problem
# Link: https://savannah.cern.ch/bugs/?73192
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='73192'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_deep_jdl(utils.get_jdl_file())

    logging.info("Submit the job")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Submission was successful.")

    logging.info("Cancel the submitted job")

    utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))
     
    logging.info("End of regression test for bug %s"%(bug))
