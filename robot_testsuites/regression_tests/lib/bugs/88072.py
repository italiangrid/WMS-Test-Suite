#
# Bug:88072
# Title: EMI-1 WMS cannot submit to ARC CEs 
# Link: https://savannah.cern.ch/bugs/?88072
#
#

import time
import os.path

from lib.Exceptions import *


def run(utils):

    bug='88072'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Prepare jdl file for submission to some ARC CE")

    dest='/nordugrid'

    # Necessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())
    utils.set_destination_ce(utils.get_jdl_name(),dest)
   
    utils.log_info("Submit job to ARC CE")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

    utils.log_info("Wait 60 secs before check job")
    time.sleep(60)

    CENAME=utils.get_CE(JOBID)

    utils.log_info("Check if match ARC CE")

    if CENAME.find(dest)==-1:
        utils.log_info("ERROR: Matching CE is not ARC CE. CE is %s"%(CENAME))
        utils.log_info("Cancel job %s"%(JOBID))
        utils.run_command("glite-wms-job-cancel --noint -c %s %s"%(utils.get_config_file(),JOBID))
        raise GeneralError("Check if match ARC CE","Matching CE is not ARC CE. CE is %s"%(CENAME))
    else:
       utils.log_info("Matchmaking is ok, now wait the job to finish")

    utils.wait_until_job_finishes (JOBID)

    utils.log_info("Try to get the output of the normal job")

    utils.job_status(JOBID)

    if utils.get_job_status().find("Done (Success)") != -1 :

        utils.remove(utils.get_tmp_file())

        utils.log_info("Retrieve the output")

        utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))
        utils.log_info("Check if the output files are correctly retrieved")

        if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
            utils.log_info("Output files are collectly retrieved")
            utils.log_info("std.out content:\n%s"%(utils.run_command("cat %s/std.out"%(utils.get_job_output_dir()))))
        else:
            utils.log_info("ERROR: Output files are not correctly retrieved")
            raise GeneralError("Check output files","Output files are not correctly retrieved")
    
    else:
        utils.log_info("ERROR: Job finishes with status %s cannont retrieve output"%(utils.get_job_status()))
        raise GeneralError("","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))

    utils.log_info("Check job's final status")

    output=utils.run_command("glite-wms-job-status %s"%(JOBID))
 
    status=''

    for line in output.split("\n"):
        if line.find("Current Status:")!=-1:
              status=line.split(":")[1].strip(' \t\n')
              break

    if status!='Cleared':
         utils.log_info("Job's final status after output retrieval is not Cleared as expected but %s"%(utils.get_job_status()))
         raise GeneralError("","Job's final status after output retrieval is not Cleared as expected but %s"%(utils.get_job_status()))
    else:
         utils.log_info("Job's final status is Cleared as expected")

    utils.log_info("Test OK")
    
    utils.log_info("End of regression test for bug %s"%(bug))
