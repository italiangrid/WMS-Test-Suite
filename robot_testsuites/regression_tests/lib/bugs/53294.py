#
# Bug: 53294
# Title: WMS 3.2 WMProxy logs are useless below level 6
# Link: https://savannah.cern.ch/bugs/index.php?53294
#
#


import socket

from lib.Exceptions import *


def run(utils):

    bug='53294'

    log_file="/var/log/wms/wmproxy.log"

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
  
    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Set WMProxy log level to 5 to glite_wms.conf at WMS")

    utils.change_attribute_at_remote_file_section(ssh,"/etc/glite-wms/glite_wms.conf", 'LogLevel','WorkloadManagerProxy','5')

    utils.log_info("Stop workload manager proxy glite-wms-wmproxy")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy stop")

    utils.log_info("Remove existing workload manager proxy log file: %s"%(log_file))

    utils.execute_remote_cmd(ssh,"rm -f %s"%(log_file))

    utils.log_info("Start workload manager proxy glite-wms-wmproxy")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy start")

    utils.log_info("Submit job and check log file")

    utils.use_utils_jdl()

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.ssh_get_file(ssh, "%s"%(log_file), "%s/local_copy"%(utils.get_tmp_dir()))

    FILE=open("%s/local_copy"%(utils.get_tmp_dir()))
    log_lines=FILE.readlines()
    log_lines=''.join(log_lines)
    FILE.close()

    dn=utils.run_command("voms-proxy-info -subject")
    fqan=utils.run_command("voms-proxy-info -fqan")
     
    ui=socket.gethostname()

    messages=log_lines.split("================== Incoming Request ==================")

    checks=['Remote Host Name: %s'%(ui),'Remote CLIENT S DN: %s'%(dn),fqan]

    find=0

    for msg in messages[1:]:

        for check in checks:
            find=find+msg.count(check)
            
        if find!=len(checks):
            utils.log_info("ERROR: Unable to find all required information at block:\n %s \n"%(msg))
            utils.log_info("Restore the initial glite_wms.conf file")
            utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
            utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
            raise GeneralError("","Unable to find all required information at block:\n %s \n"%(msg))
        else:
            utils.log_info("Find all required information at block:\n %s"%(msg))

        find=0

    utils.log_info("Test OK")
   
    utils.log_info("Restore the initial glite_wms.conf file")

    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    ssh.close()

    utils.log_info("End of regression test for bug %s"%(bug))
