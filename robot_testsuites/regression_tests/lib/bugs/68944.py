#
# Bug:68944
# Title: Bug in ICE's start/stop script
# Link: https://savannah.cern.ch/bugs/?68944
#
#

from lib.Exceptions import *

def run(utils):

    bug='68944'

    pid_before=[]
    pid_after=[]

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    utils.log_info("Connect to WMS host %s"%(utils.get_WMS()))

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Get process ids of running instances of glite-wms-ice")

    result=utils.execute_remote_cmd(ssh,"ps ax")

    for line in result.split("\n"):
        if line.find("wms-ice")!=-1:
            pid_before.append(line.strip().split(" ")[0])

  
    utils.log_info("Restart the glite-wms-ice")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-ice restart")

    utils.log_info("Get again the process ids of running instances of glite-wms-ice")

    result=utils.execute_remote_cmd(ssh,"ps ax")

    for line in result.split("\n"):
        if line.find("wms-ice")!=-1:
            pid_after.append(line.strip().split(" ")[0])
   
    if len(pid_before)>0:
        
      if len(pid_before) != len(pid_after):
        utils.log_info("ERROR: Problem during ICE restart")
        raise GeneralError("","Error !!! Problem during ICE restart")

    utils.log_info("Before restart pids:%s"%(pid_before),"DEBUG")
    utils.log_info("After restart pids:%s"%(pid_after),"DEBUG")

    pid=set(pid_before)&set(pid_after)

    if len(pid) != 0:
      utils.log_info("ERROR: Problem during ICE restart")
      raise GeneralError("","Error !!! Problem during ICE restart")
    
    ssh.close()

    utils.log_info("End of regression test for bug %s"%bug)

