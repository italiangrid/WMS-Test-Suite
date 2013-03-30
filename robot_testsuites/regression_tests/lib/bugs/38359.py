#
# Bug:38359
# Title: Some issues in the limit for the output sandbox in the WMS jobwrapper
# Link: https://savannah.cern.ch/bugs/?38359
#
#


import os.path

from lib.Exceptions import *
from lib import Job_utils


def run(utils):

    bug='38359'

    utils.log_info("Start regression test for bug %s"%(bug))
  
    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Set MaxOutputSandoxSize=100; to glite_wms.conf at WMS")

    utils.change_remote_file(ssh,"/etc/glite-wms/glite_wms.conf", ['MaxOutputSandboxSize'],['*'],['100'])

    utils.log_info("Restart Workload Manager glite-wms-wm")
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    utils.log_info("Submit the job and wait to finish")

    utils.use_external_jdl("%s.jdl"%(bug))

    JOBID=Job_utils.submit_wait_finish(utils,"")

    utils.log_info("Get job output")

    Job_utils.output_normal_job(utils,JOBID)

    #Check job output
    utils.log_info("Check if the output files are correctly retrieved")

    if os.path.isfile("%s/test.err"%(utils.get_job_output_dir())) & os.path.isfile("%s/test.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/out1"%(utils.get_job_output_dir())) & os.path.isfile("%s/out2.tail"%(utils.get_job_output_dir())) & os.path.isfile("%s/out3"%(utils.get_job_output_dir())) & os.path.isfile("%s/out4.tail"%(utils.get_job_output_dir())) :
          utils.log_info("Output files are collectly retrieved")
    else:
          utils.log_info("ERROR: Output files are not correctly retrieved")
          utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
          utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
          ssh.close()
          raise GeneralError("","Output files are not correctly retrieved")

    #Check the content of env.out file
    utils.log_info("Check output files size")

    if int(os.path.getsize("%s/out1"%(utils.get_job_output_dir()))) != 50 or int(os.path.getsize("%s/out3"%(utils.get_job_output_dir()))) !=50 or int(os.path.getsize("%s/out2.tail"%(utils.get_job_output_dir())))!=0 or int(os.path.getsize("%s/out4.tail"%(utils.get_job_output_dir())))!=0 or int(os.path.getsize("%s/test.out"%(utils.get_job_output_dir())))!=0 or int(os.path.getsize("%s/test.err"%(utils.get_job_output_dir())))!=0 :
          utils.log_info("ERROR: Output files do not have the expected sizes.")
          utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
          utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
          ssh.close()
          raise GeneralError("","Output files do not have the expected sizes")
   
    utils.log_info("Restore the initial glite_wms.conf file")

    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
   
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
    
    ssh.close()
    
    utils.log_info("End of regression test for bug %s"%(bug))
