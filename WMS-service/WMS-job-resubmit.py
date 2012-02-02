#! /usr/bin/python

import sys
import signal
import traceback

from Exceptions import *

import Test_utils


# raise GeneralError if fails
def test1(utils, title):

    utils.show_progress(title)
    utils.info(title)

    try:

        utils.set_shallow_jdl(utils.get_jdl_file())

        JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.wait_until_job_finishes(JOBID)

        utils.job_status(JOBID)

        if utils.get_job_status().find("Aborted")==-1:

            utils.error("TEST FAILS. Something goes wrong: job final status is %s"%(utils.get_job_status()))
            raise GeneralError("Check if job's status is Aborted","Something goes wrong: job final status is %s"%(utils.get_job_status()))

        else:

            OUTPUT=utils.run_command_continue_on_error("glite-wms-job-logging-info --event RESUBMISSION %s"%(JOBID))

            if OUTPUT.count("SHALLOW")!=2:
                utils.error("TEST FAILS. Job %s hasn't be correctly resubmitted"%(JOBID))
                raise GeneralError("Check the number of resubmissions","Job %s hasn't be correctly resubmitted"%(JOBID))

            else:
                utils.info("TEST PASS")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0

    
def test2(utils, title):

    utils.show_progress(title)
    utils.info(title)

    try:

        utils.set_deep_jdl(utils.get_jdl_file())

        JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.wait_until_job_finishes(JOBID)

        if utils.get_job_status().find("Aborted") == -1:

            utils.error("TEST FAILS. Something goes wrong: job final status is %s"%(utils.get_job_status()))
            raise GeneralError("Check if job's status is Aborted","Something goes wrong: job final status is %s"%(utils.get_job_status()))

        else: # job is aborted

            utils.dbg("Check the aborted reasons")
            OUTPUT=utils.run_command_continue_on_error("glite-wms-job-status %s"%(JOBID))
            
            if OUTPUT.find("Cannot take token") != -1:
                utils.error("TEST FAILS. Probably the token for job %s has not been recreated in WMS. Check it."%(JOBID))
                raise GeneralError("Detect error message: Cannot take token","Probably the token for job %s has not been recreated in WMS."%(JOBID))  
            
            for line in OUTPUT.splitlines():
                if line.split(":")[0].strip()=="Status Reason":
                    reason=line.split(":")[1].strip()
                    break
            
            if reason != "hit job retry count (2)":
                utils.warn("Job aborted for un unexpected reason: %s"%(reason))
            else:
                utils.info("TEST PASS.")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0



def main():

    fails=[]

    tests=["Test 1: Try a shallow resubmission"]
    tests.append("Test 2: Try a deep resubmission")

    utils = Test_utils.Test_utils(sys.argv[0],"WMS Job Resubmission Testing")

    utils.prepare(sys.argv[1:],tests)

    utils.info("WMS Job Resubmission Testing")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    all_tests=utils.is_all_enabled()

    if all_tests==1 or utils.check_test_enabled(1)==1 :
        if test1(utils, tests[0]):
            fails.append(tests[0])
                
    if all_tests==1 or utils.check_test_enabled(2)==1 :
        if test2(utils, tests[1]):
            fails.append(tests[1])  

    if len(fails) > 0 :
      utils.exit_failure("%s test(s) fail(s): %s"%(len(fails), fails))
    else:
      utils.exit_success()
    
    
  
if __name__ == "__main__":
    main()
