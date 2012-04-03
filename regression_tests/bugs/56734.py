#
# Bug: 56734
# Title: ListMatch should consider also SDJ specification 
# Link: https://savannah.cern.ch/bugs/index.php?56734
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='56734'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Prepare jdl file")
    utils.use_utils_jdl()

    logging.info("Execute a listmatch before insterting the attribute 'ShortDeadlineJob = true;' into the jdl file")

    output=utils.run_command_continue_on_error("glite-wms-job-list-match %s -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    matched_ces=0

    for line in output.split("\n"):
        if line.find(" - ")!=-1:
            matched_ces=matched_ces+1


    logging.info("Add 'ShortDeadlineJob = true;' into the jdl file")

    utils.add_jdl_general_attribute(utils.get_jdl_file(),"ShortDeadlineJob","true")

    logging.info("Execute a listmatch after insterting the attribute 'ShortDeadlineJob = true;' into the jdl file")

    output=utils.run_command_continue_on_error("glite-wms-job-list-match %s -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    matched_sdj_ces=0

    for line in output.split("\n"):
        if line.find(" - ")!=-1:
            matched_sdj_ces=matched_sdj_ces+1

    logging.info("Check that with attribute ShortDeadlineJob enabled only a subset of CEs are returned by the listmatch")

    if matched_sdj_ces >= matched_ces:
         logging.error("Listmatch with attribute ShortDeadlineJob returned %d CEs while available was %d CEs"%(matched_sdj_ces,matched_ces))
         raise GeneralError("","Listmatch with attribute ShortDeadlineJob returned %d CEs while available was %d CEs"%(matched_sdj_ces,matched_ces))
    else:
         logging.info("Check OK. Listmatch with attribute ShortDeadlineJob returned %d CEs while available was %d CEs"%(matched_sdj_ces,matched_ces))

    
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
