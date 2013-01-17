#
# Bug: 91941
# Title: The job replanner should be configurable
# Link: https://savannah.cern.ch/bugs/?91941
#
#

import logging
import time

from libutils.Exceptions import *


def run(utils):

    bug='91941'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())
  
    logging.info("Set EnableReplanner=true; at glite_wms.conf")
 
    config_file='/etc/glite-wms/glite_wms.conf'

    log_file='/var/log/wms/workload_manager_events.log'

    utils.change_remote_file(ssh, config_file, ['EnableReplanner'], ['*'],['true'])

    logging.info("Clear Workload Manager File")

    utils.execute_remote_cmd(ssh,"mv %s %s_%s"%(log_file,log_file,time.strftime("%Y%m%d%H%M%S")))

    logging.info("Restart Workload Manager")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    logging.info("Check if the job replanner is enabled")
   
    utils.ssh_get_file(ssh,log_file,"%s/local_copy"%(utils.get_tmp_dir()))

    FILE=open("%s/local_copy"%(utils.get_tmp_dir()))
    lines=' '.join(FILE.readlines());
    FILE.close()
   
    if lines.find("replanner in action")!=-1:
        logging.info("Job replanner is in action as expected")
    else:
        logging.error("Job replanner is not in action as expected")
        utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
        raise GeneralError("Check if job replanner is enabled","Job replanner is not in action as expected")

    utils.run_command_continue_on_error("rm -rf %s/local_copy"%(utils.get_tmp_dir()))
    
    logging.info("Set EnableReplanner=false; at glite_wms.conf")

    utils.change_remote_file(ssh, config_file, ['EnableReplanner'], ['*'],['false'])

    logging.info("Clear Workload Manager File")

    utils.execute_remote_cmd(ssh,"mv %s %s_%s"%(log_file,log_file,time.strftime("%Y%m%d%H%M%S")))

    logging.info("Restart Workload Manager")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    time.sleep(10)

    logging.info("Check if the job replanner is disabled")

    utils.ssh_get_file(ssh,log_file,"%s/local_copy"%(utils.get_tmp_dir()))

    FILE=open("%s/local_copy"%(utils.get_tmp_dir()))
    lines=' '.join(FILE.readlines());
    FILE.close()

    if lines.find("replanner in action")==-1:
        logging.info("Job replanner is not in action as expected")
    else:
        logging.error("Job replanner did not disabled , instead it is in action")
        utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
        raise GeneralError("Check if job replanner is disabled","Job replanner did not disabled , instead it is in action")

    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    utils.close_ssh(ssh)

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))

