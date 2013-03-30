
import commands
import time

from Exceptions import *

def cancel_job(utils,jobid):

    utils.log_info('Execute command: glite-wms-job-cancel --config %s --noint %s'%(utils.get_config_file(),jobid))

    OUTPUT=commands.getstatusoutput("glite-wms-job-cancel --config %s --noint %s"%(utils.get_config_file(),jobid))
             
    if OUTPUT[0]!=0:
          utils.log_info('Command glite-wms-job-cancel failed. Failure message: %s'%(OUTPUT[1]))
          raise RunCommandError('','Command glite-wms-job-cancel failed. Check log file for details')
 
    utils.log_info('Command output:\n%s'%(OUTPUT[1]),'DEBUG')
       
    return OUTPUT[1]

# On failure raise a GeneralError exception
def check_status(utils,jobid):

    i=0

    utils.log_info("Try to check the status 6 times (for a total of 100 seconds)")

    # try to check the status 6 times (for a total of 100 seconds)
    while ( utils.get_job_status(jobid).find("Cancelled")==-1 and i<6) :
        if utils.job_is_finished(jobid) :
            # final status is wrong test should fails!!!
            utils.log_info("Job %s final status is: %s."%(jobid,utils.get_job_status(jobid)))
            break
        i+=1
        time.sleep(i*5)
        utils.log_info("Wait %s seconds for the next try"%(i*5))
   
        
    #Cancelled 
    if utils.job_is_finished(jobid) == 3 :
         utils.log_info("Job has been cancelled successfully")
    else:  # All the retries fail, raise exception
	 utils.log_info("TEST FAILS. Job's %s status is wrong: %s"%(jobid,utils.get_job_status(jobid)))
         raise GeneralError("Check job status","Job status is wrong: %s"%(utils.get_job_status(jobid)))
        
   
def get_node_ids(utils,jobid):

      # Get nodes' ids
      output=commands.getoutput("glite-wms-job-status %s"%(jobid))
        
      IDS=[]

      for line in output.splitlines():
          if line.split(":",1)[0].strip() == "Status info for the Job":
              IDS.append(line.split(":",1)[1].strip())
              utils.log_info("Next node's id is: %s"%(IDS[-1]),'DEBUG')


      return IDS

