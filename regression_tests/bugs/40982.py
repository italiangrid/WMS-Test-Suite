#
# Bug:40982
# Title: When a collection is aborted the "Abort" event should be logged for the sub-nodes as well 
# Link: https://savannah.cern.ch/bugs/?40982
#
#


import logging

from libutils.Exceptions import *

def run(utils):

    bug='40982'

    logging.info("Start regression test for bug %s"%(bug))
    
    logging.info("Submit the job and wait to finish")

    utils.use_external_jdl("%s.jdl"%(bug))

    logging.info("Register the collection")

    JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg --register-only %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Start job execution")

    utils.run_command_continue_on_error ("glite-wms-job-submit --start %s"%(JOBID))

    logging.info("Wait the job to finish")

    utils.wait_until_job_finishes(JOBID)

    logging.info("Check job final status")

    output=utils.run_command_continue_on_error("glite-wms-job-status  %s "%(JOBID))

    if int(output.count("Aborted")) == 11 :
        logging.info("We have 11 Abort events as expected")
    else:
      logging.error("Error wrong number of abort events. Get %s expected 11"%(counter))
      raise GeneralError("","Error !!! Error retry count. Get %s expected 11"%(counter))


    logging.info("End of regression test for bug %s",bug)
