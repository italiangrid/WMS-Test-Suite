#! /usr/bin/python

import sys
import signal
import os
import time
import traceback

from Exceptions import *

import Test_utils

COMMAND="glite-wms-job-delegate-proxy"

# check if delegation exists and try a submit
def checkdeleg(utils,delegationid):

   utils.info("Verify the delegation")
   utils.run_command_continue_on_error("glite-wms-job-info -d %s --config %s"%(delegationid,utils.get_config_file()))
   utils.info("Try a submit")
   JOBID=utils.run_command_continue_on_error("glite-wms-job-submit -d %s --config %s --nomsg %s"%(delegationid,utils.get_config_file(),utils.get_jdl_file()))
   utils.info("Cancel the unused job")
   utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))
   
   return 0


def test1(utils, title):
    
    # Test --autm-delegation option
    utils.show_progress(title)
    utils.info(title)

    try:

        output=utils.run_command_continue_on_error ("%s --autm-delegation -c %s"%(COMMAND,utils.get_config_file()))
        for line in output.splitlines():
            if line.split(":")[0].strip() == "with the delegation identifier":
                DELEGATIONID=line.split(":")[1].strip()
            
        utils.info ("Delegation Id: %s"%(DELEGATIONID))
        checkdeleg (utils,DELEGATIONID)
        utils.info("TEST PASS.")

    except (RunCommandError,GeneralError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0

  

def test2(utils, title):

  
    # Test --delegationid option
    utils.show_progress(title)
    utils.info(title)
    
    DELEGATIONID="deleg-%s"%(os.getpid())

    try:

        output=utils.run_command_continue_on_error ("%s --config %s --delegationid %s"%(COMMAND,utils.get_config_file(),DELEGATIONID))
        for line in output.splitlines():
            if line.split(":")[0].strip() == "with the delegation identifier":
                RETURNED_ID=line.split(":")[1].strip()
                break

        if RETURNED_ID == DELEGATIONID :
            utils.info("Returned delegation Id:%s"%(RETURNED_ID))
            checkdeleg (utils,RETURNED_ID)
            utils.info("TEST PASS")
        else:
            utils.error("TEST FAILS. Error, Delegation ids not match")
            raise GeneralError("Checking defined and returned delegations","Error, Delegation ids not match")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0

def test3(utils, title):

    # Create a shorter delegation
    utils.show_progress(title)
    utils.info(title)

    DELEGATIONID="deleg-%s"%(os.getpid())

    try:

        utils.set_proxy(utils.get_PROXY(),"00:10")
        utils.run_command_continue_on_error ("%s --config %s -d %s"%(COMMAND,utils.get_config_file(),DELEGATIONID))
        utils.info("Check the delegation timeleft value")
        output=utils.run_command_continue_on_error ("glite-wms-job-info -d %s --config %s"%(DELEGATIONID,utils.get_config_file()))
        
        text="NotFound"
        
        for line in output.splitlines():
            if line.split(":")[0].strip() == "Timeleft":
                text=(line.split(":")[1]).split(" ")[2]
                value=(line.split(":")[1]).split(" ")[1]
                utils.dbg("Delegation is valid for at most '%s' '%s'"%(value, text))
                break

        if  text!='min' or int(value)>10:
            utils.error("TEST FAILS. Wrong timeleft delegating proxy")
            raise GeneralError("","Wrong timeleft delegating proxy")

        checkdeleg (utils,DELEGATIONID)
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

    #try with an expiry delegation
    utils.show_progress(title)
    utils.info(title)
    
    DELEGATIONID="deleg-%s"%(os.getpid())
        
    try:

        utils.set_proxy(utils.get_PROXY(),"00:01")
        utils.run_command_continue_on_error ("%s --config %s -d %s"%(COMMAND,utils.get_config_file(),DELEGATIONID))
        utils.info("Wait until proxy expired (60secs)")
        time.sleep(60)

        # first try to delegate again with an expired proxy
        utils.info("Try to delegate with an expired proxy")
        # we expect a failure
        utils.run_command_continue_on_error("%s --config %s --autm-delegation"%(COMMAND,utils.get_config_file()), 1)

        # refresh the proxy
        utils.info("Refresh the proxy")
        utils.set_proxy (utils.get_PROXY())

        # then check if the old delegation is expired
        utils.info("Check if the old delegation is expired")
        # we expect a failure        
        utils.run_command_continue_on_error ("glite-wms-job-info  --config %s -d %s | grep Timeleft"%(utils.get_config_file(),DELEGATIONID), 1)

        # then try to submit with the expired delegation
        utils.info("Try to submit with an expired delegation")
        # we expect a failure
        output=utils.run_command_continue_on_error ("glite-wms-job-submit -d %s --config %s %s"%(DELEGATIONID,utils.get_config_file(),utils.get_jdl_file()), 1)
        utils.info("Check the output of the command")
        if output.find("The delegated Proxy has expired") == -1:
            utils.error("TEST FAILS. Job has been submitted with the expired delegation")
            return 1
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


def test5(utils, title):

    #
    utils.show_progress(title)
    utils.info(title)
        
    try:

        ###detected if ROLE attribute is set in configuration file
        utils.info("Create a proxy certificate with voms roles enabled")

        utils.set_proxy(utils.get_PROXY())

        utils.info("Use existing proxy to contact the server and to sing the new proxy")

        utils.run_command_continue_on_error("voms-proxy-init -noregen")
               
        # try to submit with the expired delegation
        utils.info("Try to submit with that proxy")
        
        JOBID=utils.run_command_continue_on_error("glite-wms-job-submit -a --config %s --nomsg %s"%(utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Job submitted successfully")

        utils.info("Cancel submitted job")

        utils.run_command_continue_on_error("glite-wms-job-cancel -c %s --noint %s"%(utils.get_config_file(),JOBID))

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

    tests=["Test 1: Check --autm-delegation option"]
    tests.append("Test 2: Check --delegationid option")
    tests.append("Test 3: Try to delegate with a short proxy and check the validity")
    tests.append("Test 4: Works with expired proxy")
    tests.append("Test 5: Works with long chain proxies (ggus ticket 79096)")

    utils = Test_utils.Test_utils(sys.argv[0],"Test delegation operation")

    utils.prepare(sys.argv[1:],tests)

    utils.info("Test delegation operation")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    all_tests=utils.is_all_enabled()

    if all_tests==1 or utils.check_test_enabled(1)==1 :
        if test1(utils, tests[0]):
            fails.append(tests[0])
                
    if all_tests==1 or utils.check_test_enabled(2)==1 :
        if test2(utils, tests[1]):
            fails.append(tests[1])
                    
    if utils.get_NOPROXY() == 0 :
    
        if all_tests==1 or utils.check_test_enabled(3)==1 :
            if test3(utils, tests[2]):
                fails.append(tests[2])
                
        if all_tests==1 or utils.check_test_enabled(4)==1 :
            if test4(utils, tests[3]):
                fails.append(tests[3])

        if all_tests==1 or utils.check_test_enabled(5)==1 :

           if utils.ROLE!='':

              if test5(utils, tests[4]):
                fails.append(tests[4])

           else:
                utils.warn("To run this test you have to set the ROLE attribute for user proxy role at configuration file")
                utils.show_progress("To run this test you have to set the ROLE attribute for user proxy role at configuration file")
                
   
    else:
      utils.warn("There are other three tests which require the user proxy password. Use -i option to enable them")
      utils.show_progress("There are other three tests which require the user proxy password. Use -i option to enable them")

    
    if len(fails) > 0 :
      utils.exit_failure("%s test(s) fail(s): %s"%(len(fails), fails))
    else:
      utils.exit_success()
      
      

if __name__ == "__main__":
    main()
