#
# Bug: 67489
# Title: WMS needs cron job to kill stale GridFTP processes
# Link: https://savannah.cern.ch/bugs/?67489
#
#


from lib.Exceptions import *


def run(utils):

    bug='67489'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Check for kill-stale-ftp.cron file at /etc/cron.d")

    output=utils.execute_remote_cmd(ssh,"ls /etc/cron.d/")
    
    if output.find("kill-stale-ftp.cron")==-1:
        utils.close_ssh(ssh)
        utils.log_info("ERROR: Unable to find kill-stale-ftp.cron file at /etc/cron.d")
        raise GeneralError("Check for kill-stale-ftp.cron file at /etc/cron.d","Unable to find kill-stale-ftp.cron file at /etc/cron.d")
    else:
        utils.log_info("Check OK , file kill-stale-ftp.cron exists")

    utils.log_info("Check kill-stale-ftp.cron file")
    
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

    utils.log_info("Check if kill-stale-ftp.sh script file exists")

    utils.execute_remote_cmd(ssh,"ls -l %s"%(script))

    utils.log_info("Check OK")

    utils.log_info("Check kill-stale-ftp.log file")

    output=utils.execute_remote_cmd(ssh,"cat %s"%(log_file))

    if output.find("START")==-1 or output.find("READY")==-1:
        utils.close_ssh(ssh)
        utils.log_info("ERROR: Script kill-stale-ftp.sh seems not to be working")
        raise GeneralError("Check kill-stale-ftp.log file","Script kill-stale-ftp.sh seems not to be working")

    utils.log_info("Check OK")
    
    utils.close_ssh(ssh)
    
    utils.log_info("Test OK")
 
    utils.log_info("End of regression test for bug %s"%(bug))

