#
# Bug: 84839
# Title: Last LB event logged by ICE when job aborted for proxy expired should be ABORTED
# Link: https://savannah.cern.ch/bugs/?84839
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='84839'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you have to set the PROXY_PASSWORD,WMS_USERNAME and WMS_PASSWORD attributes at configuration file")

    if utils.PROXY_PASSWORD=='' or utils.WMS_USERNAME=="" or utils.WMS_PASSWORD=="":
       logging.warn("Please set the required variables PROXY_PASSWORD , WMS_USERNAME and WMS_PASSWORD in test's configuration file")
       raise GeneralError("Missing required configuration attribute","Please set the required variables PROXY_PASSWORD , WMS_USERNAME and WMS_PASSWORD in test's configuration file")

    logging.info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_long_jdl(utils.get_jdl_file())
    utils.change_jdl_attribute(utils.get_jdl_file(),"MyProxyServer","\"\"")
    utils.set_destination_ce(utils.get_jdl_file(),"/cream-")

    logging.info("Create a short proxy, valid for 4 minutes")

    utils.run_command_continue_on_error("echo %s | voms-proxy-init --voms %s --valid 00:14 -pwstdin"%(utils.PROXY_PASSWORD,utils.VO))

    logging.info("Submit the job")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Create a long proxy")

    utils.run_command_continue_on_error("echo %s | voms-proxy-init --voms %s -pwstdin "%(utils.PROXY_PASSWORD,utils.VO))

    logging.info("Wait until job finishes")

    utils.wait_until_job_finishes(JOBID)

    logging.info("Check job stauts and status reason")

    output=utils.run_command_continue_on_error("glite-wms-job-status %s"%(JOBID)).split("\n")

    status=""
    reason=""

    for line in output:
        if line.find("Current Status:")!=-1:
            status=line.split("Current Status:")[1].strip(" \n\t")
        if line.find("Status Reason:")!=-1:
            reason=line.split("Status Reason:")[1].strip(" \n\t")

    if utils.get_job_status().find("Aborted")!=-1:
        logging.info("Test OK , job failed as expected due to proxy expiration")
    else:
      logging.error("Wrong job status or status reason. Status %s Reason %s"%(status,reason))
      raise GeneralError("Check job status","Wrong job status or status reason. Status %s Reason %s"%(status,reason))

    logging.info("Check if last LB event logged by ICE is ABORTED")

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
        logging.info("Last LB event logged by ICE when job aborted due to proxy expiration is ABORTED as expected")
        logging.info("Log info from ice.log: %s"%(target))
    else:
       logging.error("Last LB event logged by ICE when job aborted due to proxy expiration isn't ABORTED")
       raise GeneralError("Check last LB event logged by ICE","Last LB event logged by ICE when job aborted due to proxy expiration isn't ABORTED")


    logging.info("End of regression test for bug %s"%(bug))
