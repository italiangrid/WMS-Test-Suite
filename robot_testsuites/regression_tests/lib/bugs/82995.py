#
# Bug: 82995
# Title: glite-wms-job-status needs a json-compliant format
# Link: https://savannah.cern.ch/bugs/?82995
#
#

import simplejson as jsn

from lib.Exceptions import *

def run(utils):

    bug='82995'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Submit a job and wait to finish")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Job submitted successfuly. Returned JOBID: %s",JOBID)

    utils.log_info("Try glite-wms-job-status with --json option")

    output=utils.run_command("glite-wms-job-status --json %s"%(JOBID))

    utils.log_info("Command executed")
 
    utils.log_info("Cancel submitted job")
  
    utils.run_command("glite-wms-job-cancel --noint %s "%(JOBID))

    utils.log_info("Try to validate json result")

    try:
          r=jsn.loads(output)
    except ValueError:
          utils.log_info("ERROR: glite-wms-job-status --json: Output is not a valid json string")
          utils.log_info("ERROR: Output:%s"%(output))
          raise GeneralError("Validate glite-wms-job-status --json output","glite-wms-job-status --json: Output is not a valid json string")            

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))
