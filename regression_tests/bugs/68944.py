#
# Bug:68944
# Title: Bug in ICE's start/stop script
# Link: https://savannah.cern.ch/bugs/?68944
#
#


import logging

from libutils.Exceptions import *

def run(utils):

    bug='68944'

    pid_before=[]
    pid_after=[]

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    logging.info("Connect to WMS host %s"%(utils.get_WMS()))

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Get process ids of running instances of glite-wms-ice")

    result=utils.execute_remote_cmd(ssh,"ps aux")

    for line in result.split("\n"):
        if line.find("wms-ice")!=-1:
            pid_before.append(line.split(" ")[5])

  
    logging.info("Restart the glite-wms-ice")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-ice restart")

    logging.info("Get again the process ids of running instances of glite-wms-ice")

    result=utils.execute_remote_cmd(ssh,"ps aux")

    for line in result.split("\n"):
        if line.find("wms-ice")!=-1:
            pid_after.append(line.split(" ")[5])
   

    if len(pid_before)>0:
        
      if len(pid_before) != len(pid_after):
        logging.error("Problem during ICE restart")
        raise GeneralError("","Error !!! Problem during ICE restart")


    pid=set(pid_before)&set(pid_after)

    if len(pid) != 0:
      logging.error("Problem during ICE restart")
      raise GeneralError("","Error !!! Problem during ICE restart")
    
    ssh.close()

    logging.info("End of regression test for bug %s",bug)
