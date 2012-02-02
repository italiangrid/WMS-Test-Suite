#! /usr/bin/python

import sys
import signal
import logging
import traceback

from Exceptions import *

import Test_utils


def main():

    fails=0

    utils = Test_utils.Test_utils(sys.argv[0],"test glite-wms-job-list-match commmad")

    utils.prepare(sys.argv[1:])

    logging.info("Test glite-wms-job-list-match command")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    COMMAND="glite-wms-job-list-match"

    # Test if command exists
    utils.show_progress("Test 1")
    logging.info("Test 1: Check if command %s exists",COMMAND)
    utils.info("Check if command %s exists"%(COMMAND))
    utils.run_command("which %s"%(COMMAND))

   

    # Test --version option
    utils.show_progress("Test 2")

    try:

        logging.info("Test 2: Check --version option")
        utils.remove(utils.get_tmp_file())
        utils.info ("")
        utils.info ("Test --version option")
        utils.run_command_continue_on_error ("%s --version >> %s"%(COMMAND,utils.get_tmp_file()))
        utils.info ("Check the command's output")
        version=utils.run_command_continue_on_error("grep \"WMS User Interface version\"  %s"%(utils.get_tmp_file()))
        utils.info("We are testing %s"%(version))
        utils.remove(utils.get_tmp_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
   
    # Test --autm-delegation (-a) option
    utils.show_progress("Test 3")

    try:

        logging.info("Test 3: Check --autm-delegation option")
        utils.remove(utils.get_tmp_file())
        utils.info ("")
        utils.info ("Test --autm-delegation option")
        utils.run_command_continue_on_error ("%s --autm-delegation %s >> %s"%(COMMAND,utils.get_jdl_file(),utils.get_tmp_file()))
        utils.info ("Check the command's output")
        logging.info("Check the command's output")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_tmp_file()))
        utils.remove(utils.get_tmp_file())
 
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
        utils.remove(utils.get_tmp_file())
        utils.info ("")
        utils.info ("Test --config option")
        utils.run_command_continue_on_error ("%s --config %s --autm-delegation %s >> %s"%(COMMAND,utils.get_config_file(),utils.get_jdl_file(),utils.get_tmp_file()))
        utils.info ("Check the command's output")
        logging.info("Check the command's output")
        utils.run_command_continue_on_error("cat %s"%(utils.get_tmp_file()))
        utils.remove(utils.get_tmp_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
   
    # Test --endpoint option
    utils.show_progress("Test 5")

    try:

        logging.info("Test 5: Check --endpoint option")
        utils.info ("")
        utils.info ("Test --endpoint option")
        utils.run_command_continue_on_error("%s --autm-delegation --endpoint https://%s:7443/glite_wms_wmproxy_server %s >> %s"%(COMMAND,utils.get_WMS(),utils.get_jdl_file(),utils.get_tmp_file()))
        utils.info ("Check the command's output")
        logging.info("Check the command's output")
        utils.run_command_continue_on_error("cat %s"%(utils.get_tmp_file()))
        utils.remove(utils.get_tmp_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    # Test --delegationid (-d) option
    utils.show_progress("Test 6")

    try:

        logging.info("Test 6: Check --delegationid option")

        # Create delegate proxy
        Delegation="DelegationTest"
        logging.info("Create a delegate proxy")
        utils.run_command_continue_on_error("glite-wms-job-delegate-proxy -d %s"%(Delegation))

        utils.remove(utils.get_tmp_file())
        utils.info ("")
        utils.info ("Test --delegationid option")
        utils.run_command_continue_on_error ("%s --delegationid %s --config %s %s >> %s"%(COMMAND,Delegation,utils.get_config_file(),utils.get_jdl_file(),utils.get_tmp_file()))
        utils.info ("Check the command's output")
        logging.info("Check the command's output")
        utils.run_command_continue_on_error("cat %s"%(utils.get_tmp_file()))
        utils.remove(utils.get_tmp_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
  
    # Test --output option
    utils.show_progress("Test 7")

    try:

        logging.info("Test 7: Check --output option")
        utils.info ("")
        utils.info ("Test --output option")
        utils.run_command_continue_on_error("%s %s --config %s --output %s %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_output_file(),utils.get_jdl_file()))
        utils.info ("Check the output file")
        logging.info("Check the output file")
        utils.run_command_continue_on_error("cat %s"%(utils.get_output_file()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
   
    # Test --logfile option
    utils.show_progress("Test 8")

    try:

        logging.info("Test 8: Check --logfile option")
        utils.info ("")
        utils.info ("Test --logfile option")
        utils.run_command_continue_on_error("%s %s --config %s --logfile %s %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_log_file(),utils.get_jdl_file()))
        utils.info ("Check the log file")
        logging.info("Check the log file")
        utils.run_command_continue_on_error("cat %s"%(utils.get_log_file()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
    
    # Test --debug option
    utils.show_progress("Test 9")

    try:

        logging.info("Test 9: Check --debug option")
        utils.info ("")
        utils.info ("Test --debug option")
        utils.run_command_continue_on_error("%s %s --config %s --debug --logfile %s %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_log_file(),utils.get_jdl_file()))
        utils.info ("Check the log file with debug option")
        logging.info("Check the log file with debug option")
        utils.run_command_continue_on_error("cat %s"%(utils.get_log_file()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    # Test --rank option
    utils.show_progress("Test 10")

    try:

        logging.info("Test 10: Check --rank option")
        utils.remove(utils.get_tmp_file())
        utils.info ("")
        utils.info ("Test --rank option")
        utils.run_command_continue_on_error("%s %s --config %s --rank %s >> %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file(),utils.get_tmp_file()))
        utils.info ("Check the command's output")
        logging.info("Check the command's output")
        utils.run_command_continue_on_error("cat %s"%(utils.get_tmp_file()))
        utils.remove(utils.get_tmp_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
       

    # Test all options together
    utils.show_progress("Test 11")

    try:

        logging.info("Test 11: Check all options together")
        utils.info ("")
        utils.info ("Test all options together")
        utils.run_command_continue_on_error("%s %s --noint --logfile %s --output %s --endpoint https://%s:7443/glite_wms_wmproxy_server %s"%(COMMAND,utils.get_delegation_options(),utils.get_log_file(),utils.get_output_file(),utils.get_WMS(),utils.get_jdl_file()))
        utils.info ("Check the output file")
        logging.info("Check the output file")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_output_file()))
        utils.remove(utils.get_output_file())
        utils.info ("Check the log file")
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
    

    # Test :  try a failure matching
    utils.show_progress("Test 12")

    try:

        logging.info("Test 12: Try a failure matching (Requirements==false)")
        utils.remove(utils.get_tmp_file())
        utils.info ("")
        utils.info ("Try a failure matching (Requirements == false)")
        utils.set_requirements ("\"false\"")
        utils.run_command_continue_on_error("%s %s --config %s %s >> %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file(),utils.get_tmp_file()))
        utils.info ("Check command's output")
        utils.run_command_continue_on_error("grep \"No Computing Element matching your job requirements has been found!\" %s"%(utils.get_tmp_file()))
        utils.remove(utils.get_tmp_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    # Test : try a restricted requirements
    utils.show_progress("Test 13")

    try:

        logging.info("Test 13: Match only CREAM CE")
        utils.remove(utils.get_tmp_file())
        utils.info ("")
        utils.info ("Match only Cream CE")
        utils.set_requirements ("regexp(\"8443/cream-\", other.GlueCEUniqueID)")
        utils.run_command_continue_on_error("%s %s --debug --config %s %s >> %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file(),utils.get_tmp_file()))
        utils.info ("Look for LCG-CE in the command output")
        logging.info("Look for LCG-CE in the command output")
        utils.run_command_continue_on_error("grep \"2118/jobmanager-\" %s"%(utils.get_tmp_file()),1)
        utils.remove(utils.get_tmp_file())

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
