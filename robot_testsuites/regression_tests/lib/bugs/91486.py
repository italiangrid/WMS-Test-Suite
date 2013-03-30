#
# Bug:91486
# Title: WMS: use logrotate uniformly in ice,lm,jc,wm,wmp
# Link: https://savannah.cern.ch/bugs/?91486
#
#

from lib.Exceptions import *


def run(utils):

    bug='91486'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")


    logrotate_files=[
        'glite-wms-purger',
        'ice',
        'jc',
        'lm',
        'wm',
        'wmproxy'
    ]

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Search /etc/cron.d directory for logrotate related files")

    output=utils.execute_remote_cmd(ssh, "grep -r rotate /etc/cron.d")

    if len(output)==0:
        utils.log_info("Check OK, /etc/cron.d does not contain any logrotate related file")
    else:
        utils.close_ssh(ssh)
        utils.log_info("ERROR: Test failed, find logrotate related files")
        utils.log_info("ERROR: Details: \n%s"%(output))
        raise GeneralError("Search /etc/cron.d directory for logrotate related files","Test failed, find logrotate related files: %s"%(output))
    
    utils.log_info("Search /etc/logrotate.d directory for logrotate related files")

    output=utils.execute_remote_cmd(ssh, "ls /etc/logrotate.d/")

    utils.close_ssh(ssh)

    files=output.split(" ")

    for file in files:
        files[files.index(file)]=file.strip(" \n\t")

    exist=set(files)&set(logrotate_files)

    missing=set(logrotate_files)-set(exist)

    if len(missing)>0:
        utils.log_info("ERROR: Test failed, unable to find all the expected logrotate files at /etc/logrotate.d")
        utils.log_info("ERROR: Missing files: %s"%(','.join(missing)))
        raise GeneralError("Search /etc/logrotate.d directory for logrotate related files","Test failed, unable to find all the expected logrotate files at /etc/logrotate.d")

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))
