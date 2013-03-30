#
# Bug: 87259
# Title: WMS purger leaves sandboxes untouched in case LB status returns EIDRM
# Link: https://savannah.cern.ch/bugs/?87259
#
#

import time

from lib.Exceptions import *


def run(utils):

    bug='87259'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    utils.log_info("TEST 1: Test purging of the JC local directories")

    utils.log_info("Prepare jdl file for submission")
    utils.use_utils_jdl()
    utils.set_isb_jdl(utils.get_jdl_file())

    utils.log_info("Submit job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))
    
    utils.log_info("Wait until job is finished")

    utils.wait_until_job_finishes(JOBID)

    utils.log_info("Wait 60 secs")

    time.sleep(60)
    
    utils.log_info("Check the log file of the LogMonitor: $WMS_LOCATION_LOG/logmonitor_events.log")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    result=utils.execute_remote_cmd(ssh,"echo $WMS_LOCATION_LOG").split("\n")[0]

    utils.ssh_get_file(ssh, "%s/logmonitor_events.log"%(result), "%s/local_copy"%(utils.get_tmp_dir()))

    FILE=open("%s/local_copy"%(utils.get_tmp_dir()))
    output=FILE.readlines()
    FILE.close()

    prefix=JOBID.split(":9000/")[1][0:2]

    job_dir=0
    job_dir_str=''
    submit_file=0
    submit_file_str=''
    classad_file=0
    classad_file_str=''
    wrapper_file=0
    wrapper_file_str=''
    
    for line in output:

       if line.find("Removing job directory: /var/jobcontrol/condorio/%s"%(prefix))!=-1:
           job_dir_str=line.strip("\n").split("Removing job directory: ")[1]
           job_dir=1
           utils.log_info("Find logging for removing of job directory")

       if line.find("Removing submit file: /var/jobcontrol/submit/%s"%(prefix))!=-1:
           submit_file_str=line.strip("\n").split("Removing submit file: ")[1]
           submit_file=1
           utils.log_info("Find logging for removing of submit file")

       if line.find("Removing classad file: /var/jobcontrol/submit/%s"%(prefix))!=-1:
           classad_file_str=line.strip("\n").split("Removing classad file: ")[1]
           classad_file=1
           utils.log_info("Find logging for removing of classad file")

       if line.find("Removing wrapper file: /var/jobcontrol/submit/%s"%(prefix))!=-1:
           wrapper_file_str=line.strip("\n").split("Removing wrapper file: ")[1]
           wrapper_file=1
           utils.log_info("Find logging for removing of wrapper file")

    if job_dir==0:
       ssh.close()
       utils.log_info("ERROR: Unable to find logging for removing of job directory")
       raise GeneralError("Check log file of LogMonitor","Unable to find logging for removing of the job directory")

    if submit_file==0:
       ssh.close()
       utils.log_info("ERROR: Unable to find logging for removing of submit file")
       raise GeneralError("Check log file of LogMonitor","Unable to find logging for removing of submit file")

    if classad_file==0:
       ssh.close()
       utils.log_info("ERROR: Unable to find logging for removing of classad file")
       raise GeneralError("Check log file of LogMonitor","Unable to find logging for removing of classad file")

    if wrapper_file==0:
       ssh.close()
       utils.log_info("ERROR: Unable to find logging for removing of wrapper file")
       raise GeneralError("Check log file of LogMonitor","Unable to find logging for removing of wrapper file")


    utils.log_info("Check that these files have been actually removed")

    utils.run_command_fail("ls %s"%(job_dir_str))
    utils.run_command_fail("ls %s"%(submit_file_str))
    utils.run_command_fail("ls %s"%(classad_file_str))
    utils.run_command_fail("ls %s"%(wrapper_file_str))

    utils.log_info("TEST 1: OK")
    
    utils.log_info("TEST 2: Check if the SBD purger can trap the EIDRM")

    utils.log_info("Prepare jdl file for submission")

    utils.set_isb_jdl(utils.get_jdl_file())

    utils.log_info("Submit job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

    utils.log_info("Wait 60 secs")
    time.sleep(60)

    utils.log_info("Create a copy of the sandbox dir in the WMS")

    prefix=JOBID.split(":9000/")[1][0:2]

    target="/var/SandboxDir/"+prefix

    file=utils.execute_remote_cmd(ssh,"ls %s/"%(target)).strip(" \t\n")
    
    utils.execute_remote_cmd(ssh,"cp -r -p %s/%s/ %s/%s.old"%(target,file,target,file))

    utils.log_info("Wait until job is finished")

    utils.wait_until_job_finishes(JOBID)

    utils.log_info("Retrieve the output sandbox")

    utils.run_command("glite-wms-job-output --noint --dir %s %s"%(utils.get_job_output_dir(),JOBID))

    utils.log_info("Check %s/%s that has been removed"%(target,file))

    res=utils.execute_remote_cmd(ssh,"ls %s/"%(target)).split("\n")

    for li in res:

       if li==file:
          ssh.close()
          utils.log_info("ERROR: %s/%s has not been removed as expected"%(target,file))
          raise GeneralError("","%s/%s has not been removed as expected"%(target,file))
    
    utils.log_info("%s/%s has been removed as expected"%(target,file))

    utils.log_info("Restored the sandbox dir in the WMS")

    utils.execute_remote_cmd(ssh,"mv %s/%s.old %s/%s"%(target,file,target,file))

    utils.execute_remote_cmd(ssh,"echo \"%s\" > /root/jobid.txt"%(JOBID))

    utils.log_info("Purge the job from LBProxy")

    output=utils.execute_remote_cmd(ssh,"/usr/bin/glite-lb-purge -m %s -x -j /root/jobid.txt"%(utils.get_WMS()))

    if output.find("The jobs were not dumped")==-1:
        ssh.close()
        utils.log_info("ERROR: Purge job from LBProxy not returned 'The jobs were not dumped' as expected")
        raise GenerarError("","Purge job from LBProxy not returned 'The jobs were not dumped' as expected")

    utils.log_info("Purge the job from LBServer")

    output=utils.execute_remote_cmd(ssh,"/usr/bin/glite-lb-purge -m %s -j /root/jobid.txt"%(utils.LB))

    if output.find("The jobs were not dumped")==-1:
        ssh.close()
        utils.log_info("ERROR: Purge job from LBProxy not returned 'The jobs were not dumped' as expected")
        raise GenerarError("","Purge job from LBProxy not returned 'The jobs were not dumped' as expected")

    utils.log_info("Verify that job status returns identifier removed (error EIDRM)")

    output=utils.run_command_fail("glite-wms-job-status -c %s %s"%(utils.get_config_file(),JOBID))

    if output.find("glite.lb.Exception: edg_wll_JobStatus: Identifier removed: matching job already purged")==-1:
        ssh.close()
        utils.log_info("ERROR: Job status did not return identifier removed error (error EIDRM)")
        raise GeneralError("","Job status did not return identifier removed error (error EIDRM)")

    utils.log_info("Execute command glite-wms-purgeStorage.sh on the WMS")

    chan=ssh.invoke_shell()

    cmd="/usr/sbin/glite-wms-purgeStorage.sh -p %s"%(target)

    chan.send("su - glite \n")

    tCheck=0

    while not chan.recv_ready():
        time.sleep(1)
        tCheck+=1
        if tCheck >= 6:
            utils.log_info("ERROR: Time out while waiting response from remote host %s"%(utils.get_WMS()))
            raise TimeOutError("","Time out while waiting response from remote host %s"%(utils.get_WMS()))

    chan.recv(1024)

    chan.send(cmd +"\n")

    tCheck=0

    while not chan.recv_ready():
        time.sleep(1)
        tCheck+=1
        if tCheck >= 6:
            utils.log_info("ERROR: Time out while waiting response from remote host %s"%(utils.get_WMS()))
            raise TimeOutError("","Time out while waiting response from remote host %s"%(utils.get_WMS()))

    output = chan.recv(1024)

    if output.find("edg_wll_JobStat [43] Identifier removed(matching job already purged)")==-1:
        ssh.close()
        utils.log_info("ERROR: Command %s did not return error identifier removed (error 43)"%(cmd))
        raise GeneralError("","Command %s did not return error identifier removed (error 43)"%(cmd))

    utils.log_info("Check that SandboxDir has been removed")

    res=utils.execute_remote_cmd(ssh,"ls %s/"%(target)).strip("\n\t")

    if len(res)!=0:
        ssh.close()
        utils.log_info("ERROR: The SandboxDir didn't removed")
        raise GeneralError("","The SandboxDir didn't removed")
    
    ssh.close()

    utils.log_info("TEST 2: OK")

    utils.log_info("End of regression test for bug %s"%(bug))
