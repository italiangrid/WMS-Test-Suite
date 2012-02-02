#! /usr/bin/python

import sys
import signal
import time
import os
import commands
import traceback

from Exceptions import *

import Test_utils
import Job_utils

# On failure raise a GeneralError exception
def check_status(utils,jobid):

    i=0

    utils.job_status(jobid)

    utils.info("Try to check the status 6 times (for a total of 100 seconds)")

    # try to check the status 6 times (for a total of 100 seconds)
    while ( utils.get_job_status().find("Cancelled")==-1 and i<6) :
        if utils.job_is_finished(jobid) :
            # final status is wrong test should fails!!!
            utils.warn("Job %s final status is: %s."%(jobid,utils.get_job_status()))
            break          
        i+=1
        time.sleep(i*5)
        utils.info("Wait %s seconds for the next try"%(i*5))
        utils.job_status(jobid)
        
    # All the retries fail, raise exception
    if utils.job_is_finished(jobid) == 0 :
        utils.error("TEST FAILS. Job's %s status is wrong: %s"%(jobid,utils.get_job_status()))
        raise GeneralError("Check job status","Job status is wrong: %s"%(utils.get_job_status()))

    if utils.job_is_finished(jobid) == 3:
        return 0
        
    # final status is wrong test should fails!!!
    return 0 


def test1(utils, title):

    # Cancel a normal job
    utils.show_progress(title)
    utils.info(title)

    try:
        
        utils.set_long_jdl(utils.get_jdl_file())

        JOBID=utils.submit_job()
        
        utils.info("Job %s has been submitted successfully."%(JOBID))

        if utils.job_is_finished(JOBID) == 0 :
            utils.run_command_continue_on_error("glite-wms-job-cancel --config %s --noint %s"%(utils.get_config_file(),JOBID))

        if not check_status(utils,JOBID):
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

    # Cancel a DAG job
    utils.show_progress(title)
    utils.info(title)

    try:

        # create dag nodes jdl files
        utils.set_dag_jdl(utils.get_jdl_file())

        utils.dbg("Submit a DAG job")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("DAG %s has been submitted successfully."%(JOBID))

        utils.dbg("Wait 10 secs")
        time.sleep(10)

        utils.run_command_continue_on_error("glite-wms-job-cancel --config %s --noint %s"%(utils.get_config_file(),JOBID))

        if not check_status(utils,JOBID):
            utils.info("TEST PASS")

    except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            return 1

    return 0


def test3(utils, title):

    # Cancel one node of a DAG job
    utils.show_progress(title)
    utils.info(title)
    
    try:

        # create dag nodes jdl files
        utils.set_dag_jdl(utils.get_jdl_file())

        utils.dbg("Submit a DAG job")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("DAG %s has been submitted successfully."%(JOBID))

        utils.dbg("Wait 30 secs")
        time.sleep(30)

        # Get nodes' ids

        output=commands.getoutput("glite-wms-job-status %s"%(JOBID))
        
        IDS=[]
        for line in output.splitlines():
            if line.split(":",1)[0].strip() == "Status info for the Job":
                IDS.append(line.split(":",1)[1].strip())
                utils.dbg("Next node's id is: %s"%(IDS[-1]))

        utils.info("Now try to cancel the first node")
        # IDS[0] is the dag ID
        utils.run_command_continue_on_error("glite-wms-job-cancel --config %s --noint %s"%(utils.get_config_file(),IDS[1]))

        if not check_status(utils,IDS[1]):
            utils.info("TEST PASS")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0
    


def test4(utils, title):

    # Cancel a collection job
    utils.show_progress(title)
    utils.info(title)

    try:

        utils.set_long_jdl(utils.get_jdl_file())
        
        Job_utils.prepare_collection_job(utils,utils.get_jdl_file())

        utils.dbg("Submit a collection job")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg --collection %s/collection_jdls"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_tmp_dir()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        utils.dbg("Wait 30 secs")
        time.sleep(30)

        utils.run_command_continue_on_error("glite-wms-job-cancel --config %s --noint %s"%(utils.get_config_file(),JOBID))

        # Get nodes' ids

        output=commands.getoutput("glite-wms-job-status %s"%(JOBID))
        
        IDS=[]
        for line in output.splitlines():
            if line.split(":",1)[0].strip() == "Status info for the Job":
                IDS.append(line.split(":",1)[1].strip())
                utils.dbg("Next node's id is: %s"%(IDS[-1]))

        for job in IDS:
            check_status(utils,job)
            
        utils.info("TEST PASS")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    os.system("rm -rf %s/collection_jdls/"%(utils.get_tmp_dir()))

    return 0


def test5(utils, title):

    # Cancel node of a collection job
    utils.show_progress(title)
    utils.info(title)  
    
    try:

        utils.set_long_jdl(utils.get_jdl_file())
        
        Job_utils.prepare_collection_job(utils,utils.get_jdl_file())

        utils.dbg("Submit a collection job")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg --output %s --collection %s/collection_jdls"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_output_file(),utils.get_tmp_dir()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        utils.dbg("Wait 30 secs")
        time.sleep(30)      

        # Get nodes' ids

        output=commands.getoutput("glite-wms-job-status %s"%(JOBID))
        
        IDS=[]
        for line in output.splitlines():
            if line.split(":",1)[0].strip() == "Status info for the Job":
                IDS.append(line.split(":",1)[1].strip())
                utils.dbg("Next node's id is: %s"%(IDS[-1]))

        utils.info("Now try to cancel the first node")
        # IDS[0] is the collection ID 
        utils.run_command_continue_on_error("glite-wms-job-cancel --config %s --noint %s"%(utils.get_config_file(),IDS[1]))

        if not check_status(utils,IDS[1]):
            utils.info("TEST PASS")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    os.system("rm -rf %s/collection_jdls/"%(utils.get_tmp_dir()))

    return 0



