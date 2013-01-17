#
# Bug: 88128
# Title: Submission with rfc proxy doesn't work 
# Link: https://savannah.cern.ch/bugs/?88128
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='88128'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you have to set the PROXY_PASSWORD attribute at configuration file")

    if utils.PROXY_PASSWORD=='':
       logging.warn("Please set the required variable PROXY_PASSWORD in test's configuration file")
       raise GeneralError("Missing required configuration attribute","Please set the required variable PROXY_PASSWORD in test's configuration file")

    logging.info("Prepare jdl file for submission to CREAM CE")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.change_jdl_attribute(utils.get_jdl_file(), "ShallowRetryCount", "1")
    utils.set_destination_ce(utils.get_jdl_file(),"/cream-")

    logging.info("Create a RFC proxy")

    utils.run_command_continue_on_error("echo %s | voms-proxy-init --voms %s -rfc -pwstdin"%(utils.PROXY_PASSWORD,utils.VO))

    logging.info("Submit the job")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Wait until job finishes")

    utils.wait_until_job_finishes(JOBID)

    logging.info("Check job stauts")

    utils.job_status(JOBID)

    if utils.get_job_status().find("Done (Success)")!=-1:
        logging.info("Test OK , job terminated successfully")
    else:
      logging.error("Job status is not 'Done (Success)', job failed to terminated successfully. Status reason %s"%(utils.get_StatusReason(JOBID)))
      raise GeneralError("Check job status","Job status is not 'Done (Success)' but %s. Status reason %s"%(utils.get_job_status(),utils.get_StatusReason(JOBID)))

    logging.info("End of regression test for bug %s"%(bug))
