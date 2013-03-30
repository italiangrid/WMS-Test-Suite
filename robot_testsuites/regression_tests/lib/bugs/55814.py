#
# Bug: 55814
# Title: the amount of information logged to the LB needs to be reviewed
# Link: https://savannah.cern.ch/bugs/?55814
#
#


import time

from lib.Exceptions import *


def run(utils):

    bug='55814'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Prepare jdl file for submission")

    utils.use_external_jdl("%s.jdl"%(bug))

    utils.log_info("Submit the job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Wait 30 secs")

    time.sleep(30)

    utils.log_info("Check if the classad file is not written anymore in the jobcontroller workdir")

    target="/var/jobcontrol/submit/%s"%(JOBID.split(":9000/")[1][0:2])

    output=utils.execute_remote_cmd(ssh,"ls -l %s"%(target)).split("\n")

    ssh.close()
    
    for file in output:
       if file.find("classad")!=-1:
         utils.log_info("Error we found the classad file in the jobcontroller workdir")
         raise GeneralError("Error","Error, we found the classad file in the jobcontroller workdir")


    utils.log_info("Check ok , classad file is not written in the jobcontroller workdir")

    utils.log_info("Check if the classad is logged in the Tansfer event")

    output=utils.run_command("glite-wms-job-logging-info -v 3 -c %s --event Transfer %s"%(utils.get_config_file(),JOBID)).split("\n")

    for line in output:
        if line.find("classad")!=-1:
           utils.log_info("Error , classad is logged in the Transfer event")
           raise GeneralError("Error","Error, classad is logged in the Transfer event")

    utils.log_info("Check ok , classad is not logged in the Transfer event")

    utils.log_info("End of regression test for bug %s"%(bug))
