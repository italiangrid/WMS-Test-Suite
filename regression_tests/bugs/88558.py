#
# Bug:88558
# Title: WM creates submit requests with old sequence code upon a replan
# Link: https://savannah.cern.ch/bugs/?88558
#
#

import logging
import time

from libutils.Exceptions import *

def get_source(data):

    source=''

    for line in data.split("\n"):
        if line.find("- Source")!=-1:
            source=line.split("=")[1].strip(" \t\n")
            break
            
    return source

def get_enqueued_with_jdl_logged(data):

     enqueued=[]

     for info in data:
        if get_source(info).find("WorkloadManager")!=-1:
            if info.find("- Job")!=-1:
              enqueued.append(info)

     return enqueued


def job_is_replanned(utils,jobid):

    logging.info("Check if job %s has been replanned"%(jobid))

    result=utils.run_command_continue_on_error("glite-wms-job-logging-info %s"%(jobid))

    if result.find("Event: Resubmission")!=-1:
                   
      logging.info("Find Event: Resubmission for job %s"%(jobid))

      output=utils.run_command_continue_on_error("glite-wms-job-logging-info -v 2 --event Resubmission %s"%(jobid))

      for line in output.split("\n"):
         if line.find("SHALLOW")!=-1:
           logging.info("Job %s has been replanned"%(jobid))
           return 1

    return 0


def wait_until_job_replanned(utils,jobid):

    logging.info("Iterating %s times and each time wait for %s secs",utils.NUM_STATUS_RETRIEVALS,utils.SLEEP_TIME)

    counter=0

    while job_is_replanned(utils,jobid) == 0 :

       if counter >= int(utils.NUM_STATUS_RETRIEVALS) :
            logging.error("Timeout reached while waiting the job %s to finish",jobid)
            raise TimeOutError("","Timeout reached while waiting the job %s to replan"%(jobid))

       logging.info("Job's %s has not replanned sleeping %s seconds ( %s/%s )",jobid,utils.SLEEP_TIME,counter,utils.NUM_STATUS_RETRIEVALS)
       time.sleep(int(utils.SLEEP_TIME))
       counter=counter+1



def run(utils):

    bug='88558'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_shallow_jdl(utils.get_jdl_file())
    
    logging.info("Submit job which triggers a replan")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Wait until job has been replanned")

    wait_until_job_replanned(utils,JOBID)

    logging.info("Get all the enqueued events for job %s"%(JOBID))

    output=utils.run_command_continue_on_error("glite-wms-job-logging-info -v 3 --event Enqueued %s"%(JOBID)).split("\t---")

    logging.info("Find the enqueued events with source WorkloadManager which also have jdl logged information")
    
    enqueued=get_enqueued_with_jdl_logged(output)

    seqcode=''
    LB_seqcode=''

    for info in enqueued:

       logging.info("For such enqueued event check that the LB_sequence_code is the same with the sequence code used to logged the event")

       for line in info.split("\n"):

           if line.find("- Seqcode")!=-1:
               seqcode=line.split( "= ")[1].strip(" \t\n")
               logging.info("Get the value of the sequence code in the event: %s"%(seqcode))

           if line.find("LB_sequence_code = ")!=-1:
               LB_seqcode=line.split(" = ")[1].strip(" ;\t\n\"")
               logging.info("Get the value of the LB_seqcode in the logged jdl: %s"%(LB_seqcode))

       if seqcode!='' and seqcode!=LB_seqcode:
           raise GeneralError("Check LB_sequence_code and event sequence code","Error !!! The LB_sequence_code is not the same with the sequence code used to logged the event")
       else:
           logging.info("Check OK. LB_seqcode in the logged jdl is the same with the event sequence code")
           seqcode=''
           LB_seqcode=''

    logging.info("Test OK")

    logging.info("End of regression test for bug %s"%(bug))
