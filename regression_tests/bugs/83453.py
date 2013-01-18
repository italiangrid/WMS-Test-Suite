#
# Bug: 83453
# Title: Deregistration of a proxy (2)
# Link: https://savannah.cern.ch/bugs/?83453
#
#

import logging

from libutils.Exceptions import *
from libutils import Job_utils

def run(utils):

    bug='83453'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Prepare jdl file for submission")

    Job_utils.prepare_collection_job(utils,utils.get_jdl_file(),"/cream-")

    logging.info("Submit collection job")

    JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg --collection %s/collection_jdls"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_tmp_dir()))

    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

    output=utils.run_command_continue_on_error("glite-wms-job-status -v 0 %s"%(JOBID))
 
    IDS=[]
     
    for line in output.split("\n"):
        if line.find("the Job :")!=-1:
             IDS.append(line.split("the Job :")[1].strip(" \n\t"))


    logging.info("Check file /var/log/messages")

    output=utils.execute_remote_cmd(ssh,"grep glite-proxy-renewd /var/log/messages" )

    for id in IDS[1:]:

        logging.info("Proxy registration for job %s"%(id))

        if output.find("of job %s has been registered as")==-1:
            ssh.close()
            logging.error("Unable to find proxy registration for job %s"%(id))
            utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))
            raise GeneralError("Check file /var/log/messages","Unable to find proxy registration for job %s"%(id))
        else:
           logging.info("Successful proxy registration for job %s"%(id))


    logging.info("Wait until job finished")

    utils.wait_until_job_finishes(JOBID)

    logging.info("Check again file /var/log/messages")

    output=utils.execute_remote_cmd(ssh,"grep glite-proxy-renewd /var/log/messages" )

    for id in IDS[1:]:

        logging.info("Proxy unregistration for job %s"%(id))

        if output.find("of job %s has been unregistered")==-1:
            ssh.close()
            logging.error("Unable to find proxy unregistration for job %s"%(id))
            raise GeneralError("Check file /var/log/messages","Unable to find proxy unregistration for job %s"%(id))
        else:
           logging.info("Successful proxy unregistration for job %s"%(id))
    
    
    ssh.close()

    logging.info("End of regression test for bug %s"%(bug))
