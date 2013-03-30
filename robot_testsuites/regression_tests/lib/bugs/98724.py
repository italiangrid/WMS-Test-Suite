#
# Bug: 98724
# Title: ICE removes its pid file at the start() instead of stop()
# Link: https://savannah.cern.ch/bugs/?98724
#
#


from lib.Exceptions import *


def run(utils):

    bug='98724'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())
  
    utils.log_info("Stop ice service")
 
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-ice stop")

    utils.log_info("Check for ice related processes")

    ice_pids=[]

    output=utils.execute_remote_cmd(ssh,"ps -ef | grep ice")

    for line in output.split("\n"):
      if line.find("glite-wms-ice")!=-1 and len(line)>0:
          ice_pids.append(line)

    if len(ice_pids)==0:
        utils.log_info("There are no ice related processes as expected")
    else:
        utils.close_ssh(ssh)
        utils.log_info("ERROR: There are ice related processes")
        raise GeneralError("Check for ice related processes after stopping ice","There are ice related processes")

    utils.log_info("Start ice service")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-ice start")

    utils.log_info("Check for related processes")

    ice_pids=[]

    output=utils.execute_remote_cmd(ssh,"ps -ef | grep ice")

    for line in output.split("\n"):
      if line.find("glite-wms-ice")!=-1 and len(line)>0:
          ice_pids.append(line)

    if len(ice_pids)>0:
        utils.log_info("There are ice related processes as expected")
    else:
        utils.close_ssh(ssh)
        utils.log_info("ERROR: Unable to find ice related processes")
        raise GeneralError("Check for ice related processes after starting ice","Unable to find ice related processes")

    utils.log_info("Check for the pid file")

    utils.execute_remote_cmd(ssh,"ls -l /var/run/glite-wms-ice-safe.pid")

    utils.log_info("Pid file glite-wms-ice-safe.pid is in /var/run directory")

    utils.log_info("Stop ice service")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-ice stop")

    utils.log_info("Check for related processes")

    ice_pids=[]

    output=utils.execute_remote_cmd(ssh,"ps -ef | grep ice")

    for line in output.split("\n"):
      if line.find("glite-wms-ice")!=-1 and len(line)>0:
          ice_pids.append(line)

    if len(ice_pids)==0:
        utils.log_info("There are no ice related processes as expected")
    else:
        utils.close_ssh(ssh)
        utils.log_info("ERROR: There are ice related processes")
        raise GeneralError("Check for ice related processes after stopping ice","There are ice related processes")


    utils.log_info("Check for the pid file")

    utils.execute_remote_cmd_fail(ssh,"ls -l /var/run/glite-wms-ice-safe.pid")

    utils.log_info("Pid file glite-wms-ice-safe.pid has been removed from its directory as expected")

    utils.close_ssh(ssh)

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))

