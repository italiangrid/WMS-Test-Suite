#
# Bug:28235
# Title: Previously used CEs are not considered at all in the resubmission
# Link: https://savannah.cern.ch/bugs/?28235
#

import logging

from libutils.Exceptions import *
from libutils import Job_utils


def test_logic(utils,dest_CE):


       JOBID=Job_utils.submit_wait_finish(utils,"")

       #Check for job status
       logging.info("Check job stauts")

       utils.job_status(JOBID)

       if utils.get_job_status()=="Aborted":
          logging.info("Job status is Aborted")
       else:
          logging.error("Job status is not Aborted")
          raise GeneralError("","Error !!! Job status is not Aborted")

       result=utils.run_command_continue_on_error("glite-wms-job-logging-info --event Match %s"%(JOBID))

       used_ces=[]

       for line in result.split("\n"):
         if line.find("Dest id") !=-1 :
            used_ces.append(line.split("=")[1].strip())


       for CE in used_ces :
         if CE!=  dest_CE :
          logging.error("Test failed, not found 3 times the name of the previously choosen CE. Target CE: %s while found %s"%(dest_CE,CE))
          raise GeneralError("","Error !!! Test failed, not found 3 times the name of the previously choosen CE. Target CE: %s while found %s"%(dest_CE,CE))


       logging.info("Test OK")

def run(utils):

    bug='28235'

    logging.info("Start regression test for bug %s"%(bug))
    
    utils.use_utils_jdl()
    utils.set_shallow_jdl(utils.get_jdl_file())
    
    logging.info("Get availabe CEs for job submission")

    result=utils.run_command_continue_on_error("glite-wms-job-list-match %s -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    
    available_ces=[]
        
    for line in result.split("\n"):
       if line.find("-") !=-1 :
         available_ces.append(line.split(" - ")[1])


    logging.info("Check if there is CREAM CE available")

    CE=''

    for x in available_ces :
       if x.find("/cream-") != -1 :
          CE=x
          break


    if len(CE) > 0 :

       logging.info("Execute the test for the CREAM CE: %s"%(CE))

       utils.add_jdl_attribute(utils.get_jdl_file(),'Requirements','other.GlueCEUniqueID==\"%s\"'%(CE))

       test_logic(utils,CE)

   
       
    logging.info("Check if there is LCG CE available")

    CE=''

    for x in available_ces :
       if x.find("2119/jobmanager") != -1 :
          CE=x
          break

    if len(CE) > 0 :

       logging.info("Execute the test for the LCG CE: %s"%(CE))

       utils.remove(utils.get_jdl_file())
       utils.use_utils_jdl()
       utils.set_shallow_jdl(utils.get_jdl_file())
       utils.add_jdl_attribute(utils.get_jdl_file(),'Requirements','other.GlueCEUniqueID==\"%s\"'%(CE))

       test_logic(utils,CE)
       
   
 
    logging.info("End of regression test for bug %s",bug)