def test6(utils, title):

    # Cancel a parametric job
    utils.show_progress(title)
    utils.info(title) 

    try:

        # create parametric jdl and required files
        utils.set_parametric_jdl(utils.get_jdl_file())

        utils.dbg("Submit a parametric job")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        utils.dbg("Wait 30 secs")
        time.sleep(30)  

        utils.run_command_continue_on_error("glite-wms-job-cancel --config %s --noint %s"%(utils.get_config_file(),JOBID))

        # Get nodes' ids

        output=commands.getoutput("glite-wms-job-status %s"%(JOBID))
        
        IDS=[]
        for line in output.splitlines():
            if line.split(":",1)[0].strip() == "Status info for the Job":
                IDS.append(line.split(":",1)[1].strip())
                utils.dbg("Next node's id is: %s"%(IDS[-1]))

        for job in IDS:
            check_status(utils,job)
            
        utils.info("TEST PASS")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    os.system("rm -f %s/input*"%(utils.get_tmp_dir()))

    return 0

   
def test7(utils, title):

    # Cancel one node of a parametric job
    utils.show_progress(title)
    utils.info(title)     

    try:

        # create parametric jdl and required files
        utils.set_parametric_jdl(utils.get_jdl_file())

        utils.dbg("Submit a parametric job")
        
        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        utils.dbg("Wait 10 secs")
        time.sleep(10)  
        
        # Get nodes' ids

        output=commands.getoutput("glite-wms-job-status %s"%(JOBID))
        
        IDS=[]
        for line in output.splitlines():
            if line.split(":",1)[0].strip() == "Status info for the Job":
                IDS.append(line.split(":",1)[1].strip())
                utils.dbg("Next node's id is: %s"%(IDS[-1]))
                
        utils.info("Now try to cancel the first node")
        # IDS[0] is the parametric job ID 
        utils.run_command_continue_on_error("glite-wms-job-cancel --config %s --noint %s"%(utils.get_config_file(),IDS[1]))

        if not check_status(utils,IDS[1]):
            utils.info("TEST PASS")             

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    os.system("rm -f %s/input*"%(utils.get_tmp_dir()))

    return 0


def test8(utils, title):

    # Cancel a MPI job
    utils.show_progress(title)
    utils.info(title) 
    try:

        # create mpi jdl and required files
        utils.set_mpi_jdl(utils.get_jdl_file())

        utils.dbg("Submit a MPI job")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        utils.dbg("Wait 10 secs")
        time.sleep(10)

        utils.run_command_continue_on_error("glite-wms-job-cancel --config %s --noint %s"%(utils.get_config_file(),JOBID))

        if not check_status(utils,JOBID):
            utils.info("TEST PASS")             


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0


def test9(utils, title):
    
    # Test try to cancel a DoneOK job
    utils.show_progress
    utils.info(title) 

    try:
        
        # Use a very short job (print hostname)
        utils.set_jdl(utils.get_jdl_file())

        JOBID=utils.submit_job()
        utils.wait_until_job_finishes(JOBID)

        if utils.job_is_finished(JOBID) != 0 :
            # we expect a failure
            utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID),1)
            utils.info("TEST PASS")

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

    tests=["Test 1: Try to cancel a normal job"]
    tests.append("Test 2: Try to cancel a DAG job")
    tests.append("Test 3: Try to cancel one node of a DAG job")
    tests.append("Test 4: Try to cancel a collection job")
    tests.append("Test 5: Try to cancel one node of a collection job")
    tests.append("Test 6: Try to cancel a parametric job")
    tests.append("Test 7: Try to cancel one node of a parametric job")
    tests.append("Test 8: Try to cancel a MPI job")
    tests.append("Test 9: Try to cancel a DoneOK job")

    utils = Test_utils.Test_utils(sys.argv[0],"WMS Job Cancel Testing")

    utils.prepare(sys.argv[1:],tests)

    utils.info("WMS Job Cancel Testing")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    all_tests=utils.is_all_enabled()

    if all_tests==1 or utils.check_test_enabled(1)==1 :
        if test1(utils, tests[0]):
            fails.append(tests[0])
                
    if all_tests==1 or utils.check_test_enabled(2)==1 :
        if test2(utils, tests[1]):
            fails.append(tests[1])
            
    if all_tests==1 or utils.check_test_enabled(3)==1 :
        if test3(utils, tests[2]):
            fails.append(tests[2])
                
    if all_tests==1 or utils.check_test_enabled(4)==1 :
        if test4(utils, tests[3]):
            fails.append(tests[3])
            
    if all_tests==1 or utils.check_test_enabled(5)==1 :
        if test5(utils, tests[4]):
            fails.append(tests[4])
                
    if all_tests==1 or utils.check_test_enabled(6)==1 :
        if test6(utils, tests[5]):
            fails.append(tests[5])
            
    if all_tests==1 or utils.check_test_enabled(7)==1 :
        if test7(utils, tests[6]):
            fails.append(tests[6])
                
    if all_tests==1 or utils.check_test_enabled(8)==1 :
        if test8(utils, tests[7]):
            fails.append(tests[7])
            
    if all_tests==1 or utils.check_test_enabled(9)==1 :
        if test9(utils, tests[8]):
            fails.append(tests[8])                      

    if len(fails) > 0 :
      utils.exit_failure("%s test(s) fail(s): %s"%(len(fails), fails))
    else:
      utils.exit_success()
   

if __name__ == "__main__":
    main()




