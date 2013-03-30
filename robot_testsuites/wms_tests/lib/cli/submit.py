import commands


from Exceptions import *

def test_submit(utils,options,jdl=""):

    if len(jdl)>0:
        exec_str="%s %s"%(options,jdl)
    else:
        exec_str=options
  
    utils.log_info('Execute command: glite-wms-job-submit %s'%(exec_str))

    OUTPUT=commands.getstatusoutput("glite-wms-job-submit %s"%(exec_str))
             
    if OUTPUT[0]!=0:
          utils.log_info('Command glite-wms-job-submit failed. Failure message: %s'%(OUTPUT[1]))
          raise RunCommandError('','Command glite-wms-job-submit failed. Check log file for details')
 
    utils.log_info('Command output:\n%s'%(OUTPUT[1]),'DEBUG')
       
    return OUTPUT[1]


def cancel_job(utils,jobid): 
    
    utils.log_info("Cancel submitted job with identifier: %s"%(jobid))

    utils.run_command("glite-wms-job-cancel --noint %s "%(jobid))


def parse_jobid(utils,input):

    jobid='' 

    for line in input.split("\n"):
       if line.find(":9000")!=-1:
           
           if line.find("--start")!=-1:
              line=line.split("--start")[1]  

           jobid=line.strip(" \t\n")
           break

  
    utils.log_info("Job id is: %s"%(jobid))

    return jobid

def get_first_ce(utils,input):

    ce=''

    for line in input.split("\n"):
      if line.find(" - ")!=-1:
         ce=line.strip(" \t\n")
         break        

    return ce

def clear_ce(input):
    
   return input.split("- ")[1]


def parse_json_jobid(input):

  jobid=''
  
  lines=input.split(",")

  for line in lines:
     if line.find("jobid")!=-1:
        jobid=line.split("jobid\":")[1].strip(" \n\t")
        jobid=jobid.replace("\"","")
 
  return jobid
 
def get_jdl_expiry(utils,jobid):
    
   expiry_time=''

   output=utils.run_command("glite-wms-job-info --noint --jdl %s"%(jobid))

   for line in output.split("\n"):
       if line.find("ExpiryTime")!=-1:
          expiry_time=line.split("=")[1].strip(" \t\n;")
          break  

   return expiry_time



