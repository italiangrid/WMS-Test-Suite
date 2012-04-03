#
# Bug: 84155
# Title: Internal proxy structure convertion error in ICE 
# Link: https://savannah.cern.ch/bugs/?84155
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='84155'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you have to set the PROXY_PASSWORD attribute for user proxy password at configuration file")

    if utils.PROXY_PASSWORD=='':
       logging.warn("Please set the required variable PROXY_PASSWORD in test's configuration file")
       raise GeneralError("Missing required configuration attribute","Please set the required variable PROXY_PASSWORD in test's configuration file")

    logging.info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_external_jdl("%s.jdl"%(bug))
    utils.add_jdl_attribute(utils.get_jdl_file(),'MyProxyServer',"%s"%utils.get_MYPROXY_SERVER())

    logging.info("Create a short proxy, valid for 14 minutes")

    utils.run_command_continue_on_error("echo %s | voms-proxy-init --voms %s --valid 00:14 -pwstdin"%(utils.PROXY_PASSWORD,utils.VO))

    logging.info("Submit the job")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Check that job's proxy is valid for no more than 14 minutes")

    output=utils.run_command_continue_on_error ("glite-wms-job-info -p %s"%(JOBID))

    for line in output.splitlines():
            if line.split(":")[0].strip() == "Timeleft":
                token=line.split(":")[1].strip()
                if ( (token.split(" ")[1] == "hours") or
                   (int(token.split(" ")[0]) > 14 ) ):
                    logging.error("The proxy of the submitted job has not the expected duration")
                    raise GeneralError("Check proxy of the submitted job","Wrong duration")


    logging.info("Create a long proxy")

    utils.run_command_continue_on_error("echo %s | voms-proxy-init --voms %s -pwstdin "%(utils.PROXY_PASSWORD,utils.VO))

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
