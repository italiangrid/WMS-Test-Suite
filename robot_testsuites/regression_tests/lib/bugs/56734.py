#
# Bug: 56734
# Title: ListMatch should consider also SDJ specification 
# Link: https://savannah.cern.ch/bugs/index.php?56734
#
#

from lib.Exceptions import *

def run(utils):

    bug='56734'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Prepare jdl file")
    utils.use_utils_jdl()

    utils.log_info("Execute a listmatch before insterting the attribute 'ShortDeadlineJob = true;' into the jdl file")

    output=utils.run_command("glite-wms-job-list-match %s -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    matched_ces=0

    for line in output.split("\n"):
        if line.find(" - ")!=-1:
            matched_ces=matched_ces+1

    utils.log_info("Add 'ShortDeadlineJob = true;' into the jdl file")

    utils.add_jdl_general_attribute(utils.get_jdl_file(),"ShortDeadlineJob","true")

    utils.log_info("Execute a listmatch after insterting the attribute 'ShortDeadlineJob = true;' into the jdl file")

    output=utils.run_command("glite-wms-job-list-match %s -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    matched_sdj_ces=0

    for line in output.split("\n"):
        if line.find(" - ")!=-1:
            matched_sdj_ces=matched_sdj_ces+1

    utils.log_info("Check that with attribute ShortDeadlineJob enabled only a subset of CEs are returned by the listmatch")

    if matched_sdj_ces >= matched_ces:
         utils.log_info("ERROR: Listmatch with attribute ShortDeadlineJob returned %d CEs while available was %d CEs"%(matched_sdj_ces,matched_ces))
         raise GeneralError("","Listmatch with attribute ShortDeadlineJob returned %d CEs while available was %d CEs"%(matched_sdj_ces,matched_ces))
    else:
         utils.log_info("Check OK. Listmatch with attribute ShortDeadlineJob returned %d CEs while available was %d CEs"%(matched_sdj_ces,matched_ces))

    utils.log_info("Submit a job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

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
