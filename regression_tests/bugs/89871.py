#
# Bug: 89871
# Title: WMS logs should keep track of the last 90 days
# Link: https://savannah.cern.ch/bugs/?89871
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='89871'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    logrotate_files=[
        '/etc/logrotate.d/glite-wms-purger',
        '/etc/logrotate.d/globus-gridftp',
        '/etc/logrotate.d/kill-stale-ftp',
        '/etc/logrotate.d/lcmaps',
        '/etc/logrotate.d/ice',
        '/etc/logrotate.d/jc',
        '/etc/logrotate.d/lm',
        '/etc/logrotate.d/wm',
        '/etc/logrotate.d/wmproxy',
        '/etc/logrotate.d/argus'
    ]

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Check if all WMS logs keep track of the last 90 days")

    output=utils.execute_remote_cmd(ssh, "grep -r rotate\ 90 /etc/logrotate.d")

    files_90=[]
    files_daily=[]
    
    for file in output.split("\n"):
          file=file.strip(" \n\t")
          if len(file)>0:
              files_90.append(file.split(":")[0])

    exist_90=set(files_90)&set(logrotate_files)
    missing_90=set(logrotate_files)-set(exist_90)

    if len(missing_90)==0:
        logging.info("Check OK, all WMS logs keep track of the last 90 days")
    else:
        utils.close_ssh(ssh)
        logging.error("Test failed, not all WMS logs keep track of the last 90 days")
        logging.error("Logs don't keep track of the last 90 days: %s"%(' , ').join(missing_90))
        raise GeneralError("Check tath WMS logs keep track of the last 90 days","Test failed, not all WMS logs keep track of the last 90 days")
    
    logging.info("Check if all WMS logs rotate daily")

    output=utils.execute_remote_cmd(ssh, "grep -r daily /etc/logrotate.d")

    for file in output.split("\n"):
          file=file.strip(" \n\t")
          if len(file)>0:
              files_daily.append(file.split(":")[0])

    exist_daily=set(files_daily)&set(logrotate_files)
    missing_daily=set(logrotate_files)-set(exist_daily)

    if len(missing_daily)>0:
        utils.close_ssh(ssh)
        logging.error("Test failed, not all WMS logs rotate daily")
        logging.error("Logs don't rotate daily: %s"%(' , '.join(missing_daily)))
        raise GeneralError("Check if all WMS logs rotate daily","Test failed, not all WMS logs rotate daily")
    
    utils.close_ssh(ssh)

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
