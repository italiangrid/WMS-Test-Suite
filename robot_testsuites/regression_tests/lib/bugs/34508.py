#
# Bug:34508
# Title: Any collection submitted while the WMS is down is not recovered upon WM startup
# Link: https://savannah.cern.ch/bugs/?34508
#
#


from lib.Exceptions import *
from lib import Job_utils


def run(utils):

    bug='34508'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Stop glite-wms-wm")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm stop")

    utils.log_info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
   
    Job_utils.prepare_collection_job(utils,utils.get_jdl_file())

    utils.log_info("Submit collection")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg --collection %s/collection_jdls"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_tmp_dir()))

    utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

    utils.log_info("Start glite-wms-wm")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm start")

    utils.log_info("Wait until collection is finished")

    utils.wait_until_job_finishes (JOBID)

    utils.log_info("Check final status of collection")

    utils.job_status(JOBID)

    if utils.JOBSTATUS.find('Done (Success)') == -1 :
        utils.log_info("ERROR: Job not finished successfully. Job final status is '%s' instead of 'Done (Success)'"%(utils.get_job_status()))
        raise GeneralError("Check job final status","Job not finished successfully. Job final status is '%s' instead of 'Done (Success)'"%(utils.get_job_status()))
    else:
         utils.log_info("Collection finished successfully. Test OK")

    utils.log_info("End of regression test for bug %s"%(bug))

