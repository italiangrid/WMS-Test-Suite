#
# Bug: 98279
# Title:Job perusal is broken in EMI-2 WMS
# Link: https://savannah.cern.ch/bugs/?98279
#
#

import logging
import time
import glob

from libutils.Exceptions import *


def run(utils):

    bug='98279'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Create perusal jdl")

    utils.use_external_jdl("%s.jdl"%(bug))

    logging.info("Submit job")

    JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --nomsg -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Enable perusal operation for file out.txt")

    utils.run_command_continue_on_error ("glite-wms-job-perusal --set -f out.txt %s"%(JOBID))

    logging.info("Wait until job's state is Running")

    utils.job_status(JOBID)


    while utils.get_job_status().find("Running")==-1 and utils.job_is_finished(JOBID)==0:
        time.sleep(30)
        utils.job_status(JOBID)

    utils.job_status(JOBID)

    if utils.job_is_finished(JOBID) !=0:
        logging.error("Job's status is %s  , can't continue."%(utils.get_job_status()))
        raise GeneralError("Check job's status","Job's status is %s  , can't continue."%(utils.get_job_status()))

    logging.info("Wait for 1010 secs")

    time.sleep(1010)

    utils.run_command_continue_on_error ("glite-wms-job-perusal --get -f out.txt --dir %s %s"%(utils.get_job_output_dir(),JOBID))

    logging.info("Check if some chunkes have been retrieved")

    filespec="out.txt-*"

    first_try_chunk=glob.glob(os.path.join(utils.get_job_output_dir(),filespec))

    if len(first_try_chunk):
          logging.info("These chunks have been retrieved: %s"%(first_try_chunk))
    else:
          logging.error("TEST FAILS. No chunks have been retrieved")
          raise GeneralError("glite-wms-job-perusal --get","No chunks have been retrieved.")

    
    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
