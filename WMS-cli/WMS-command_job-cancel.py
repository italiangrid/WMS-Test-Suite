#! /usr/bin/python

import sys
import signal
import time
import logging

import traceback

from Exceptions import *

import Test_utils

def check_status(utils,jobid):

    i=0

    utils.job_status(jobid)

    logging.info("Try to check the job status 5 times (for a total of 75 seconds)")

    utils.dbg("Try to check the job status 5 times (for a total of 75 seconds)")

    # try to check the status 5 times (for a total of 75 seconds)
    while ( utils.get_job_status() !="Cancelled" and i<5) :
        i=i+1
        logging.info("Wait %s seconds for the next try",(i*5))
        utils.dbg("Wait %s seconds for the next try"%(i*5))
        time.sleep(i*5)
        utils.job_status(jobid)


    # if all tries fail exit with failure

    if utils.get_job_status() !="Cancelled" :

        if utils.job_is_finished(jobid) == 0 :
           logging.error("Job's %s status is wrong: %s",jobid,utils.get_job_status())
           raise GeneralError("Check job status","Job status is wrong: %s"%(utils.get_job_status()))
        else :
           logging.warning("Job %s finished %s before cancellation.",jobid,utils.get_job_status())
           utils.warn("WARNING: Job finished (%s) before cancellation ..."%(utils.get_job_status()))

   

def main():

    fails=0
    
    utils = Test_utils.Test_utils(sys.argv[0],"Test glite-wms-job-cancel commmad")

    utils.prepare(sys.argv[1:])

    logging.info("Test glite-wms-job-cancel command")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    COMMAND="glite-wms-job-cancel"

    utils.show_progress("Test 1")
    logging.info("Test 1: Check if command %s exists"%(COMMAND))
    utils.info ("Check if command %s exists"%(COMMAND))
    utils.run_command("which %s"%(COMMAND))

    
    # Test --version option
    utils.show_progress("Test 2")

    try:

        logging.info("Test 2: Check --version option")
        utils.remove(utils.get_tmp_file())
        utils.info ("")
        utils.info ("Test --version option")
        utils.run_command_continue_on_error ("%s --version >> %s"%(COMMAND,utils.get_tmp_file()))
        utils.dbg ("Check the output command")
        version=utils.run_command_continue_on_error("grep \"WMS User Interface version\"  %s"%(utils.get_tmp_file()))
        utils.info("We are testing %s"%(version))
   
    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    utils.remove(utils.get_tmp_file())


    # jdl
    if utils.has_external_jdl() == 0:
      utils.set_long_jdl(utils.get_jdl_file())

    
    # Test --config option
    utils.show_progress("Test 3")
    
    try:

        logging.info("Test 3: Check --config option")
        utils.info ("")
        utils.info ("Test --config option")

        JOBID=utils.submit_job()

        if utils.job_is_finished(JOBID) == 0 : #cancel the job only if it is not finished
            utils.run_command_continue_on_error("%s --config %s --noint %s"%(COMMAND,utils.get_config_file(),JOBID))

        check_status(utils,JOBID)

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    utils.remove (utils.get_jobid_file()) # remove unused jobid file

    
    # Test --output option
    utils.show_progress("Test 4")

    try:

        logging.info("Test 4: Check --output option")
        utils.info ("")
        utils.info ("Test --output option")

        JOBID=utils.submit_job()

        if utils.job_is_finished(JOBID) == 0 :
            utils.run_command_continue_on_error ("%s --config %s --noint --output %s %s"%(COMMAND,utils.get_config_file(),utils.get_output_file(),JOBID))

        check_status(utils,JOBID)

        utils.info ("Check output file:")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_output_file()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    utils.remove (utils.get_jobid_file())


    # Test --logfile option
    utils.show_progress("Test 5")

    try:

        logging.info("Test 5: Check --logfile option")
        utils.info ("")
        utils.info ("Test --logfile option")

        JOBID=utils.submit_job()

        if utils.job_is_finished(JOBID) == 0 :
            utils.run_command_continue_on_error ("%s --config %s --noint --logfile %s %s"%(COMMAND,utils.get_config_file(),utils.get_log_file(),JOBID))
    
        check_status(utils,JOBID)

        utils.info("Check logfile:")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    utils.remove (utils.get_jobid_file())

    # Test --debug and --logfile option
    utils.show_progress("Test 6")

    try:

        logging.info("Test 6: Check --debug and --logfile options")
        utils.info ("")
        utils.info ("Test --debug and --logfile options")

        JOBID=utils.submit_job()

        if utils.job_is_finished(JOBID) == 0 :
            utils.run_command_continue_on_error ("%s --config %s --noint --debug --logfile %s %s"%(COMMAND,utils.get_config_file(),utils.get_log_file(),JOBID))

        check_status(utils,JOBID)


        utils.info("Check logfile:")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    utils.remove (utils.get_jobid_file())
    
    # Test --input option, submit 5 jobs
    utils.show_progress("Test 7")

    try:

        logging.info("Test 7: Check --input option")
        utils.info ("")
        utils.info ("Test --input option")

        logging.info("Submit 5 jobs")

        for i in range(5) :
            utils.submit_job()

        utils.run_command_continue_on_error("%s --config %s --noint --input %s"%(COMMAND,utils.get_config_file(),utils.get_jobid_file()))

        JOBIDS=utils.load_job_ids(utils.get_jobid_file())
    
        for JOBID in JOBIDS :

            if JOBID.startswith("http") == True:
                utils.info("Check status of %s"%(JOBID))
                check_status(utils,JOBID)

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
    
    utils.remove (utils.get_jobid_file())
      
    
    # Test all options together
    utils.show_progress("Test 8")

    try:

        logging.info("Test 8: Check all options together")
        utils.info ("")
        utils.info  ("Test all options together")

        JOBID=utils.submit_job()

        if utils.job_is_finished(JOBID) == 0 :
            utils.run_command_continue_on_error ("%s --noint --input %s --output %s --logfile %s --debug --config %s"%(COMMAND,utils.get_jobid_file(),utils.get_output_file(),utils.get_log_file(),utils.get_config_file()))

        check_status(utils,JOBID)

        utils.info  ("Check logfile:")
        logging.info("Check the logfile")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
        utils.info  ("Check outfile:")
        logging.info("Check the outfile")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_output_file()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    utils.remove (utils.get_jobid_file())
        
    # Test try to cancel a DoneOK job
    utils.show_progress("Test 9")

    try:

        logging.info("Test 9: Try to cancel a DoneOK job")

        # Use a very short job (print hostname)
        if utils.has_external_jdl() == 0 :
            utils.set_jdl(utils.get_jdl_file())
    
        utils.info ("")
        utils.info ("Try to cancel a DoneOk job")
        JOBID=utils.submit_job()
        utils.wait_until_job_finishes(JOBID)

        if utils.job_is_finished(JOBID) != 0 :
            utils.run_command_continue_on_error("%s --noint %s"%(COMMAND,JOBID),1)

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
    

    if fails > 0 :
      utils.exit_failure("%s test(s) fail(s)"%(fails))
    else:
      utils.exit_success()
    


if __name__ == "__main__":
    main()



