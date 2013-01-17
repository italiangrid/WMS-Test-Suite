import commands

from Exceptions import *

#Check Proxy Duration
def check_job_proxy_duration(utils,jobid):
        
    output=utils.run_command("glite-wms-job-info -p %s"%(jobid))
        
    for line in output.splitlines():
         if line.split(":")[0].strip() == "Timeleft":
             token=line.split(":")[1].strip()
             if ( (token.split(" ")[1] == "hours") or
                   (int(token.split(" ")[0]) > 14 ) ):
                    utils.log_info("The proxy of the submitted job has not the expected duration")
                    raise GeneralError("Check proxy of the submitted job","heck proxy of the submitted job: Wrong duration")


#Check failed reason
def check_failed_reason(utils,jobid):

    utils.log_info('Execute command: glite-wms-job-status %s'%(jobid))

    OUTPUT=commands.getstatusoutput("glite-wms-job-status %s"%(jobid))
    
    utils.log_info('Command output:\n%s'%(OUTPUT[1]),'DEBUG')
            
    if OUTPUT[1].find("proxy expired") != -1:
          utils.log_info("TEST FAILS. Proxy expired")
          raise GeneralError("Check failed reason","Check failed reason: Proxy expired")
    else:
          utils.log_info("TEST FAILS. Unexpected failed reason")
          raise GeneralError("Check failed reason","Check failed reason: Unexpected failed reason")


#Evaluate Test Final Status
def evaluate_test_final_status(utils,final_status,jobid):

    if final_status.find('Aborted')!=-1 or final_status.find('Done (Failed)')!=-1:

            OUTPUT=commands.getstatusoutput("glite-wms-job-status %s"%(jobid))
           
            if OUTPUT[1].find('Proxy is expired')!=-1:
                utils.log_info("TEST PASS")
            else: 
                utils.log_info('Unexpected failed reason','WARN')
                raise GeneralError("Unexpected failed reason","Unexpected failed reason")

    else:
         utils.log_info("TEST FAILS. Job not failed")
         raise GeneralError("Wrong job's final status","Job finished with a unexpected status: %s."%(final_status))

    
