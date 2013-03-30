#
# Bug: 85327
# Title: [yaim-wms] glite-wms-wmproxy.restart.cron missing HOSTNAME environment variable
# Link: https://savannah.cern.ch/bugs/?85327
#
#

from lib.Exceptions import *

def run(utils):

    bug='85327'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    file="/etc/cron.d/glite-wms-wmproxy.restart.cron"

    utils.log_info("Get file %s from remote host"%(file))

    utils.ssh_get_file(ssh,file,"%s/glite-wms-wmproxy.restart.cron_local"%(utils.get_tmp_dir()))
  
    utils.log_info("Check if it contains the setting of HOSTNAME before the graceful restarting of wmproxy service")

    F=open("%s/glite-wms-wmproxy.restart.cron_local"%(utils.get_tmp_dir()))
    lines=F.readlines()
    F.close()

    ok=0

    for line in lines:

      if line.find("HOSTNAME=%s"%(utils.get_WMS()))!=-1:
         ok=1

    
    if ok==1:
         utils.log_info("Test OK, there is the HOSTNAME setting")
    else:
        ssh.close()
        utils.log_info("ERROR - Test failed: There is not the HOSTNAME setting")
        raise GeneralError("Test failed","Error !!! There is not the HOSTNAME setting")

    utils.log_info("Restart gLite service and check for warnings")

    stdin,stdout,stderr=ssh.exec_command("service gLite restart")

    errors=stderr.readlines()

    for line in errors:

       if line.find("[warn] PassEnv variable HOSTNAME was undefined")!=-1:
         ssh.close()
         utils.log_info("ERROR: Test failed - During the wmproxy restart we get the following warning: [warn] PassEnv variable HOSTNAME was undefined")
         raise GeneralError("Test failed","During the wmproxy restart we get the following warning: [warn] PassEnv variable HOSTNAME was undefined")

    utils.log_info("Test OK, restart gLite service without warning ([warn] PassEnv variable HOSTNAME was undefined)")

    ssh.close()

    utils.log_info("End of regression test for bug %s"%bug)
