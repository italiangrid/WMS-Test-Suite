#
# Bug: 67489
# Title: WMS needs cron job to kill stale GridFTP processes
# Link: https://savannah.cern.ch/bugs/?67489
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='67489'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Check for kill-stale-ftp.cron file at /etc/cron.d")

    output=utils.execute_remote_cmd(ssh,"ls /etc/cron.d/")
    
    if output.find("kill-stale-ftp.cron")==-1:
        utils.close_ssh(ssh)
        logging.error("Unable to find kill-stale-ftp.cron file at /etc/cron.d")
        raise GeneralError("Check for kill-stale-ftp.cron file at /etc/cron.d","Unable to find kill-stale-ftp.cron file at /etc/cron.d")
    else:
        logging.info("Check OK , file kill-stale-ftp.cron exists")

    logging.info("Check kill-stale-ftp.cron file")
    
    output=utils.execute_remote_cmd(ssh,"cat /etc/cron.d/kill-stale-ftp.cron")

    script=''
    log_file=''

    for line in output.split("\n"):
        if line.find("kill-stale-ftp.sh")!=-1:
           for part in line.split(" "):
               if part.find("kill-stale-ftp.sh")!=-1:
                   script=part.strip(" \n\t")
               if part.find("kill-stale-ftp.log")!=-1:
                   log_file=part.strip(" \n\t")

    logging.info("Check if kill-stale-ftp.sh script file exists")

    utils.execute_remote_cmd(ssh,"ls -l %s"%(script))

    logging.info("Check OK")

    logging.info("Check kill-stale-ftp.log file")

    output=utils.execute_remote_cmd(ssh,"cat %s"%(log_file))

    if output.find("START")==-1 or output.find("READY")==-1:
        utils.close_ssh(ssh)
        logging.error("Script kill-stale-ftp.sh seems not to be working")
        raise GeneralError("Check kill-stale-ftp.log file","Script kill-stale-ftp.sh seems not to be working")

    logging.info("Check OK")
    
    utils.close_ssh(ssh)
    
    logging.info("Test OK")
 
    logging.info("End of regression test for bug %s"%(bug))

