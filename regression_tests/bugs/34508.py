#
# Bug:34508
# Title: Any collection submitted while the WMS is down is not recovered upon WM startup
# Link: https://savannah.cern.ch/bugs/?34508
#
#

import logging

from libutils.Exceptions import *
from libutils import Job_utils


def run(utils):

    bug='34508'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Stop glite-wms-wm")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm stop")

    logging.info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
   
    Job_utils.prepare_collection_job(utils,utils.get_jdl_file())

    logging.info("Submit collection")

    JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg --collection %s/collection_jdls"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_tmp_dir()))

    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

    logging.info("Start glite-wms-wm")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm start")

    logging.info("Wait until collection is finished")

    utils.wait_until_job_finishes (JOBID)

    logging.info("Check final status of collection")

    utils.job_status(JOBID)

    if utils.JOBSTATUS.find('Done (Success)') == -1 :
        logging.error("Job not finished successfully. Job final status is '%s' instead of 'Done (Success)'"%(utils.get_job_status()))
        raise GeneralError("Check job final status","Job not finished successfully. Job final status is '%s' instead of 'Done (Success)'"%(utils.get_job_status()))
    else:
         logging.info("Collection finished successfully. Test OK")

    logging.info("End of regression test for bug %s"%(bug))
