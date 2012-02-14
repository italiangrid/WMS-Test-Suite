#
# Bug: 85327
# Title: [yaim-wms] glite-wms-wmproxy.restart.cron missing HOSTNAME environment variable
# Link: https://savannah.cern.ch/bugs/?85327
#
#


import logging

from libutils.Exceptions import *

def run(utils):

    bug='85327'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    file="/etc/cron.d/glite-wms-wmproxy.restart.cron"

    logging.info("Get file %s from remote host"%(file))

    utils.ssh_get_file(ssh,file,"%s/glite-wms-wmproxy.restart.cron_local"%(utils.get_tmp_dir()))
  
    logging.info("Check if it contains the setting of HOSTNAME before the graceful restarting of wmproxy service")

    F=open("%s/glite-wms-wmproxy.restart.cron_local"%(utils.get_tmp_dir()))
    lines=F.readlines()
    F.close()

    ok=0

    for line in lines:

      if line.find("HOSTNAME=%s"%(utils.get_WMS()))!=-1:
         ok=1

    
    if ok==1:
         logging.info("Test OK, there is the HOSTNAME setting")
    else:
        ssh.close()
        logging.error("Test failed: There is not the HOSTNAME setting")
        raise GeneralError("Test failed","Error !!! There is not the HOSTNAME setting")

    logging.info("Restart gLite service and check for warnings")

    stdin,stdout,stderr=ssh.exec_command("service gLite restart")

    errors=stderr.readlines()

    for line in errors:

       if line.find("[warn] PassEnv variable HOSTNAME was undefined")!=-1:
         ssh.close()
         logging.error("Test failed: During the wmproxy restart we get the following warning: [warn] PassEnv variable HOSTNAME was undefined")
         raise GeneralError("Test failed","During the wmproxy restart we get the following warning: [warn] PassEnv variable HOSTNAME was undefined")

    logging.info("Test OK, restart gLite service without warning ([warn] PassEnv variable HOSTNAME was undefined)")

    ssh.close()

    logging.info("End of regression test for bug %s",bug)
