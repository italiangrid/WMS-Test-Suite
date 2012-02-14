#
# Bug:77004
# Title: Wrong myproxyserver string processing in ICE
# Link: https://savannah.cern.ch/bugs/?77004
#
#

import logging
import time

from libutils.Exceptions import *


def run(utils):

    bug='77004'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    logging.info("Prepare jdl file for submission")

    utils.use_external_jdl("%s.jdl"%(bug))
    
    #Get current user identity
    result=utils.run_command_continue_on_error("voms-proxy-info -all")

    for line in result.split("\n"):
        if line.find("identity") !=-1 :
           identity=line.split(":")[1].strip()
        if line.find("attribute") !=-1 :
	   attribute=line.split(":")[1].strip()
           break


    logging.info("Submit the job")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Connect to WMS host: %s"%(utils.get_WMS()))

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Query database table proxy of ice in the WMS")

    CMD="sqlite3 /var/ice/persist_dir/ice.db \"select myproxyurl from proxy where userdn like '%s-%s%%';\""%(identity,attribute)

    result=utils.execute_remote_cmd(ssh,CMD)
   
    result=result.strip(' \n')

    ssh.close()
 
    logging.info("Cancel the submitted job")

    utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))

    logging.info("Check if command's output is empty")

    if len(result) == 0 :
        logging.info("Field myproxyurl is empty as expected")
    else:
      logging.error("Error field 'myproxyurl' is not empty as expected. Get %s while nothing expected"%(result))
      raise GeneralError("","Error !!! Field 'myproxyurl' is not empty as expected. Get %s while nothing expected "%(result))
       
    
    logging.info("End of regression test for bug %s"%(bug))
