#
# Bug:48636
# Title: job wrapper should log events for truncated files
# Link: https://savannah.cern.ch/bugs/?48636
#
#

import logging

from libutils.Exceptions import *
from libutils import Job_utils

def run(utils):

    bug='48636'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Set MaxOutputSandboxSize=50M; to glite_wms.conf at WMS")

    utils.change_remote_file(ssh,"/etc/glite-wms/glite_wms.conf", ['MaxOutputSandboxSize'],['*'],['50M'])

    logging.info("Restart workload manager glite-wms-wm")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    logging.info("Submit the job and wait to finish")

    utils.use_external_jdl("%s.jdl"%(bug))

    JOBID=Job_utils.submit_wait_finish(utils,"")

    logging.info("Check job status")
    
    result=utils.run_command_continue_on_error("glite-wms-job-logging-info -v 3 --event UserTag %s"%(JOBID))


    if result.find("OSB quota exceeded for") == -1:
        logging.error("Not found message 'OSB quota exceeded for' at UserTag")
        utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
        raise GeneralError("Check UserTag event","Not found message 'OSB quota exceeded for' at UserTag")

    if result.find("Truncated last 52428800 bytes for file") == -1:
        logging.error("Not found message 'Truncated last 52428800 bytes for file")
        utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
        raise GeneralError("Check UserTag event","Not found message 'Truncated last 52428800 bytes for file' at UserTag")

        
    logging.info("Restore the initial glite_wms.conf file")

    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
   
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
    
    ssh.close()
    
    logging.info("End of regression test for bug %s"%(bug))