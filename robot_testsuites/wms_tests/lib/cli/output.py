import commands
import time
import os
import os.path

from Exceptions import *

def test_output(utils,options,jobid=''):

    if len(jobid)>0:
        exec_str="%s %s"%(options,jobid)
    else:
        exec_str=options 
  
    utils.log_info('Execute command: glite-wms-job-output %s'%(exec_str))

    OUTPUT=commands.getstatusoutput("glite-wms-job-output %s"%(exec_str))
             
    if OUTPUT[0]!=0:
          utils.log_info('Command glite-wms-job-output failed. Failure message: %s'%(OUTPUT[1]))
          raise RunCommandError('','Command glite-wms-job-output failed. Check log file for details')
 
    utils.log_info('Command output:\n%s'%(OUTPUT[1]),'DEBUG')
       
    return OUTPUT[1]


def checkstatus(utils,jobid,input):

    time.sleep(10)

    utils.log_info("Check if job's status is correct") 

    if input.find("Warning - JobPurging not allowed")==-1:

        if utils.get_job_status(jobid).find("Cleared")!=-1:
           utils.log_info("Job's status is Cleared")        
        else:
           utils.log_info("=== WARNING === Job %s is not cleared"%(jobid))
           raise GeneralError("Check job's status","Job %s is not cleared"%(jobid))
           return 1
 
    else:
        utils.log_info("Warning: WMS is not recognized by the LB, JobPurging not allowed !")
   
    return 0

def checkoutput(utils,input):

    utils.log_info("Check if output files are correctly retrieved")

    dir=''

    lines=input.split("\n") 

    for line in lines:

       if line.find("have been successfully retrieved")!=-1:
          dir=lines[lines.index(line)+1].strip(" \n\t")           
          break
  
    if len(dir)==0:
        utils.log_info("=== ERROR === Unable to find the output directory")
        raise GeneralError("Check output","Unable to find the output directory")
     
    if os.path.isfile("%s/std.out"%(dir)) & os.path.isfile("%s/std.err"%(dir)):
        utils.log_info("Check ok , output files have been successfully retrieved")
        os.unlink("%s/std.out"%(dir))   
        os.unlink("%s/std.err"%(dir))
        os.rmdir(dir)
    else:
        utils.log_info("=== ERROR === Unable to find the expected output files: std.out and std.err")
        raise GeneralError("Check output","Unable to find the expected output files: stdout and std.err")
 


def check(utils,jobid,input):

    result=checkstatus(utils,jobid,input)

    if result==0:
       checkoutput(utils,input)
