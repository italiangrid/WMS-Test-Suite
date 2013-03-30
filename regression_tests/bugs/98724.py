#
# Bug: 98724
# Title: ICE removes its pid file at the start() instead of stop()
# Link: https://savannah.cern.ch/bugs/?98724
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='98724'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())
  
    logging.info("Stop ice service")
 
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-ice stop")

    logging.info("Check for ice related processes")

    ice_pids=[]

    output=utils.execute_remote_cmd(ssh,"ps -ef | grep ice")

    for line in output.split("\n"):
      if line.find("glite-wms-ice")!=-1 and len(line)>0:
          ice_pids.append(line)

    if len(ice_pids)==0:
        logging.info("There are no ice related processes as expected")
    else:
        utils.close_ssh(ssh)
        logging.error("There are ice related processes")
        raise GeneralError("Check for ice related processes after stopping ice","There are ice related processes")

    logging.info("Start ice service")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-ice start")

    logging.info("Check for related processes")

    ice_pids=[]

    output=utils.execute_remote_cmd(ssh,"ps -ef | grep ice")

    for line in output.split("\n"):
      if line.find("glite-wms-ice")!=-1 and len(line)>0:
          ice_pids.append(line)

    if len(ice_pids)>0:
        logging.info("There are ice related processes as expected")
    else:
        utils.close_ssh(ssh)
        logging.error("Unable to find ice related processes")
        raise GeneralError("Check for ice related processes after starting ice","Unable to find ice related processes")

    logging.info("Check for the pid file")

    utils.execute_remote_cmd(ssh,"ls -l /var/run/glite-wms-ice-safe.pid")

    logging.info("Pid file glite-wms-ice-safe.pid is in /var/run directory")

    logging.info("Stop ice service")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-ice stop")

    logging.info("Check for related processes")

    ice_pids=[]

    output=utils.execute_remote_cmd(ssh,"ps -ef | grep ice")

    for line in output.split("\n"):
      if line.find("glite-wms-ice")!=-1 and len(line)>0:
          ice_pids.append(line)

    if len(ice_pids)==0:
        logging.info("There are no ice related processes as expected")
    else:
        utils.close_ssh(ssh)
        logging.error("There are ice related processes")
        raise GeneralError("Check for ice related processes after stopping ice","There are ice related processes")


    logging.info("Check for the pid file")

    utils.execute_remote_cmd_fail(ssh,"ls -l /var/run/glite-wms-ice-safe.pid")

    logging.info("Pid file glite-wms-ice-safe.pid has been removed from its directory as expected")

    utils.close_ssh(ssh)

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))

