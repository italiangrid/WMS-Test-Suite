#
# Bug: 88128
# Title: Submission with rfc proxy doesn't work 
# Link: https://savannah.cern.ch/bugs/?88128
#
#

from lib.Exceptions import *


def run(utils):

    bug='88128'

    utils.log_info("Start regression test for bug %s"%(bug))

    if utils.PROXY_PASSWORD=='':
       utils.log_info("ERROR: Please set the required variable PROXY_PASSWORD in test's configuration file")
       raise GeneralError("Missing required configuration attribute","Please set the required variable PROXY_PASSWORD in test's configuration file")

    utils.log_info("Prepare jdl file for submission to CREAM CE")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.change_jdl_attribute(utils.get_jdl_file(), "ShallowRetryCount", "1")
    utils.set_destination_ce(utils.get_jdl_file(),"/cream-")

    utils.log_info("Create a RFC proxy")

    utils.run_command("echo %s | voms-proxy-init --voms %s -rfc -pwstdin"%(utils.PROXY_PASSWORD,utils.VO))

    utils.log_info("Submit the job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Wait until job finishes")

    utils.wait_until_job_finishes(JOBID)

    utils.log_info("Check job stauts")

    utils.job_status(JOBID)

    if utils.get_job_status().find("Done (Success)")!=-1:
        utils.log_info("Test OK , job terminated successfully")
    else:
      utils.log_info("ERROR: Job status is not 'Done (Success)', job failed to terminated successfully. Status reason %s"%(utils.get_StatusReason(JOBID)))
      raise GeneralError("Check job status","Job status is not 'Done (Success)' but %s. Status reason %s"%(utils.get_job_status(),utils.get_StatusReason(JOBID)))

    utils.log_info("End of regression test for bug %s"%(bug))
