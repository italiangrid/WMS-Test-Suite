#
# Bug: 53294
# Title: WMS 3.2 WMProxy logs are useless below level 6
# Link: https://savannah.cern.ch/bugs/index.php?53294
#
#

import logging
import socket

from libutils.Exceptions import *

def run(utils):

    bug='53294'

    log_file="/var/log/wms/wmproxy.log"

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Set WMProxy log level to 5 to glite_wms.conf at WMS")

    utils.change_attribute_at_remote_file_section(ssh,"/etc/glite-wms/glite_wms.conf", 'LogLevel','WorkloadManagerProxy','5')

    logging.info("Stop workload manager proxy glite-wms-wmproxy")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy stop")

    logging.info("Remove existing workload manager proxy log file: %s"%(log_file))

    utils.execute_remote_cmd(ssh,"rm -f %s"%(log_file))

    logging.info("Start workload manager proxy glite-wms-wmproxy")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy start")

    logging.info("Submit job and check log file")

    utils.use_utils_jdl()

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.ssh_get_file(ssh, "%s"%(log_file), "%s/local_copy"%(utils.get_tmp_dir()))

    FILE=open("%s/local_copy"%(utils.get_tmp_dir()))
    log_lines=FILE.readlines()
    log_lines=''.join(log_lines)
    FILE.close()

    dn=utils.run_command_continue_on_error("voms-proxy-info -subject")
    fqan=utils.run_command_continue_on_error("voms-proxy-info -fqan")
     
    ui=socket.gethostname()

    messages=log_lines.split("================== Incoming Request ==================")

    checks=['Remote Host Name: %s'%(ui),'Remote CLIENT S DN: %s'%(dn),fqan]

    find=0

    for msg in messages[1:]:

        for check in checks:
            find=find+msg.count(check)
            
        if find!=len(checks):
            logging.error("Unable to find all required information at block:\n %s \n"%(msg))
            logging.info("Restore the initial glite_wms.conf file")
            utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
            utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
            raise GeneralError("","Unable to find all required information at block:\n %s \n"%(msg))
        else:
            logging.info("Find all required information at block:\n %s"%(msg))

        find=0

    logging.info("Test OK")
   
    logging.info("Restore the initial glite_wms.conf file")

    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    ssh.close()

    logging.info("End of regression test for bug %s"%(bug))
