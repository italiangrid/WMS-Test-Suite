import commands
import time

from Exceptions import *

def test_status(utils,options,jobid=''):

    if len(jobid)>0:
        exec_str="%s %s"%(options,jobid)
    else:
        exec_str=options 
  
    utils.log_info('Execute command: glite-wms-job-status %s'%(exec_str))

    OUTPUT=commands.getstatusoutput("glite-wms-job-status %s"%(exec_str))
             
    if OUTPUT[0]!=0:
          utils.log_info('Command glite-wms-job-status failed. Failure message: %s'%(OUTPUT[1]))
          raise RunCommandError('','Command glite-wms-job-status failed. Check log file for details')
 
    utils.log_info('Command output:\n%s'%(OUTPUT[1]),'DEBUG')
       
    return OUTPUT[1]

def sleep_until_wait_status(utils,jobid):

    utils.log_info("Waiting until job arrives to the Waiting status")

    while utils.get_job_status(jobid).find("Waiting")==-1:
          utils.log_info("Job's status is %s sleep 10 secs"%(utils.get_job_status(jobid)))
          time.sleep(10) 
                    
