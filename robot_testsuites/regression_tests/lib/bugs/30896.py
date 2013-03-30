#
# Bug: 30896
# Title: WMS must limit number of files per sandbox
# Link: https://savannah.cern.ch/bugs/?30896
#
#


from lib.Exceptions import *


def test_sandbox_files(utils,bug,test):

    ret=[0,'']

    attributes=['MaxInputSandboxFiles','MaxOutputSandboxFiles']
    msg=['The maximum number of input sandbox files is reached','The maximum number of output sandbox files is reached']


    utils.log_info("Execute test for attribute %s"%(attributes[test-1]))

    utils.log_info("Submit the job and wait to finish")

    utils.use_external_jdl("%s.jdl"%(bug))

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Check job status")

    utils.job_status(JOBID)

    STATUS=utils.get_job_status()

    if STATUS.find("Aborted") ==-1:
          utils.log_info("ERROR: Job status is not Aborted as expected. Instead we get %s"%(STATUS))
          ret[0]=-1
          ret[1]="Test attribute %s: Job status is not Aborted as expected, instead we get %s"%(attributes[test-1],STATUS)
    else:

        utils.log_info("Check status reason")

        OUTPUT=utils.run_command("glite-wms-job-status %s"%(JOBID))

        if OUTPUT.find("%s"%(msg[test-1])) == -1:
          utils.log_info("ERROR: Job aborted not because 'The maximum number of input sandbox files is reached'.")
          ret[0]=-1
          ret[1]="Test attribute %s: Job aborted not because '%s'"%(attributes[test-1],msg[test-1])

    return ret



def run(utils):

    bug='30896'

    error_msg=[]

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Set MaxInputSandboxFiles=2; to glite_wms.conf at WMS")

    utils.add_attribute_to_remote_file(ssh, "/etc/glite-wms/glite_wms.conf","WorkloadManagerProxy", ['MaxInputSandboxFiles'],['2'])

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

    #Test attribute MaxInputSandboxFiles
    ret1=test_sandbox_files(utils,bug,1)

    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")

    utils.log_info("Set MaxOutputSandboxFiles=2; to glite_wms.conf at WMS")

    utils.add_attribute_to_remote_file(ssh, "/etc/glite-wms/glite_wms.conf","WorkloadManagerProxy", ['MaxOutputSandboxFiles'],['2'])

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
    
    #Test attribute MaxOutputSandboxFiles
    ret2=test_sandbox_files(utils,bug,2)

    if ret1[0] == -1:
      error_msg.append(ret1[1])

    if ret2[0] == -1:
      error_msg.append(ret2[1])


    if len(error_msg)>0:
       utils.log_info("ERROR: Test Failed. Error: %s"%(error_msg))
       utils.log_info("Restore the initial glite_wms.conf file")
       utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
       utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
       ssh.close()
       raise GeneralError("Check test results","Test Failed. Error:%s"%(error_msg))

    
    utils.log_info("Restore the initial glite_wms.conf file")

    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
   
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
    
    ssh.close()
    
    utils.log_info("End of regression test for bug %s"%(bug))
