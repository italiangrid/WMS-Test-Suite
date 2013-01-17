import commands

from Exceptions import *

def test_job_info(utils,options,jobid=""):

    if len(jobid)>0:
        exec_str="%s %s"%(options,jobid)
    else:
        exec_str=options
  
    utils.log_info('Execute command: glite-wms-job-info %s'%(exec_str))

    OUTPUT=commands.getstatusoutput("glite-wms-job-info %s"%(exec_str))
             
    if OUTPUT[0]!=0:
          utils.log_info('Command glite-wms-job-info failed. Failure message: %s'%(OUTPUT[1]))
          raise RunCommandError('','Command glite-wms-job-info failed. Check log file for details')
 
    utils.log_info('Command output:\n%s'%(OUTPUT[1]),'DEBUG')
       
    return OUTPUT[1]

def clear_jobid(input):
   
    jobid=input.strip(" \n\t;")
    jobid=jobid.replace("\"","")

    return jobid

def get_expiry_time(input):
   
    exp=''

    for line in input.split("\n"):
        if line.find("Expiration")!=-1:
           exp=line.split(" : ")[1].strip(" \t\n")
           break
 
    return exp
