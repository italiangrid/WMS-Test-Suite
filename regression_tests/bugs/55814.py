#
# Bug: 55814
# Title: the amount of information logged to the LB needs to be reviewed
# Link: https://savannah.cern.ch/bugs/?55814
#
#

import logging
import time

from libutils.Exceptions import *

def run(utils):

    bug='55814'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Prepare jdl file for submission")

    utils.use_external_jdl("%s.jdl"%(bug))

    logging.info("Submit the job")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Wait 30 secs")

    time.sleep(30)

    logging.info("Check if the classad file is not written anymore in the jobcontroller workdir")

    target="/var/jobcontrol/submit/%s"%(JOBID.split(":9000/")[1][0:2])

    output=utils.execute_remote_cmd(ssh,"ls -l %s"%(target)).split("\n")

    ssh.close()
    
    for file in output:
       if file.find("classad")!=-1:
         logging.error("Error we found the classad file in the jobcontroller workdir")
         raise GeneralError("Error","Error, we found the classad file in the jobcontroller workdir")


    logging.info("Check ok , classad file is not written in the jobcontroller workdir")

    logging.info("Check if the classad is logged in the Tansfer event")

    output=utils.run_command_continue_on_error("glite-wms-job-logging-info -v 3 -c %s --event Transfer %s"%(utils.get_config_file(),JOBID)).split("\n")

    for line in output:
        if line.find("classad")!=-1:
           logging.error("Error , classad is logged in the Transfer event")
           raise GeneralError("Error","Error, classad is logged in the Transfer event")

    logging.info("Check ok , classad is not logged in the Transfer event")

    logging.info("End of regression test for bug %s"%(bug))
