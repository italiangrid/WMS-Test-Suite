#
# Bug:78047
# Title: LB Query timeout
# Link: https://savannah.cern.ch/bugs/?78047
#
#


import time

from lib.Exceptions import *


def run(utils):

    bug='78047'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    CREAMs=[]

    utils.log_info("Set MaxReplansCount=5; and ReplanGracePeriod=10; to glite_wms.conf at WMS")

    ssh=utils.open_ssh(utils.get_WMS(),utils.WMS_USERNAME,utils.WMS_PASSWORD)

    utils.change_remote_file(ssh,"/etc/glite-wms/glite_wms.conf", ['MaxReplansCount','ReplanGracePeriod','LogLevel'],['*','*','*'],['5','10','6'])

    utils.log_info("Restart workload manager glite-wms-wm")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    utils.log_info("Prepare jdl file for submission")

    utils.use_external_jdl("%s.jdl"%(bug))
   
    utils.log_info("Get available CREAM CEs")

    CEs=utils.run_command("glite-wms-job-list-match -a -c %s %s"%(utils.get_config_file(),utils.get_jdl_file())).split("\n")

    for CE in CEs:
       if CE.find(":8443")!=-1:
           CREAMs.append(CE.strip(" -\t\n").split(":")[0])

    if len(CREAMs)>1:
         utils.set_requirements("RegExp(\"%s*\", other.GlueCEUniqueID) || RegExp(\"%s*\", other.GlueCEUniqueID)"%(CREAMs[0],CREAMs[1]))

    utils.log_info("Submit jobs to trigger feedback mechanism")

    JOBIDS=[]

    for i in range(0,10):
      JOBIDS.append(utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file())))

    utils.log_info("Wait 60 secs")
    time.sleep(60)

    counter=0
    limit=10
    find=0

    target="%s/workload_manager_events.log"%(utils.execute_remote_cmd(ssh,"echo $WMS_LOCATION_LOG").strip(" \n\t"))

    while counter<limit :

        for JOBID in JOBIDS:

            utils.log_info("Check if replan mechanism is triggered for job %s"%(JOBID))

            output=utils.execute_remote_cmd(ssh,"grep \"created replanning request for job %s\" %s"%(JOBID,target))

            if output!='':
              utils.log_info("Found in workload_manager_events.log a replanning request for job %s"%(JOBID))
              utils.log_info(output,'DEBUG')
              find=1
              break

        if find==1:
            break

        time.sleep(60)
        counter=counter+1


    if find==0:
       utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
       utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
       utils.close_ssh(ssh)
       utils.log_info("ERROR: Timeout reached while checking if replan mechanism is triggered at least for one job")
       raise TimeOutError("","Timeout reached while checking if replan mechanism is triggered at least for one job")


    utils.log_info("Check if resubmission event is logged for replan job %s"%(JOBID))

    OUTPUT=utils.run_command("glite-wms-job-logging-info -c %s %s"%(utils.get_config_file(),JOBID)).split("\n")

    find=0

    for line in OUTPUT:
        if line.find("Event: Resubmission")!=-1:
            utils.log_info("Check OK, find resubmission event for job %s"%(JOBID))
            find=1
            break

    if find==0:
        utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
        utils.close_ssh(ssh)
        utils.log_info("ERROR: Test failed, unable to find resubmission event for replan job %s"%(JOBID))
        raise GeneralError("Check if resubmission event is logged for replan job %s"%(JOBID),"Unable to find resubmission event for replan job %s"%(JOBID))

    utils.log_info("Check if job is aborted due to the maximum number of allowed replans")

    utils.wait_until_job_finishes(JOBID)

    utils.job_status(JOBID)

    if utils.get_job_status().find("Aborted")==-1:
          utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
          utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
          utils.close_ssh(ssh)
          utils.log_info("ERROR: Test Faile - Job's final status is %s and not Aborted"%(utils.get_job_status()))
          raise GeneralError("Check if job's status is Aborted","Error job's final status is %s and not Aborted"%(utils.get_job_status()))
    else:

          OUTPUT=utils.run_command("glite-wms-job-status -c %s %s"%(utils.get_config_file(),JOBID)).split("\n")

          for line in OUTPUT:
              if line.find("Status Reason")!=-1:
                 reason=line.split(":")[1].strip(" \n\t")

          if reason.find("hit max number of replans")==-1:
              utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
              utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
              utils.close_ssh(ssh)
              utils.log_info("ERROR: Test Failed - Aborted reason is '%s' while expected is 'hit max number of replans'"%(reason))
              raise GeneralError("Check status reason","Aborted reason is %s while expected is 'hit max number of replans'"%(reason))
          else:
              utils.log_info("TEST OK")

    utils.log_info("Cancel the remaining jobs")

    for JOBID in JOBIDS:
       if utils.job_is_finished(JOBID)==0:
          utils.run_command("glite-wms-job-cancel -c %s --noint %s"%(utils.get_config_file(),JOBID))

    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
    utils.close_ssh(ssh)
    
    utils.log_info("End of regression test for bug %s"%(bug))

