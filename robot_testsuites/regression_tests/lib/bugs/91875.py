#
# Bug: 91875
# Title: EMI WMS does not use grid_monitor
# Link: https://savannah.cern.ch/bugs/?91875
#
#

import time

from lib.Exceptions import *


def run(utils):

    bug='91875'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Get last access date for script /opt/lcg/sbin/grid_monitor.sh before submission")

    output=utils.execute_remote_cmd(ssh, "ls -lu --time-style=full-iso `locate grid_mon`")

    before_access=''

    for line in output.split("\n"):
        if line.find("/opt/lcg/sbin/grid_monitor.sh")!=-1 and line.find("/usr/sbin/grid_monitor.sh")==-1:
            before_access=line

    if len(before_access)==0:
        utils.log_info("ERROR: Unable to find script /opt/lcg/sbin/grid_monitor.sh")
        raise GeneralError("Check if script /opt/lcg/sbin/grid_monitor.sh has been used during the job submission","Unable to find script /opt/lcg/sbin/grid_monitor.sh")

    utils.log_info("Wait 10 secs")
    time.sleep(10)

    utils.log_info("Submit a job to GRAM CE")

    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())
    utils.set_destination_ce(utils.get_jdl_file(),"2119/jobmanager")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.job_status(JOBID)

    while utils.get_job_status().find("Ready")!=-1 or utils.get_job_status().find("Waiting")!=-1:
        utils.log_info("Wait 30 secs")
        time.sleep(30)
        utils.job_status(JOBID)

    utils.log_info("Get last access date for script /opt/lcg/sbin/grid_monitor.sh after submission")

    output=utils.execute_remote_cmd(ssh, "ls -lu  --time-style=full-iso `locate grid_mon`")

    utils.close_ssh(ssh)
    
    after_access=''

    for line in output.split("\n"):
        if line.find("/opt/lcg/sbin/grid_monitor.sh")!=-1 and line.find("/usr/sbin/grid_monitor.sh")==-1:
            after_access=line

    for value in before_access.split(" "):
        if value.find(":")!=-1:
            before_time=value.split(".")[0]

        if value.find("-")!=-1 and value.find("->")==-1:
            before_date=value

    for value in after_access.split(" "):
        if value.find(":")!=-1:
            after_time=value.split(".")[0]

        if value.find("-")!=-1 and value.find("->")==-1:
            after_date=value

    before=time.mktime(time.strptime("%s %s"%(before_date,before_time),"%Y-%m-%d %H:%M:%S"))
    after=time.mktime(time.strptime("%s %s"%(after_date,after_time),"%Y-%m-%d %H:%M:%S"))
 
    utils.log_info("Check if script /opt/lcg/sbin/grid_monitor.sh has been used during the job submission")

    if after>before:
        utils.log_info("Check OK, script /opt/lcg/sbin/grid_monitor.sh has been used during the job submission")
    else:
        utils.log_info("ERROR: Test failed, script /opt/lcg/sbin/grid_monitor.sh hasn't been used during the job submission")
        utils.log_info("ERROR: Access details before submission: %s %s"%(before_date,before_time))
        utils.log_info("ERROR: Access details after submission: %s %s"%(after_date,after_time))
        raise GeneralError("Check if script /opt/lcg/sbin/grid_monitor.sh has been used during the job submission","Test failed, script /opt/lcg/sbin/grid_monitor.sh hasn't been used during the job submission")
    
    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))
