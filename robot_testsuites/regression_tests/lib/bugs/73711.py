#
# Bug:73711
# Title: edg_wll_SetLoggingJobProxy with empty sequence code returns "no state in DB"
# Link: https://savannah.cern.ch/bugs/?73711
#
#
# WARNING: to verify this bug you need a WMS set in proxy mode only 
#         (i.e. LBServer must be in another machine)
#          
# It is simply verified by checking that submission for both a job 
# and a collection returns the jobid.

import logging

from lib.Exceptions import *
from lib import Job_utils

def run(utils):

    utils.log_info("Start regression test for bug 73711")

    logging.warning("To verify this bug you need a WMS set in proxy mode only ")

    # Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()

    utils.set_jdl(utils.get_jdl_file())

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Cancel submitted job")

    utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))

    if JOBID.find(utils.get_WMS()) == -1:
        utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))
    else:
        utils.log_info("ERROR: WMS is not set in 'proxy' mode only. We can't verify the bug.")
        raise GeneralError("Check LBServer","WMS is not set in 'proxy' mode only. We can't verify the bug.")

    utils.log_info("Prepare a job collecion")

    Job_utils.prepare_collection_job(utils,utils.get_jdl_file())
     
    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg --collection %s/collection_jdls"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_tmp_dir()))

    utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

    utils.log_info("Cancel submitted job")

    utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))
    
    if JOBID.find(utils.get_WMS()) == -1:
        utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))
    else:
        utils.log_info("ERROR: WMS is not set in 'proxy' mode only. We can't verify the bug.")
        raise GeneralError("Check LBServer","WMS is not set in 'proxy' mode only. We can't verify the bug.")   

    utils.log_info("End of regression test for bug 73711")

