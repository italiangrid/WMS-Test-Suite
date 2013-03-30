#
# Bug: 92657
# Title: some sensible information should be logged on syslog
# Link: https://savannah.cern.ch/bugs/?92657
#
#

import socket
import time

from lib.Exceptions import *


def run(utils):

    bug='92657'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Prepare jdl file for submission")

    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())

    utils.log_info("Submit a job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    UI=socket.gethostname()

    output=utils.run_command("voms-proxy-info -all").split("extension information ===")[1].split("\n")
      
    DN=''
    FQAN=''

    for line in output:

        if line.find("subject")!=-1:
            DN=line.split(":")[1].strip(" \n\t")

        if line.find("attribute")!=-1:
            FQAN=line.split(":")[1].strip(" \n\t")


    utils.log_info("Wait until job matched")

    utils.job_status(JOBID)

    while utils.get_job_status()=="Waiting" or utils.get_job_status()=="Ready":
        time.sleep(30)
        utils.job_status(JOBID)


    output=utils.run_command("glite-wms-job-status %s"%(JOBID)).split("\n")

    CE=''

    for line in output:
        if line.find("Destination:")!=-1:
            CE=line.split("Destination:")[1].strip(" \t\n")
            break

    utils.log_info("Get syslog file")

    utils.ssh_get_file(ssh,"/var/log/messages","%s/local_copy"%(utils.get_tmp_dir()))

    utils.close_ssh(ssh)

    FILE=open("%s/local_copy"%(utils.get_tmp_dir()))
    lines=FILE.readlines()
    FILE.close()

    wmproxy=''
    workload=''

    for line in lines:

        if line.find(JOBID)!=-1 and line.find("glite_wms_wmproxy_server"):
            wmproxy=line

        if line.find(JOBID)!=-1 and line.find("glite-wms-workload_manager"):
            workload=line

    utils.log_info("Check if WMProxy logged the relevant information (UI's hostname,DN,FQAN,Jobid)")

    if wmproxy.find("submission from %s"%(UI))==-1 or wmproxy.find("DN=%s"%(DN))==-1 or wmproxy.find("FQAN=%s"%(FQAN))==-1 or wmproxy.find("jobid=%s"%(JOBID))==-1 :
       utils.log_info("ERROR: Unable to find all the relevant information. Get %s"%(wmproxy))
       raise GeneralError("Check if WMProxy logged the relevant information (UI's hostname,DN,FQAN)","Unable to find all the relevant information")
    else:
       utils.log_info("Check OK , find all relevant information")


    utils.log_info("Check if workload manager logged the relevant information (Jobid,Destination)")

    if workload.find("jobid=%s"%(JOBID))==-1 or workload.find("destination %s"%(CE))==-1 :
       utils.log_info("ERROR: Unable to find all the relevant information. Get %s"%(workload))
       raise GeneralError("Check if workload manager logged the relevant information (Jobid,Destination)","Unable to find all the relevant information")
    else:
       utils.log_info("Check OK , find all relevant information")

    utils.log_info("End of regression test for bug %s"%(bug))
