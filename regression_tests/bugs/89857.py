#
# Bug: 89857
# Title: Wrong location for PID file
# Link: https://savannah.cern.ch/bugs/?89857
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='89857'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    pid_files=[
        '/var/run/glite-wms-job_controller.pid',
        '/var/run/glite-wms-log_monitor.pid',
        '/var/run/condor_master.pid',
        '/var/run/glite-wms-ice-safe.pid',
        '/var/run/glite-wms-workload_manager.pid'
    ]

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Check if all WMS related pid files are saved in /var/run directory")

    output=utils.execute_remote_cmd(ssh, "ls /var/run/*.pid")

    files=[]

    for file in output.split("\n"):
          file=file.strip(" \n\t")
          if len(file)>0:
             files.append(file)

    exist=set(files)&set(pid_files)
    missing=set(pid_files)-set(exist)

    if len(missing)==0:
        logging.info("Check OK, all WMS related pid files are saved in /var/run directory")
    else:
        utils.close_ssh(ssh)
        logging.error("Test failed, not all WMS related pid files are saved in /var/run directory")
        logging.error("Missing pid files: %s"%(' , ').join(missing))
        raise GeneralError("Check if all WMS related pid files are saved in /var/run directory","Test failed, not all WMS related pid files are saved in /var/run directory")

    logging.info("Check that /tmp directory does not contain WMS related pid files")

    output=utils.execute_remote_cmd(ssh, "ls /tmp/*.pid")

    tmp_files=[]
    files=[]
    
    for file in output.split("\n"):
          file=file.strip(" \n\t")
          if len(file)>0:
              tmp_files.append(file.split("/tmp/")[1])

    for file in pid_files:
         files.append(file.split("/var/run/")[1])

    exist_tmp=set(files)&set(tmp_files)
    
    if len(exist_tmp)>0:
        utils.close_ssh(ssh)
        logging.error("Test failed, there are WMS related pid files in /tmp directory")
        logging.error("Pid files: %s"%(' , '.join(exist_tmp)))
        raise GeneralError("Check that /tmp directory does not contain WMS related pid files","Test failed, there are WMS related pid files in /tmp directory")

    utils.close_ssh(ssh)

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
