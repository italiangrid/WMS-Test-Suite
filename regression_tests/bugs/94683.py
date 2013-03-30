#
# Bug: 94683
# Title: Better output message from glite-wms-job-status for missing jobs
# Link: https://savannah.cern.ch/bugs/?94683
#
#

import logging

from libutils.Exceptions import *

def run(utils):

    bug='98524'

    logging.info("Start regression test for bug %s"%(bug))
 
    logging.info("Submit a job to get a valid job id")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())
    
    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Extend job id with 2 characters to get an invalid job job id")

    TEST_JOBID="%s01"%(JOBID)

    logging.info("Get status for the invalid job id: %s"%(TEST_JOBID))

    message=utils.run_command_fail_continue_on_error("glite-wms-job-status %s"%(TEST_JOBID))

    if message.find("at glite::lb::Job::status[./src/Job.cpp:87]") !=-1 or message.find("Error while calling the \"Job:getStatus\" native api")!=-1 or message.find("glite.lb.Exception: edg_wll_JobStatus: No such file or directory: no matching jobs found") !=-1 :
        logging.error("Get the old output message from glite-wms-job-status fro missing jobs")
        logging.error("Output message: %s"%(message))
        raise GeneralError("Check output message from glite-wms-job-status fro missing jobs","Get the old output message from glite-wms-job-status fro missing jobs")
    else:
        logging.info("Find the new output message for missing jobs")

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
