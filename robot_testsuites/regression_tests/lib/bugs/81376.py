#
# Bug: 81376
# Title: glite-wms-wmproxy.restart.cron MUST support graceful wmp restart
# Link: https://savannah.cern.ch/bugs/?81376
#
#


from lib.Exceptions import *

def run(utils):

    bug='81376'

    utils.log_info("Start regression test for bug %s"%(bug))
  
    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    file="/etc/cron.d/glite-wms-wmproxy.restart.cron"

    utils.log_info("Get file %s from remote host"%(file))

    utils.ssh_get_file(ssh,file,"%s/glite-wms-wmproxy.restart.cron_local"%(utils.get_tmp_dir()))

    ssh.close()

    utils.log_info("Check if command (/etc/init.d/glite-wms-wmproxy) use the graceful option")

    F=open("%s/glite-wms-wmproxy.restart.cron_local"%(utils.get_tmp_dir()))
    lines=F.readlines()
    F.close()

    ok=0

    for line in lines:

      if line.find("/etc/init.d/glite-wms-wmproxy graceful")!=-1:
         ok=1

    
    if ok==1:
         utils.log_info("Test OK, Graceful option is found")
    else:
        utils.log_info("ERROR: Test failed - Command does not use the graceful option ")
        raise GeneralError("Test failed","Error !!! Command does not use the graceful option")
    
    utils.log_info("End of regression test for bug %s"%(bug))
