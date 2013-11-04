
from Exceptions import *

import commands
import time
import glob
import os

def perusal_target_ces(utils,custom_requirements):

   CES=[]
   NAMES=[]

   for requirement in custom_requirements:
       NAMES.append(requirement)
       CES.append(custom_requirements[requirement])

   if len(custom_requirements)>0:
         utils.EXTERNAL_REQUIREMENTS=1
   else:
         utils.EXTERNAL_REQUIREMENTS=0
         NAMES=["Submit to LCG-CE","Submit to CREAM CE"]
         CES=["2119/jobmanager","/cream-"]

   return NAMES,CES
	


def perusal_submit_test(utils,target):

    utils.set_perusal_jdl(utils.get_jdl_file())

    if target !="":
        if utils.EXTERNAL_REQUIREMENTS==0:
             utils.set_destination_ce(utils.get_jdl_file(),target)
        else:
             utils.set_requirements("%s && %s"%(target,utils.DEFAULTREQ))

    JOBID=utils.run_command("glite-wms-job-submit %s --nomsg -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Job %s has been submitted"%(JOBID),'DEBUG')

    utils.run_command("glite-wms-job-perusal --set --filename out.txt -f std.out %s"%(JOBID))

    utils.log_info("Wait until job's state is Running")

    while utils.get_job_status(JOBID).find("Running")==-1 and utils.job_is_finished(JOBID)==0:
        time.sleep(30)
           
    utils.log_info("Wait for 1010 secs")

    time.sleep(1010)

    utils.run_command("glite-wms-job-perusal --get -f out.txt --dir %s %s"%(utils.get_job_output_dir(),JOBID))

    utils.log_info("Check if some chunkes have been retrieved")

    filespec="out.txt-*"

    first_try_chunk=glob.glob(os.path.join(utils.get_job_output_dir(),filespec))

    if len(first_try_chunk):
         utils.log_info("These chunks have been retrieved: %s"%(first_try_chunk))
    else:
         utils.log_info("ERROR: No chunks have been retrieved")
         raise GeneralError("glite-wms-job-perusal --get","No chunks have been retrieved.")

    utils.log_info("Wait for another 1010 secs")

    time.sleep(1010)

    utils.run_command("glite-wms-job-perusal --get -f out.txt --dir %s %s"%(utils.get_job_output_dir(),JOBID))

    utils.log_info("Check if some chunks have been retrieved")

    second_try_chunk=glob.glob(os.path.join(utils.get_job_output_dir(),filespec))

    if len(second_try_chunk)>len(first_try_chunk):
         utils.log_info("These chunks have been retrieved: %s"%(second_try_chunk))
    else:
         utils.log_info("ERROR: No chunks have been retrieved")
         raise GeneralError("glite-wms-job-perusal --get","No chunks have been retrieved.")

    second_try_chunk.remove(first_try_chunk[0])


def test8_target_ces(utils,custom_requirements):

   CES=[]
   NAMES=[]

   for requirement in custom_requirements:
       NAMES.append(requirement)
       CES.append(custom_requirements[requirement])

   if len(custom_requirements)>0:
         utils.EXTERNAL_REQUIREMENTS=1
   else:
         utils.EXTERNAL_REQUIREMENTS=0
         NAMES.append("Default Test")
         CES.append("/cream-")

   return NAMES,CES
	


def check_forward_parameters(utils,cream_jdl,case):

   errors=[]
   
   params=[
            'CpuNumber = 2,WholeNodes = true,SMPGranularity = 2,Hostnumber = 1',
            'CpuNumber = 1,WholeNodes = true,SMPGranularity = 2',
            'CpuNumber = 2,WholeNodes = false,SMPGranularity = 1',
            'CpuNumber = 2,WholeNodes = true,SMPGranularity = 1,Hostnumber = 2',
            'CpuNumber = 3,WholeNodes = false,SMPGranularity = 3,Hostnumber = 1'
 	  ]    

   utils.log_info("Check the cream jdl for the forwarding parameters")

   check=params[int(case)-1].split(",")

   for attribute in check:
      if cream_jdl.find(attribute)==-1:
         errors.append(attribute)

   if len(errors)>0:
      msg=' , '.join(errors)
      utils.log_info("Problem with the following parameters: %s"%(msg))
      raise GeneralError("Check forwarding parameters","Problem with the following parameters: %s"%(msg)) 
   else:
      utils.log_info("Check OK , found all forwarding parameters")

 
def check_forward_invalid_parameters(utils,jdlfile):

    OUTPUT=commands.getstatusoutput("glite-wms-job-submit %s -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),jdlfile))

    if OUTPUT[0]==0 :
         utils.log_info("Submission not failed as expected")
         raise RunCommandError("Forward invalid parameters","Submission with invalid parameters not failed as expected")
    else:        
         utils.log_info("Submission failed as expected")
         utils.log_info('Command output:%s'%(OUTPUT[1]),'DEBUG')

         utils.log_info("Check error message")

         if OUTPUT[1].find("SMPGranularity and HostNumber are mutually exclusive when WholeNodes allocation is not requested: wrong combination of values")==-1:
           utils.log_info("Job failed reason: %s. Expected reason: SMPGranularity and HostNumber are mutually exclusive when WholeNodes allocation is not requested: wrong combination of values"%(OUTPUT[1]))
           raise GeneralError("","Job failed but not with the expected reason. Job failed reason"%(OUTPUT[1]))
      
