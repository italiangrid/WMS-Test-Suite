#
# Bug: 98279
# Title:Job perusal is broken in EMI-2 WMS
# Link: https://savannah.cern.ch/bugs/?98279
#
#


import time
import glob

from lib.Exceptions import *


def run(utils):

    bug='98279'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Create perusal jdl")

    utils.use_external_jdl("%s.jdl"%(bug))

    utils.log_info("Submit job")

    JOBID=utils.run_command("glite-wms-job-submit %s --nomsg -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Enable perusal operation for file out.txt")

    utils.run_command("glite-wms-job-perusal --set -f out.txt %s"%(JOBID))

    utils.log_info("Wait until job's state is Running")

    utils.job_status(JOBID)


    while utils.get_job_status().find("Running")==-1 and utils.job_is_finished(JOBID)==0:
        time.sleep(30)
        utils.job_status(JOBID)

    utils.job_status(JOBID)

    if utils.job_is_finished(JOBID) !=0:
        utils.log_info("ERROR: Job's status is %s  , can't continue."%(utils.get_job_status()))
        raise GeneralError("Check job's status","Job's status is %s  , can't continue."%(utils.get_job_status()))

    utils.log_info("Wait for 1010 secs")

    time.sleep(1010)

    utils.run_command("glite-wms-job-perusal --get -f out.txt --dir %s %s"%(utils.get_job_output_dir(),JOBID))

    utils.log_info("Check if some chunkes have been retrieved")

    filespec="out.txt-*"

    first_try_chunk=glob.glob(os.path.join(utils.get_job_output_dir(),filespec))

    if len(first_try_chunk):
          utils.log_info("These chunks have been retrieved: %s"%(first_try_chunk))
    else:
          utils.log_info("ERROR: No chunks have been retrieved")
          raise GeneralError("glite-wms-job-perusal --get","No chunks have been retrieved.")

    
    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))
