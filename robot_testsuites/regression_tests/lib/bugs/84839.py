#
# Bug: 84839
# Title: Last LB event logged by ICE when job aborted for proxy expired should be ABORTED
# Link: https://savannah.cern.ch/bugs/?84839
#
#


from lib.Exceptions import *


def run(utils):

    bug='84839'

    utils.log_info("Start regression test for bug %s"%(bug))

    if utils.PROXY_PASSWORD=='' or utils.WMS_USERNAME=="" or utils.WMS_PASSWORD=="":
       utils.log_info("ERROR: Please set the required variables PROXY_PASSWORD , WMS_USERNAME and WMS_PASSWORD in test's configuration file")
       raise GeneralError("Missing required configuration attribute","Please set the required variables PROXY_PASSWORD , WMS_USERNAME and WMS_PASSWORD in test's configuration file")

    utils.log_info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_long_jdl(utils.get_jdl_file())
    utils.change_jdl_attribute(utils.get_jdl_file(),"MyProxyServer","\"\"")
    utils.set_destination_ce(utils.get_jdl_file(),"/cream-")

    utils.log_info("Create a short proxy, valid for 4 minutes")

    utils.run_command("echo %s | voms-proxy-init --voms %s --valid 00:14 -pwstdin"%(utils.PROXY_PASSWORD,utils.VO))

    utils.log_info("Submit the job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Create a long proxy")

    utils.run_command("echo %s | voms-proxy-init --voms %s -pwstdin "%(utils.PROXY_PASSWORD,utils.VO))

    utils.log_info("Wait until job finishes")

    utils.wait_until_job_finishes(JOBID)

    utils.log_info("Check job stauts and status reason")

    output=utils.run_command("glite-wms-job-status %s"%(JOBID)).split("\n")

    status=""
    reason=""

    for line in output:
        if line.find("Current Status:")!=-1:
            status=line.split("Current Status:")[1].strip(" \n\t")
        if line.find("Status Reason:")!=-1:
            reason=line.split("Status Reason:")[1].strip(" \n\t")

    if utils.get_job_status().find("Aborted")!=-1:
        utils.log_info("Test OK , job failed as expected due to proxy expiration")
    else:
        utils.log_info("ERROR: Wrong job status or status reason. Status %s Reason %s"%(status,reason))
        raise GeneralError("Check job status","Wrong job status or status reason. Status %s Reason %s"%(status,reason))

    utils.log_info("Check if last LB event logged by ICE is ABORTED")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.ssh_get_file(ssh, "/var/log/wms/ice.log","%s/local_ice.log"%(utils.get_tmp_dir()))

    utils.close_ssh(ssh)

    FILE=open("%s/local_ice.log"%(utils.get_tmp_dir()))
    lines=FILE.readlines()
    FILE.close()
   
    job_lines=[]

    for line in lines:
        if line.find(JOBID)!=-1:
            job_lines.append(line)

    target=""

    for line in job_lines:
        if line.find("Job Aborted Event")!=-1:
            target=line
            break

    if len(target)>0:
        utils.log_info("Last LB event logged by ICE when job aborted due to proxy expiration is ABORTED as expected")
        utils.log_info("Log info from ice.log: %s"%(target))
    else:
        utils.log_info("ERROR: Last LB event logged by ICE when job aborted due to proxy expiration isn't ABORTED")
        raise GeneralError("Check last LB event logged by ICE","Last LB event logged by ICE when job aborted due to proxy expiration isn't ABORTED")

    utils.log_info("End of regression test for bug %s"%(bug))
