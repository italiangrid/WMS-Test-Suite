#! /usr/bin/python

import sys
import signal
import traceback
import time

from Exceptions import *

import Test_utils
import SSH_utils


def test1(utils, title):

    utils.show_progress(title)
    utils.info(title)

    try:

        CREAMs=[]

        utils.info("Set MaxReplansCount=5; and ReplanGracePeriod=10; to glite_wms.conf at WMS")

        ssh=SSH_utils.open_ssh(utils.get_WMS(),utils.WMS_USERNAME,utils.WMS_PASSWORD)

        SSH_utils.change_remote_file(utils,ssh,"/etc/glite-wms/glite_wms.conf", ['MaxReplansCount','ReplanGracePeriod','LogLevel'],['*','*','*'],['5','10','6'])

        utils.info("Restart workload manager glite-wms-wm")

        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

        utils.set_feedback_jdl(utils.get_jdl_file())

        utils.info("Get available CREAM CEs")

        CEs=utils.run_command_continue_on_error("glite-wms-job-list-match -a -c %s %s"%(utils.get_config_file(),utils.get_jdl_file())).split("\n")

        for CE in CEs:
            if CE.find(":8443")!=-1:
                CREAMs.append(CE.strip(" -\t\n").split(":")[0])

        if len(CREAMs)>1:
          utils.set_requirements("RegExp(\"%s*\", other.GlueCEUniqueID) || RegExp(\"%s*\", other.GlueCEUniqueID)"%(CREAMs[0],CREAMs[1]))

        utils.info("Submit jobs to trigger feedback mechanism")
        
        JOBIDS=[]

        for i in range(0,10):
          JOBIDS.append(utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file())))

        utils.info("Wait 60 secs")
        time.sleep(60)

        counter=0        
        limit=10
        find=0

        target="%s/workload_manager_events.log"%(SSH_utils.execute_remote_cmd(ssh,"echo $WMS_LOCATION_LOG").strip(" \n\t"))

        while counter<limit :

             for JOBID in JOBIDS:

                 utils.info("Check if replan mechanism is triggered for job %s"%(JOBID))

                 output=SSH_utils.execute_remote_cmd(ssh,"grep \"created replanning request for job %s\" %s"%(JOBID,target))

                 if output!='':
                    utils.info("Found in workload_manager_events.log a replanning request for job %s"%(JOBID))
                    utils.dbg(output)
                    find=1
                    break

             if find==1:
                break
                
             time.sleep(60)
             counter=counter+1


        if find==0:
           utils.error("Timeout reached while checking if replan mechanism is triggered at least for one job")
           raise TimeOutError("","Timeout reached while checking if replan mechanism is triggered at least for one job")


        utils.info("Check if resubmission event is logged for replan job %s"%(JOBID))

        OUTPUT=utils.run_command_continue_on_error("glite-wms-job-logging-info -c %s %s"%(utils.get_config_file(),JOBID)).split("\n")

        find=0

        for line in OUTPUT:

            if line.find("Event: Resubmission")!=-1:
               utils.info("Check OK, find resubmission event for job %s"%(JOBID))
               find=1
               break

        if find==0:
            utils.error("Test failed, unable to find resubmission event for replan job %s"%(JOBID))
            raise GeneralError("Check if resubmission event is logged for replan job %s"%(JOBID),"Unable to find resubmission event for replan job %s"%(JOBID))

        utils.info("Check if job is aborted due to the maximum number of allowed replans")

        utils.wait_until_job_finishes(JOBID)

        utils.job_status(JOBID)

        if utils.get_job_status().find("Aborted")==-1:

            utils.error("TEST FAILED. Error job's final status is %s and not Aborted"%(utils.get_job_status()))
            raise GeneralError("Check if job's status is Aborted","Error job's final status is %s and not Aborted"%(utils.get_job_status()))

        else:

            OUTPUT=utils.run_command_continue_on_error("glite-wms-job-status -c %s %s"%(utils.get_config_file(),JOBID)).split("\n")

            for line in OUTPUT:
                 if line.find("Status Reason")!=-1:
                     reason=line.split(":")[1].strip(" \n\t")

            if reason.find("hit max number of replans")==-1:
                utils.error("TEST FAILED. Aborted reason is '%s' while expected is 'hit max number of replans'"%(reason))
                raise GeneralError("Check status reason","Aborted reason is %s while expected is 'hit max number of replans'"%(reason))
            else:
                utils.info("TEST PASS")

        utils.info("Cancel the remaining jobs")

        for JOBID in JOBIDS:
            if utils.job_is_finished(JOBID)==0:
               utils.run_command_continue_on_error("glite-wms-job-cancel -c %s --noint %s"%(utils.get_config_file(),JOBID))

        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
        SSH_utils.close_ssh(ssh)


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
        SSH_utils.close_ssh(ssh)
        return 1

    return 0

    
def main():

    fails=[]

    tests=["Test 1: Test WMS feedback feature"]
    
    utils = Test_utils.Test_utils(sys.argv[0],"WMS Feedback")

    utils.prepare(sys.argv[1:],tests)

    if utils.WMS_USERNAME=='' or utils.WMS_PASSWORD=='':
       utils.warn("Please set the required variables WMS_USERNAME , WMS_PASSWORD in test's configuration file")
       utils.show_progress("Please set the required variables WMS_USERNAME , WMS_PASSWORD in test's configuration file")
       sys.exit(0)

    utils.info("WMS Job Resubmission Testing")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    if test1(utils, tests[0]):
        fails.append(tests[0])
                
    if len(fails) > 0 :
      utils.exit_failure("%s test(s) fail(s): %s"%(len(fails), fails))
    else:
      utils.exit_success()
    
    
  
if __name__ == "__main__":
    main()
