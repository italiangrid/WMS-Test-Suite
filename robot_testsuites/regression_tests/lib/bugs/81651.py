#
# Bug: 81651
# Title: Cancellation of a dag's node doesn't work
# Link: https://savannah.cern.ch/bugs/?81651
#
#


import time

from lib.Exceptions import *


def run(utils):

    bug='81651'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_dag_jdl(utils.get_jdl_file())

    utils.log_info("Submit the job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("For each DAG node get its job id")

    output=utils.run_command("glite-wms-job-status %s"%(JOBID))

    NODE_JOBIDS=[]

    for line in output.split("\n"):
        if line.find("Status info for the Job :")!=-1 and line.find(JOBID)==-1:
            id=line.split("Status info for the Job :")[1]
            utils.log_info("Find job id: %s"%(id.strip(" \n\t")))
            NODE_JOBIDS.append(id.strip(" \t\n"))

    utils.log_info("Wait until some node is running")

    counter=0
    CANCEL_JOBID=""

    while len(CANCEL_JOBID)==0 and counter < 6:

      for node_id in NODE_JOBIDS:
            
          utils.log_info("Check status for node: %s"%(node_id))
          utils.job_status(node_id)

          if utils.get_job_status()=="Running":
             CANCEL_JOBID=node_id
             utils.log_info("Find running node: %s"%(node_id))
             break

      counter+=1
      utils.log_info("Wait 60 seconds before the next try. (%s/6)"%(counter))
      time.sleep(60)


    if len(CANCEL_JOBID)>0:

        utils.log_info("Cancel running node: %s"%(CANCEL_JOBID))

        utils.run_command("glite-wms-job-cancel --noint %s"%(CANCEL_JOBID))

        utils.log_info("Check node final status")

        utils.job_status(CANCEL_JOBID)

        utils.log_info("Try to check the status 6 times (for a total of 420 seconds)")

        i=0

        while ( utils.get_job_status().find("Cancelled")==-1 and i<6) :

            if utils.job_is_finished(jobid) :
                logging.error("ERROR: Job %s final status is: %s."%(CANCEL_JOBID,utils.get_job_status()))
                raise GeneralError("Check job status","Job status is wrong: %s"%(utils.get_job_status()))

            i+=1
            time.sleep(i*20)
            utils.log_info("Wait %s seconds for the next try"%(i*5))
            utils.job_status(CANCEL_JOBID)

        if utils.job_is_finished(CANCEL_JOBID) != 3:
            logging.error("ERROR: Job's %s status is wrong: %s"%(CANCEL_JOBID,utils.get_job_status()))
            raise GeneralError("Check job status","Job's status is wrong: %s"%(utils.get_job_status()))
        else:
            utils.log_info("Job's %s final status is Cancelled as expected")

    else:
        logging.error("ERROR: Waiting 6 minutes but unable to find a running node")
        raise GeneralError("Check for running node","Waiting 6 minutes but unable to find a running node")

    utils.log_info("End of regression test for bug %s"%(bug))

