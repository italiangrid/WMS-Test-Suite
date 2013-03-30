#
# Bug: 95584
# Title: glite-wms-ice-proxy-renew can block undefinitely
# Link: https://savannah.cern.ch/bugs/?95584
#
#

import logging

from time import strftime
from libutils.Exceptions import *


def run(utils):

    bug='95584'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you have to set the PROXY_PASSWORD attribute for user proxy password at configuration file")

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    if utils.PROXY_PASSWORD=='':
       logging.warn("Please set the required variable PROXY_PASSWORD in test's configuration file")
       raise GeneralError("Missing required configuration attribute","Please set the required variable PROXY_PASSWORD in test's configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Set logging level for ICE to debug (700)")

    utils.change_attribute_at_remote_file_section(ssh, "/etc/glite-wms/glite_wms.conf","ice_log_level","ICE","700")

    logging.info("Check for ICE configuration proxy_renewal_timeout parameter in the glite_wms.conf file")

    output=utils.execute_remote_cmd(ssh,"grep proxy_renewal_timeout /etc/glite-wms/glite_wms.conf")
    
    if len(output)==0:
        logging.info("Unable to find ICE cofiguration proxy_renewal_timeout parameter in the glite_wms.conf file. Use default value 120 secs")
        timeout=120
    else:
        logging.info("Find the following parameter: %s"%(output))
        output=output.split("=")[1]
        output=output.strip(" \n\n;")
        timeout=int(output)

    logging.info("Stop ICE service")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-ice stop")

    logging.info("Backup the existing ICE log file")

    utils.execute_remote_cmd(ssh,"mv /var/log/wms/ice.log /var/log/wms/ice.log_%s"%(strftime("%Y%m%d%H%M%S")))

    logging.info("Start ICE service")
    
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-ice start")

    logging.info("Prepare jdl file for submission")

    utils.use_external_jdl("%s.jdl"%(bug))

    logging.info("Create a short proxy, valid for 10 minutes")

    utils.run_command_continue_on_error("echo %s | voms-proxy-init --voms %s --valid 00:10 -pwstdin"%(utils.PROXY_PASSWORD,utils.VO))

    logging.info("Submit the job")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Create a long proxy")

    utils.run_command_continue_on_error("echo %s | voms-proxy-init --voms %s -pwstdin "%(utils.PROXY_PASSWORD,utils.VO))

    logging.info("Wait until job finishes")

    utils.wait_until_job_finishes(JOBID)

    logging.info("Check ice log file")

    utils.ssh_get_file(ssh, "/var/log/wms/ice.log","%s/ice.log"%(utils.get_tmp_dir()))

    utils.close_ssh(ssh)

    FILE=open("%s/ice.log"%(utils.get_tmp_dir()))
    lines=FILE.readlines()
    FILE.close()

    ice_log=' '.join(lines)

    message="iceCommandDelegationRenewal::renewAllDelegations() - Proxy renewal failed: [ERROR - /usr/bin/glite-wms-ice-proxy-renew"
            
    if ice_log.find(message)!=-1:
        logging.info("The renewal child has been killed after timeout of %s seconds as expected"%(timeout))
    else:
        logging.error("The renewal child hasn't been killed after timeout of %s seconds as expected"%(timeout))
        raise GeneralError("Check ICE log file","The renewal child hasn't been killed after timeout of %s seconds as expected"%(timeout))

    logging.info("Check job stauts")

    utils.job_status(JOBID)

    if utils.get_job_status().find("Aborted")!=-1:
        logging.info("Test OK , job aborted")
    else:
        logging.error("Job status is not Aborted")
        raise GeneralError("Check job status","Job status is not Aborted")


    logging.info("End of regression test for bug %s"%(bug))

