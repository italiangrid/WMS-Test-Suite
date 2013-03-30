import commands
import time

from Exceptions import *

def test_cancel(utils,options,jobid=""):

    if len(jobid)>0:
        exec_str="--noint %s %s"%(options,jobid)
    else:
        exec_str="--noint %s"%(options) 
  
    utils.log_info('Execute command: glite-wms-job-cancel %s'%(exec_str))

    OUTPUT=commands.getstatusoutput("glite-wms-job-cancel %s"%(exec_str))
             
    if OUTPUT[0]!=0:
          utils.log_info('Command glite-wms-job-cancel failed. Failure message: %s'%(OUTPUT[1]))
          raise RunCommandError('','Command glite-wms-job-cancel failed. Check log file for details')
 
    utils.log_info('Command output:\n%s'%(OUTPUT[1]),'DEBUG')
       
    return OUTPUT[1]


def check_status(utils,jobid):

    i=0

    utils.log_info("Try to check the job status 5 times (for a total of 75 seconds)")

    # try to check the status 5 times (for a total of 75 seconds)
    while ( utils.get_job_status(jobid) !="Cancelled" and i<5) :
        i=i+1
        utils.log_info("Wait %s seconds for the next try"%(i*5),'DEBUG')
        time.sleep(i*5)

    # if all tries fail exit with failure

    if utils.get_job_status(jobid) !="Cancelled" :

        if utils.job_is_finished(jobid) == 0 :
           utils.log_info(" == ERROR == Job's %s status is wrong: %s"%(jobid,utils.get_job_status(jobid)))
           raise GeneralError("Check job status","Job status is wrong: %s"%(utils.get_job_status(jobid)))
        else :
           utils.log_info("== WARNING == Job %s finished with status %s before cancellation."%(jobid,utils.get_job_status(jobid)))
           raise GeneralError("Check job status","Job finished with status %s before cancellation"%(utils.get_job_status(jobid)))
       

