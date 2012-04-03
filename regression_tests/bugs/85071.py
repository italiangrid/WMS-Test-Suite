#
# Bug: 85071
# Title: Wmproxy authorization breaks with longer proxy chain
# Link: https://savannah.cern.ch/bugs/?85071
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='85071'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warn("Interactive test")

    utils.show_critical("Interactive test")

    if utils.MYPROXYSERVER =='' :
        logging.error("Please set the required variable MYPROXYSERVER at configuration file.")
        raise GeneralError("Check Configuration","Please set the required variable MYPROXYSERVER at configuration file.")

    logging.info("Prepare jdl file for submission")
    utils.use_utils_jdl()
  
    logging.info("Store a credential for later retrieval")

    utils.run_command_continue_on_error("myproxy-init -d -s %s "%(utils.MYPROXYSERVER))

    logging.info("Retrieve a new proxy from the myproxy server")

    utils.run_command_continue_on_error("myproxy-logon -d -s %s --voms %s "%(utils.MYPROXYSERVER,utils.VO))

    logging.info("Check that we have a proxy with a longer chain")

    result=utils.run_command_continue_on_error("voms-proxy-info -all")

    result=result.split("\n")

    for line in result:
        if line.find("subject")!=-1:
            subject=line
            break

  
    if subject.count("CN=proxy")!=4:
       logging.error("Test failed. Problem with proxy chain . Subject is (%s)"%(subject))
       raise GeneralError("Test failed","Problem with proxy chain. Subject is (%s)"%(subject))

    logging.info("Submit a job")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

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
