#
# Bug: 91941
# Title: The job replanner should be configurable
# Link: https://savannah.cern.ch/bugs/?91941
#
#

import time

from lib.Exceptions import *


def run(utils):

    bug='91941'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())
  
    utils.log_info("Set EnableReplanner=true; at glite_wms.conf")
 
    config_file='/etc/glite-wms/glite_wms.conf'

    log_file='/var/log/wms/workload_manager_events.log'

    utils.change_remote_file(ssh, config_file, ['EnableReplanner'], ['*'],['true'])

    utils.log_info("Clear Workload Manager File")

    utils.execute_remote_cmd(ssh,"mv %s %s_%s"%(log_file,log_file,time.strftime("%Y%m%d%H%M%S")))

    utils.log_info("Restart Workload Manager")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    utils.log_info("Check if the job replanner is enabled")
   
    utils.ssh_get_file(ssh,log_file,"%s/local_copy"%(utils.get_tmp_dir()))

    FILE=open("%s/local_copy"%(utils.get_tmp_dir()))
    lines=' '.join(FILE.readlines());
    FILE.close()
   
    if lines.find("replanner in action")!=-1:
        utils.log_info("Job replanner is in action as expected")
    else:
        utils.log_info("ERROR: Job replanner is not in action as expected")
        utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
        raise GeneralError("Check if job replanner is enabled","Job replanner is not in action as expected")

    utils.run_command("rm -rf %s/local_copy"%(utils.get_tmp_dir()))
    
    utils.log_info("Set EnableReplanner=false; at glite_wms.conf")

    utils.change_remote_file(ssh, config_file, ['EnableReplanner'], ['*'],['false'])

    utils.log_info("Clear Workload Manager File")

    utils.execute_remote_cmd(ssh,"mv %s %s_%s"%(log_file,log_file,time.strftime("%Y%m%d%H%M%S")))

    utils.log_info("Restart Workload Manager")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    time.sleep(10)

    utils.log_info("Check if the job replanner is disabled")

    utils.ssh_get_file(ssh,log_file,"%s/local_copy"%(utils.get_tmp_dir()))

    FILE=open("%s/local_copy"%(utils.get_tmp_dir()))
    lines=' '.join(FILE.readlines());
    FILE.close()

    if lines.find("replanner in action")==-1:
        utils.log_info("Job replanner is not in action as expected")
    else:
        utils.log_info("ERROR: Job replanner did not disabled , instead it is in action")
        utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
        raise GeneralError("Check if job replanner is disabled","Job replanner did not disabled , instead it is in action")

    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    utils.close_ssh(ssh)

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))

