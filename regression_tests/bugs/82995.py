#
# Bug: 82995
# Title: glite-wms-job-status needs a json-compliant format
# Link: https://savannah.cern.ch/bugs/?82995
#
#

import logging
import simplejson as jsn

from libutils.Exceptions import *

def run(utils):

    bug='82995'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Submit a job and wait to finish")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

    logging.info("Try glite-wms-job-status with --json option")

    output=utils.run_command_continue_on_error("glite-wms-job-status --json %s"%(JOBID))

    logging.info("Command executed")
 
    logging.info("Cancel submitted job")
  
    utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s "%(JOBID))

    logging.info("Try to validate json result")

    try:
          r=jsn.loads(output)
    except ValueError:
          logging.error("glite-wms-job-status --json: Output is not a valid json string")
          logging.error("Output:%s"%(output))
          raise GeneralError("Validate glite-wms-job-status --json output","glite-wms-job-status --json: Output is not a valid json string")            

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
