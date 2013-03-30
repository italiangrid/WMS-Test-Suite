#
# Bug:45883
# Title: Optimization of resubmission
# Link: https://savannah.cern.ch/bugs/?45883
#
#


from lib.Exceptions import *
from lib import Job_utils


def run(utils):

    bug='45883'

    utils.log_info("Start regression test for bug %s"%(bug))
    
    utils.use_external_jdl("%s.jdl"%(bug))

    utils.log_info("Get availabe CEs for job submission")

    result=utils.run_command("glite-wms-job-list-match %s -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    available_ces=[]
        
    for line in result.split("\n"):
       if line.find(" - ") !=-1 : 
          available_ces.append(line.split(" - ")[1].split(":")[0])

  
    utils.log_info("Submit job and wait to finish")

    JOBID=Job_utils.submit_wait_finish(utils,"")

    utils.log_info("Check job final stauts")

    utils.job_status(JOBID)

    if utils.get_job_status()=="Aborted":
        utils.log_info("Job status is Aborted")
    else:
        utils.log_info("ERROR: Job status is not Aborted")
        raise GeneralError("Check job status","Error !!! Job status is not Aborted")

    utils.log_info("Get the used CEs")

    result=utils.run_command("glite-wms-job-logging-info --event Match %s"%(JOBID))

    used_ces=[]

    for line in result.split("\n"):
       if line.find("Dest id") !=-1 :
         used_ces.append(line.split("=")[1].strip().split(":")[0])
         
    utils.log_info("Check the used CEs")

    z = set(available_ces) & set(used_ces)
  
    if len(available_ces)<=4:

         if len(z) != len(available_ces):         
            utils.log_info("ERROR: Resubmission did not use all the available CEs. Used only %s while available CEs was %s"%(len(z),len(available_ces)))
            raise GeneralError("","Error !!!. Resubmission did not use all the available CEs. Used only %d while available CEs was %d"%(len(z),len(available_ces)))
    
    else: 
         
         if len(z) != 4:
             utils.log_info("ERROR: Resubmission did not prefer different CEs. Used CEs %s while available CEs was %s"%(len(z),len(available_ces)))
             raise GeneralError("","Error !!!. Resubmission did not prefer different CEs. Used CEs %d while available CEs was %d"%(len(z),len(available_ces)))

    utils.log_info("TEST OK")  
 
    utils.log_info("End of regression test for bug %s"%(bug))

