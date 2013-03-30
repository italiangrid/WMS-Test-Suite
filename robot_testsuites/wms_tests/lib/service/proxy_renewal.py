import commands
import os.path

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

		utils.log_info("Check job's final status")

		utils.log_info("Execute: glite-wms-job-status %s"%(jobid))

		OUTPUT=commands.getstatusoutput("glite-wms-job-status %s"%(jobid))
		
		utils.log_info(OUTPUT)        
   
		if OUTPUT[1].find('Proxy is expired')!=-1:
			utils.log_info("TEST PASS")
		else: 
			utils.log_info('Unexpected failed reason','WARN')
			raise GeneralError("Unexpected failed reason","Unexpected failed reason")

	else:
		utils.log_info("TEST FAILS. Job not failed")
		raise GeneralError("Wrong job's final status","Job finished with a unexpected status: %s."%(final_status))

    
###
def check_proxy_renewal_output_file(utils,jobid):

	utils.remove(utils.get_tmp_file())

	utils.log_info("Retrieve the output")

	utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))

	utils.log_info("Check if the output files are correctly retrieved")

	if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
		utils.log_info("Output files are correctly retrieved")
	else:
		utils.log_info("Output files are not correctly retrieved")
		raise GeneralError("Check output files","Output files are not correctly retrieved")
                


