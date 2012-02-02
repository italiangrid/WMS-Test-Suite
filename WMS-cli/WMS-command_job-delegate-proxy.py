#! /usr/bin/python

import sys
import signal
import os
import time
import logging
import traceback

from Exceptions import *


import Test_utils

# check if delegation exists and try a submit
def checkdeleg(utils,delegationid):

   logging.info("Check if delegation %s exists , try a submit and finally cancel the unused job",delegationid)

   utils.info ("Verify the delegation")
   utils.run_command_continue_on_error("glite-wms-job-info -d %s --config %s"%(delegationid,utils.get_config_file()))
   utils.info ("Try a submit")
   JOBID=utils.run_command_continue_on_error("glite-wms-job-submit -d %s --config %s --nomsg %s"%(delegationid,utils.get_config_file(),utils.get_jdl_file()))
   utils.info ("Cancel the unused job")
   utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))


def main():

    fails=0

    utils = Test_utils.Test_utils(sys.argv[0],"test glite-wms-job-delegate-proxy commmad")

    utils.prepare(sys.argv[1:])

    logging.info("Test glite-wms-job-delegate-proxy command")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    COMMAND="glite-wms-job-delegate-proxy"

    DELEGATIONID="deleg-%s"%(os.getpid())

    logging.info("Delegation Id for testing %s",DELEGATIONID)

    utils.info(DELEGATIONID)

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
        utils.info ("Check the output command")
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

    # Test --autm-delegation option
    utils.show_progress("Test 3")

    try:
        utils.remove(utils.get_tmp_file())
        logging.info("Test 3: Check --autm-delegation option")
        utils.info ("")
        utils.info ("Test option --autm-delegation")
        utils.run_command_continue_on_error ("%s --autm-delegation >> %s"%(COMMAND,utils.get_tmp_file()))
        DELEGATIONID=utils.run_command_continue_on_error("awk -F ' ' '/delegation/ {print $NF}' %s"%(utils.get_tmp_file()))
        utils.info ("Delegation Id: %s"%(DELEGATIONID))
        checkdeleg (utils,DELEGATIONID)
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

        utils.remove(utils.get_tmp_file())
        logging.info("Test 4: Check --config option")
        utils.info ("")
        utils.info ("Test option --config")
        utils.run_command_continue_on_error ("%s --autm-delegation --config %s >> %s"%(COMMAND,utils.get_config_file(),utils.get_tmp_file()))
        DELEGATIONID=utils.run_command_continue_on_error("awk -F ' ' '/delegation/ {print $NF}' %s"%(utils.get_tmp_file()))
        utils.info ("Delegation Id: %s"%(DELEGATIONID))
        checkdeleg (utils,DELEGATIONID)
        utils.remove(utils.get_tmp_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    
    #Test --delegationid option
    utils.show_progress("Test 5")

    try:

        utils.remove(utils.get_tmp_file())
        logging.info("Test 5: Check --delegationid option")
        utils.info ("")
        utils.info ("Test option --delegationid ")
        utils.run_command_continue_on_error ("%s --config %s --delegationid %s >> %s"%(COMMAND,utils.get_config_file(),DELEGATIONID,utils.get_tmp_file()))
        
        RETURNED_ID=utils.run_command_continue_on_error("awk -F ' ' '/delegation/ {print $NF}' %s"%(utils.get_tmp_file()))
    
        if RETURNED_ID == DELEGATIONID :
            logging.info("Returned delegation Id is : %s",RETURNED_ID)
            utils.info ("Returned delegation Id: %s"%(RETURNED_ID))
            checkdeleg (utils,RETURNED_ID)
            utils.remove(utils.get_tmp_file())
        else:
            logging.error("Delegation ids does not match. One is %s and the other is %s",RETURNED_ID,DELEGATIONID)
            raise GeneralError("Chech delegation ids","Error, Delegation ids does not match")

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    #Test --output option
    utils.show_progress("Test 6")

    try:

        logging.info("Test 6: Check --output option")
        utils.info ("")
        utils.info ("Test option --output")
        utils.run_command_continue_on_error ("%s --config %s --output %s --delegationid %s >> %s"%(COMMAND,utils.get_config_file(),utils.get_output_file(),DELEGATIONID,utils.get_tmp_file()))
        utils.info ("Check the output command")
        utils.run_command_continue_on_error("cat %s"%(utils.get_output_file()))
        checkdeleg (utils,DELEGATIONID)

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
    
    
    #Test --logfile option
    utils.show_progress("Test 7")

    try:

        logging.info("Test 7: Check --logfile option")
        utils.info ("")
        utils.info ("Test option --logfile")
        utils.run_command_continue_on_error ("%s --config %s --logfile %s -d %s"%(COMMAND,utils.get_config_file(),utils.get_log_file(),DELEGATIONID))
        utils.info ("Check logfile")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
        checkdeleg (utils,DELEGATIONID)
        utils.remove (utils.get_log_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
        

    #Test --debug and --logfile
    utils.show_progress("Test 8")

    try:

        logging.info("Test 8: Check --debug and --logfile options")
        utils.info ("")
        utils.info ("Test options --debug and --logfile")
        utils.run_command_continue_on_error ("%s --config %s --debug --logfile %s -d %s"%(COMMAND,utils.get_config_file(),utils.get_log_file(),DELEGATIONID))
        utils.info ("Check logfile")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
        checkdeleg (utils,DELEGATIONID)
        utils.remove (utils.get_log_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    
    #Test --endpoint option
    utils.show_progress("Test 9")

    try:

        logging.info("Test 9: Check --endpoint option")
        utils.remove(utils.get_output_file())
        utils.info ("")
        utils.info ("Test option --endpoint")
        utils.run_command_continue_on_error("%s --endpoint https://%s:7443/glite_wms_wmproxy_server --output %s -d %s"%(COMMAND,utils.get_WMS(),utils.get_output_file(),DELEGATIONID))
        endpoint=utils.run_command_continue_on_error("awk -F ' ' ' /WMProxy/ {print $NF}' %s"%(utils.get_output_file()))

        logging.info("Used endpoint is %s",endpoint)

        if endpoint != "https://%s:7443/glite_wms_wmproxy_server"%(utils.get_WMS()) :
            logging.error("Wrong endpoint delegating proxy. Specified %s while used %s","https://%s:7443/glite_wms_wmproxy_server"%(utils.get_WMS()) ,endpoint)
            raise GeneralError ("Check used endpoint","Wrong endpoint delegating proxy")
   
        checkdeleg (utils,DELEGATIONID)
        utils.remove(utils.get_output_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    #Test all options
    utils.show_progress("Test 10")

    try:

        logging.info("Test 10: Check all options together")
        utils.info ("")
        utils.info ("Test all options together")
        utils.run_command_continue_on_error ("%s --noint --output %s --logfile %s --config %s --endpoint https://%s:7443/glite_wms_wmproxy_server -d %s"%(COMMAND,utils.get_output_file(),utils.get_log_file(),utils.get_config_file(),utils.get_WMS(),DELEGATIONID))
        RETURNED_ID=utils.run_command_continue_on_error("awk -F ' ' '/delegation/ {print $NF}' %s"%(utils.get_output_file()))

        if RETURNED_ID == DELEGATIONID :

            utils.info ("Check the output")
            utils.run_command_continue_on_error ("cat %s"%(utils.get_output_file()))
            utils.info ("Check the logfile")
            utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
            utils.info ("Returned delegation Id: %s"%(RETURNED_ID))
            checkdeleg (utils,DELEGATIONID)
            utils.remove (utils.get_log_file())
            utils.remove (utils.get_output_file())

        else:
            raise GeneralError("Check delegation ids","Error, Delegation ids does not match")

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    # for the next tests we need user proxy password

    if utils.get_NOPROXY() == 0 :

       utils.show_progress("Test 11")

       try:

            logging.info("Test 11: Try to delegate with a short proxy and check the validity")
            # Create a shorter delegation
            utils.set_proxy(utils.get_PROXY(),"00:10")
            utils.info ("")
            utils.info ("Try to delegate with a short proxy and check the validity")
            utils.run_command_continue_on_error ("%s --config %s -d %s"%(COMMAND,utils.get_config_file(),DELEGATIONID))
            utils.info ("Check the delegation timeleft value")
            utils.run_command_continue_on_error ("glite-wms-job-info -d %s --config %s --output %s"%(DELEGATIONID,utils.get_config_file(),utils.get_output_file()))

            text=utils.run_command_continue_on_error("grep -m 1 Timeleft %s | awk '{print $4}'"%(utils.get_output_file()))
            value=utils.run_command_continue_on_error("grep -m 1 Timeleft %s | awk '{print $3}'"%(utils.get_output_file()))

            utils.remove (utils.get_output_file())

            if  text!='min' or int(value)>10:
                logging.error("Wrong timeleft delegating proxy")
                raise GeneralError("","Wrong timeleft delegating proxy")

            checkdeleg (utils,DELEGATIONID)

       except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


       # try with an expiry delegation
       utils.show_progress("Test 12")

       try:

            logging.info("Test 12: Works with expiring proxy...")
            utils.set_proxy(utils.get_PROXY(),"00:01")
            utils.info ("")
            utils.info ("Works with expiring proxy...")
            utils.run_command_continue_on_error ("%s --config %s -d %s"%(COMMAND,utils.get_config_file(),DELEGATIONID))
            utils.info ("Wait until proxy expired...")
            logging.info("Wait until proxy expired ...")
            time.sleep(60)

            # first try to delegate again with an expired proxy
            utils.info ("Try to delegate with an expired proxy")
            utils.run_command_fail_continue_on_error("%s --config %s --autm-delegation"%(COMMAND,utils.get_config_file()))

            # refresh the proxy
            utils.set_proxy (utils.get_PROXY(),"")

            # then check if the old delegation is expired
            utils.info ("Check if the old delegation is expired")
            utils.run_command_fail_continue_on_error ("glite-wms-job-info  --config %s -d %s | grep Timeleft"%(utils.get_config_file(),DELEGATIONID))

            # then try to submit with the expired delegation
            utils.info ("Try to submit with an expired delegation")
            utils.run_command_fail_continue_on_error ("glite-wms-job-submit -d %s --config %s --logfile %s %s"%(DELEGATIONID,utils.get_config_file(),utils.get_log_file(),utils.get_jdl_file()))
            utils.info ("Check the output of the command")
            utils.run_command_continue_on_error ("grep \"The delegated Proxy has expired\" %s"%(utils.get_log_file()))
            utils.remove(utils.get_log_file())
       
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
