#! /usr/bin/python

import sys
import signal
import time
import os
import logging
import traceback

from Exceptions import *

import Test_utils


def main():

    fails=0

    utils = Test_utils.Test_utils(sys.argv[0],"test glite-wms-job-logging-info commmad")

    utils.prepare(sys.argv[1:])

    logging.info("Test glite-wms-job-logging-info command")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    COMMAND="glite-wms-job-logging-info"

    START=time.strftime("%H:%M")
    
    utils.show_progress("Test 1")
    logging.info("Test 1: Check if command %s exists",COMMAND)
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
        utils.info ("Check the output command")
        version=utils.run_command_continue_on_error("grep \"User Interface version\"  %s"%(utils.get_tmp_file()))
        utils.info("We are testing %s"%(version))
        utils.remove(utils.get_tmp_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    utils.info ("Submit a job")
    logging.info("Submit a job")

    JOBID=utils.run_command ("glite-wms-job-submit %s --config %s --nomsg --output %s %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jobid_file(),utils.get_jdl_file()))

    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

    # Test a simple logging info operation
    utils.show_progress("Test 3")

    try:

        logging.info("Test 3: Test a simple logging info operation")
        utils.info ("")
        utils.info ("Test a simple logging info operation")
        utils.run_command_continue_on_error ("%s %s"%(COMMAND,JOBID))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    # Test --config option
    utils.show_progress("Test 4")

    try:

        logging.info("Test 4: Check --config option")
        utils.info ("")
        utils.info ("Test option --config")
        utils.run_command_continue_on_error ("%s --config %s %s"%(COMMAND,utils.get_config_file(),JOBID))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    # Test --output option
    utils.show_progress("Test 5")

    try:

        logging.info("Test 5: Check --output option")
        utils.info ("")
        utils.info ("Test option --output")
        utils.run_command_continue_on_error ("%s --output %s --config %s %s"%(COMMAND,utils.get_output_file(),utils.get_config_file(),JOBID))
        utils.info ("Check the output file")
        logging.info("Check the output file")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_output_file()))
        utils.remove(utils.get_output_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    # Test --logfile option
    utils.show_progress("Test 6")

    try:

        logging.info("Test 6: Check --logfile option")
        utils.info ("")
        utils.info ("Test option --logfile")
        utils.run_command_continue_on_error ("%s --logfile %s --config %s %s"%(COMMAND,utils.get_log_file(),utils.get_config_file(),JOBID))
        utils.info ("Check the log file")
        logging.info("Check the log file")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
        utils.remove(utils.get_log_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    # Test --debug and --logfile options
    utils.show_progress("Test 7")

    try:

        logging.info("Test 7: Check --debug and --logfile options")
        utils.info ("")
        utils.info ("Test options --debug and --logfile")
        utils.run_command_continue_on_error ("%s --debug --logfile %s --output %s %s"%(COMMAND,utils.get_log_file(),utils.get_output_file(),JOBID))
        utils.info ("Check the log file with debug option enabled")
        logging.info("Check the log file with debug option enabled")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
        utils.info ("Check the output file with debug option enabled")
        logging.info("Check the output file with debug option enabled")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_output_file()))
        utils.remove(utils.get_output_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    # Test --verbosity [0|1|2|3] option
    utils.show_progress("Test 8")

    try:

        logging.info("Test 8: Check --verbosity option")
        utils.info ("")
        utils.info ("Test option --verbosity")

        for i in range(4) :

            utils.run_command_continue_on_error ("%s --verbosity %d --output %s %s"%(COMMAND,i,utils.get_output_file(),JOBID))
            utils.info ("Check the output file with verbosity %d option"%(i))
            logging.info("Check the output file with verbosity %d option",i)
            utils.run_command_continue_on_error ("cat %s"%(utils.get_output_file()))
            utils.remove(utils.get_output_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
    
    # Test --input option
    utils.show_progress("Test 9")

    try:

        logging.info("Test 9: Check --input option")

        utils.info ("Submit 2 jobs")
        logging.info("Submit 2 jobs and save their ids in file %s",utils.get_jobid_file())
        utils.run_command_continue_on_error ("glite-wms-job-submit %s --output %s %s"%(utils.get_delegation_options(),utils.get_jobid_file(),utils.get_jdl_file()))
        utils.run_command_continue_on_error ("glite-wms-job-submit %s --output %s %s"%(utils.get_delegation_options(),utils.get_jobid_file(),utils.get_jdl_file()))

        utils.info ("")
        utils.info ("Test the --input option")
        utils.run_command_continue_on_error ("%s --noint --config %s --input %s"%(COMMAND,utils.get_config_file(),utils.get_jobid_file()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    utils.info("Sleep for 60 secs")
    time.sleep (60)
    
    NOW = time.strftime("%H:%M")
    
    # Test --to option
    utils.show_progress("Test 10")

    try:

        logging.info("Test 10: Check --to option")
        utils.info ("")
        utils.info ("Test the --to option")
        # this test fails on gLite UI 3.2.2
        utils.run_command_continue_on_error ("%s --config %s --to %s %s"%(COMMAND,utils.get_config_file(),NOW,JOBID))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    # Test --from option
    utils.show_progress("Test 11")

    try:

        logging.info("Test 11: Check --from option")
        utils.info ("")
        utils.info ("Test the --from option")
        utils.run_command_continue_on_error ("%s --config %s --from %s %s"%(COMMAND,utils.get_config_file(),START,JOBID))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    # Test --event option
    utils.show_progress("Test 12")

    try:

        logging.info("Test 12: Test the --event option (show only ACCEPTED events)")
        utils.info ("")
        utils.info ("Test the --event option (show only ACCEPTED events)")
        utils.run_command_continue_on_error ("%s  --config %s --event ACCEPTED %s | grep \"Event: Accepted\""%(COMMAND,utils.get_config_file(),JOBID))
   
    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    # Test --exclude option
    utils.show_progress("Test 13")

    try:

        logging.info("Test 13: Test the --exclude option (exclude ACCEPTED events)")
        utils.info ("")
        utils.info ("Test the --exclude option (exclude ACCEPTED events)")
        utils.run_command_continue_on_error ("%s --config %s --exclude ACCEPTED %s | grep \"Event: Accepted\""%(COMMAND,utils.get_config_file(),JOBID),1)

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    # Test --user-tag option
    os.system("echo \"\nusertags = [ type = \'test job\' ];\" >> %s"%(utils.get_jdl_file()))

    utils.show_progress("Test 14")

    try:

        logging.info("Test 14: Check --user-tag option")
        utils.info ("")
        utils.info ("Test the --user-tag option ")
        utils.run_command_continue_on_error ("%s  --config %s --user-tag type=\'test job\' %s"%(COMMAND,utils.get_config_file(),JOBID))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
        
    # Test all options together
    utils.show_progress("Test 15")

    try:

        logging.info("Test 15: Test all options together")
        utils.info ("")
        utils.info ("Test all the options together (extract only EnQueued events)")
        utils.run_command_continue_on_error ("%s --noint --input %s --output %s --logfile %s --config %s --verbosity 3 --from %s --to %s --event EnQueued"%(COMMAND,utils.get_jobid_file(),utils.get_output_file(),utils.get_log_file(),utils.get_config_file(),START,NOW))
        utils.info ("Check the log file")
        logging.info("Check the log file")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
        utils.info ("Check the output file")
        logging.info("Check the output file")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_output_file()))

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
