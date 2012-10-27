#
# Bug:91486
# Title: WMS: use logrotate uniformly in ice,lm,jc,wm,wmp
# Link: https://savannah.cern.ch/bugs/?91486
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='91486'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    logrotate_files=[
        'glite-wms-purger',
        'ice',
        'jc',
        'lm',
        'wm',
        'wmproxy'
    ]

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Search /etc/cron.d directory for logrotate related files")

    output=utils.execute_remote_cmd(ssh, "grep -r rotate /etc/cron.d")

    if len(output)==0:
        logging.info("Check OK, /etc/cron.d does not contain any logrotate related file")
    else:
        utils.close_ssh(ssh)
        logging.error("Test failed, find logrotate related files")
        logging.error("Details: \n%s"%(output))
        raise GeneralError("Search /etc/cron.d directory for logrotate related files","Test failed, find logrotate related files: %s"%(output))
    
    logging.info("Search /etc/logrotate.d directory for logrotate related files")

    output=utils.execute_remote_cmd(ssh, "ls /etc/logrotate.d/")

    utils.close_ssh(ssh)

    files=output.split(" ")

    for file in files:
        files[files.index(file)]=file.strip(" \n\t")

    exist=set(files)&set(logrotate_files)

    missing=set(logrotate_files)-set(exist)

    if len(missing)>0:
        logging.error("Test failed, unable to find all the expected logrotate files at /etc/logrotate.d")
        logging.error("Missing files: %s"%(','.join(missing)))
        raise GeneralError("Search /etc/logrotate.d directory for logrotate related files","Test failed, unable to find all the expected logrotate files at /etc/logrotate.d")

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
