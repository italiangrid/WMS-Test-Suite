#! /usr/bin/python

import os
import time
import sys
import signal
import logging
import traceback

from Exceptions import *


import Test_utils


def main():

    fails=0

    utils = Test_utils.Test_utils(sys.argv[0],"test glite-wms-job-status commmad")

    logging.info("Test glite-wms-job-status command")

    utils.prepare(sys.argv[1:])

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    COMMAND="glite-wms-job-status"

    utils.show_progress("Test 1")
    logging.info("Test 1: Check if command %s exists",COMMAND)
    utils.info ("Check if command %s exists"%(COMMAND))
    utils.run_command_continue_on_error ("which %s"%(COMMAND))


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
    JOBID=utils.run_command ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)
    
    # Test a simple status
    utils.show_progress("Test 3")

    try:

        logging.info("Test 3: Test a simple status operation")
        utils.info ("")
        utils.info ("Test a simple status...")
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
        utils.run_command_continue_on_error ("%s --config %s --output %s %s"%(COMMAND,utils.get_config_file(),utils.get_output_file(),JOBID))
        utils.info("Check the output file")
        logging.info("Check the output file")
        utils.run_command_continue_on_error("cat %s"%(utils.get_output_file()))
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
        utils.run_command_continue_on_error ("%s --config %s --logfile %s %s"%(COMMAND,utils.get_config_file(),utils.get_log_file(),JOBID))
        utils.info("Check the log file")
        logging.info("Check the log file")
        utils.run_command_continue_on_error("cat %s"%(utils.get_log_file()))
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
        utils.info ("Test options --debug and --logfile ")
        utils.run_command_continue_on_error ("%s --config %s --debug --logfile %s %s"%(COMMAND,utils.get_config_file(),utils.get_log_file(),JOBID))
        utils.info("Check the log file with debug option enabled")
        logging.info("Check the log file with debug option enabled")
        utils.run_command_continue_on_error("cat %s"%(utils.get_log_file()))
        utils.remove(utils.get_log_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
    
    # Test --verbosity option
    utils.show_progress("Test 8")

    try:

        logging.info("Test 8: Check --verbosity option")
        utils.info ("")
        utils.info ("Test option --verbosity [0|1|2|3] ")

        for i in range(4):

            utils.run_command_continue_on_error ("%s --config %s --verbosity %d --output %s %s"%(COMMAND,utils.get_config_file(),i,utils.get_output_file(),JOBID))
            utils.info("Check the command's output")
            logging.info("Check the command's output")
            utils.run_command_continue_on_error("cat %s"%(utils.get_output_file()))
            utils.remove(utils.get_output_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    # Test --input option
    utils.info ("Submit some jobs")
    logging.info("Submit 3 jobs")
    utils.run_command ("glite-wms-job-submit %s --output %s --config %s %s"%(utils.get_delegation_options(),utils.get_jobid_file(),utils.get_config_file(),utils.get_jdl_file()))
    utils.run_command ("glite-wms-job-submit %s --output %s --config %s %s"%(utils.get_delegation_options(),utils.get_jobid_file(),utils.get_config_file(),utils.get_jdl_file()))
    utils.run_command ("glite-wms-job-submit %s --output %s --config %s %s"%(utils.get_delegation_options(),utils.get_jobid_file(),utils.get_config_file(),utils.get_jdl_file()))

    utils.show_progress("Test 9")

    try:

        logging.info("Test 9: Check --input option")
        utils.info ("")
        utils.info ("Test the --input option")
        utils.run_command_continue_on_error ("%s --noint --config %s --output %s --input %s"%(COMMAND,utils.get_config_file(),utils.get_output_file(),utils.get_jobid_file()))
        utils.info("Check the command's output")
        logging.info("Check the command's output")
        utils.run_command_continue_on_error("cat %s"%(utils.get_output_file()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    utils.show_critical("")
    utils.show_critical("==========================================================================================================")
    utils.show_critical("BEWARE: The following tests require certain indexing capabilities to be enabled on the LB server!")
    utils.show_critical("=======================================================================================================--=")
    utils.show_critical("")

    utils.set_requirements("\"false\"")
    os.system("echo \"\nusertags = [ type = \'test job\' ];\" >> %s"%(utils.get_jdl_file()))

    logging.info("Submit a job")

    utils.run_command("glite-wms-job-submit %s --config %s --output %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jobid_file(),utils.get_jdl_file()))

    JOBID=utils.run_command("tail -1 %s"%(utils.get_jobid_file()))

    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

    utils.info("Waiting until job arrives to the expected status.")

    utils.job_status(JOBID)

    while utils.get_job_status().find("Waiting") == -1: 
        utils.job_status(JOBID)
        time.sleep(5)

    utils.show_progress("Test 10")

    try:

        logging.info("Test 10: Check --exclude option (exclude Waiting,Done,Cleared and Aborted jobs")
        utils.info ("")
        utils.info ("Test the --exclude option (exclude Waiting,  Done, Cleared and Aborted jobs)")
        OUTPUT=utils.run_command_continue_on_error ("%s --noint --config %s --all --exclude Waiting --exclude Done --exclude 8 --exclude 7"%(COMMAND,utils.get_config_file()))
        utils.run_command_continue_on_error_fail("grep %s %s"%(JOBID,OUTPUT))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    utils.show_progress("Test 11")

    try:

        logging.info("Test 11: Check --status option (look for Waiting job)")
        utils.info ("")
        utils.info ("Test the --status option (look for Waiting job)")
        OUTPUT=utils.run_command_continue_on_error ("%s --noint --config %s --all --status Waiting"%(COMMAND,utils.get_config_file()))
        utils.run_command_continue_on_error ("grep %s %s"%(JOBID,OUTPUT))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    utils.show_progress("Test 12")

    try:

        logging.info("Test 12: Check --user-tag option")
        utils.info ("")
        utils.info ("Test the --user-tag option")
        OUTPUT=utils.run_command_continue_on_error ("%s --noint --config %s -all --user-tag type=\'test job\'"%(COMMAND,utils.get_config_file()))
        utils.run_command_continue_on_error ("grep %s %s"%(JOBID,OUTPUT))
        utils.run_command_fail_continue_on_error ("%s --noint --config %s --all --user-tag type=\"wrong tag\""%(COMMAND,utils.get_config_file()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    """
    utils.show_progress("Test 13")
    utils.info ("")
    utils.info ("Test the --to option")


    utils.show_progress("Test 14")
    utils.info ("")
    utils.info ("Test the --from option")
    """

    if fails > 0 :
      utils.exit_failure("%s test(s) fail(s)"%(fails))
    else:
      utils.exit_success()


if __name__ == "__main__":
   main()
