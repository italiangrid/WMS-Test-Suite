#! /usr/bin/python

import sys
import signal
import commands
import time
import traceback

from Exceptions import *

import Test_utils


def test1(utils, title):

    utils.show_progress(title)
    try:

        utils.info(title)

        utils.set_long_jdl(utils.get_jdl_file())
        utils.set_destination_ce(utils.get_jdl_file(),"2119/jobmanager")
        utils.add_jdl_attribute("MyProxyServer", utils.get_MYPROXY_SERVER())

        utils.info("Submit a job with a short proxy")
        utils.set_proxy(utils.get_PROXY(),"00:14")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit --nomsg --config %s -a %s"%(utils.get_config_file(),utils.get_jdl_file()))

        utils.dbg ("Check if the job has been submitted with the right proxy")
        
        output=utils.run_command_continue_on_error ("glite-wms-job-info -p %s"%(JOBID))
        
        for line in output.splitlines():
            if line.split(":")[0].strip() == "Timeleft":
                token=line.split(":")[1].strip()
                if ( (token.split(" ")[1] == "hours") or
                   (int(token.split(" ")[0]) > 14 ) ):
                    utils.error("The proxy of the submitted job has not the expected duration")
                    raise GeneralError("Check proxy of the submitted job","Wrong duration")

        utils.dbg ("Wait until job finishes (more than 15 minutes)")

        # we now need a long proxy to check job status
        utils.set_proxy(utils.get_PROXY(),"12:00")

        utils.wait_until_job_finishes(JOBID)

        utils.job_status(JOBID)

        if utils.get_job_status().find('Aborted')!=-1:

            OUTPUT=commands.getstatusoutput("glite-wms-job-status %s"%(JOBID))
                
            if OUTPUT[1].find("the user proxy expired") != -1:
                utils.error("TEST FAILS. Proxy expired")
                raise GeneralError("Check failed reason","Proxy expired")

            else:
                utils.error("TEST FAILS. Unexpected failed reason")
                raise GeneralError("Check failed reason","Unexpected failed reason")

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

def test2(utils,title):

    utils.show_progress(title)
    try:

        utils.info(title)

        utils.set_long_jdl(utils.get_jdl_file())
        utils.set_destination_ce(utils.get_jdl_file(),"/cream-")
        utils.add_jdl_attribute("MyProxyServer", utils.get_MYPROXY_SERVER())

        utils.info("Submit a job with a short proxy")
        utils.set_proxy(utils.get_PROXY(),"00:14")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit --nomsg --config %s -a %s"%(utils.get_config_file(),utils.get_jdl_file()))

        utils.dbg ("Check if the job has been submitted with the right proxy")
        
        output=utils.run_command_continue_on_error ("glite-wms-job-info -p %s"%(JOBID))
        
        for line in output.splitlines():
            if line.split(":")[0].strip() == "Timeleft":
                token=line.split(":")[1].strip()
                if ( (token.split(" ")[1] == "hours") or
                   (int(token.split(" ")[0]) > 14 ) ):
                    utils.error("The proxy of the submitted job has not the expected duration")
                    raise GeneralError("Check proxy of the submitted job","Wrong duration")

        utils.dbg ("Wait until job finishes (more than 15 minutes)")

        # we now need a long proxy to check job status
        utils.set_proxy(utils.get_PROXY(),"12:00")

        utils.wait_until_job_finishes(JOBID)

        utils.job_status(JOBID)

        if utils.get_job_status().find('Aborted')!=-1:

            OUTPUT=commands.getstatusoutput("glite-wms-job-status %s"%(JOBID))
                
            if OUTPUT[1].find("the user proxy expired") != -1:
                utils.error("TEST FAILS. Proxy expired")
                raise GeneralError("Check failed reason","Proxy expired")

            else:
                utils.error("TEST FAILS. Unexpected failed reason")
                raise GeneralError("Check failed reason","Unexpected failed reason")

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

def test3(utils, title):

    utils.show_progress(title)

    try:

        utils.info(title)

        utils.set_long_jdl(utils.get_jdl_file())
        utils.set_destination_ce(utils.get_jdl_file(),"2119/jobmanager")
        utils.add_jdl_attribute("MyProxyServer", "")

        utils.info("Submit a job with a short proxy")
        utils.set_proxy(utils.get_PROXY(),"00:14")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit --nomsg --config %s -a %s"%(utils.get_config_file(),utils.get_jdl_file()))

        utils.dbg ("Check if the job has been submitted with the right proxy")
        
        output=utils.run_command_continue_on_error ("glite-wms-job-info -p %s"%(JOBID))
        
        for line in output.splitlines():
            if line.split(":")[0].strip() == "Timeleft":
                token=line.split(":")[1].strip()
                if ( (token.split(" ")[1] == "hours") or
                   (int(token.split(" ")[0]) > 14 ) ):
                    utils.error("The proxy of the submitted job has not the expected duration")
                    raise GeneralError("Check proxy of the submitted job","Wrong duration")
        
        utils.dbg ("Wait until job finishes (more than 15 minutes)")

        # we now need a long proxy to check job status
        utils.set_proxy(utils.get_PROXY(),"12:00")

        utils.wait_until_job_finishes(JOBID)

        utils.job_status(JOBID)

        if utils.get_job_status().find('Aborted')!=-1 or utils.get_job_status().find('Done (Failed)')!=-1:

            OUTPUT=commands.getstatusoutput("glite-wms-job-status -v 2 %s | grep 'Failure reasons'"%(JOBID))
                
            if OUTPUT[1].find('expired')!=-1:
                utils.info("TEST PASS")

            else:
                utils.warn("Unexpected failed reason: %s"%(OUTPUT[1]))

        else:
            utils.error("TEST FAILS. Job not failed")
            raise GeneralError("Job finished with a unexpected status: %s."%(utils.get_job_status()),"Wrong job's final status")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0


def test4(utils, title):

    utils.show_progress(title)
    try:

        utils.info(title)

        utils.set_long_jdl(utils.get_jdl_file())
        utils.set_destination_ce(utils.get_jdl_file(),"/cream-")
        utils.add_jdl_attribute("MyProxyServer", "")

        utils.info("Submit a job with a short proxy")
        utils.set_proxy(utils.get_PROXY(),"00:14")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit --nomsg --config %s -a %s"%(utils.get_config_file(),utils.get_jdl_file()))

        utils.dbg ("Wait until job finishes (more than 15 minutes)")

        # we now need a long proxy to check job status
        utils.set_proxy(utils.get_PROXY(),"12:00")

        utils.wait_until_job_finishes(JOBID)

        utils.job_status(JOBID)

        if utils.get_job_status().find('Aborted')!=-1 or utils.get_job_status().find('Done (Failed)')!=-1:

            OUTPUT=commands.getstatusoutput("glite-wms-job-status -v 2 %s | grep 'Failure reasons'"%(JOBID))
                
            if OUTPUT[1].find('expired')!=-1:
                utils.info("TEST PASS")

            else:
                utils.warn("Unexpected failed reason: %s"%(OUTPUT[1]))

        else:
            utils.error("TEST FAILS. Job not failed")
            raise GeneralError("Job finished with a unexpected status: %s."%(utils.get_job_status()),"Wrong job's final status")
            
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

    tests=["Test 1: Test proxy renewal with LCG CE"]
    tests.append("Test 2: Test proxy renewal with CREAM CE")
    tests.append("Test 3: Test proxy renewal with LCG CE (without setting MYPROXYSERVER)")
    tests.append("Test 4: Test proxy renewal with CREAM CE (without setting MYPROXYSERVER)")

    utils = Test_utils.Test_utils(sys.argv[0],"WMS test proxy renewal operation")

    utils.prepare(sys.argv[1:],tests)

    utils.info("WMS test proxy renewal operation")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    if utils.get_NOPROXY()==0 and utils.get_MYPROXY_SERVER():
    
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

    else:
        if utils.get_NOPROXY()!=0:
            utils.warn("Tests require the user proxy password, please use -i option")
            utils.show_progress("Tests require the user proxy password, please use -i option")
        else:
            utils.warn("Tests require variable MYPROXYSERVER, please set it in the configuration file")
            utils.show_progress("Tests require variable MYPROXYSERVER, please set it in the configuration file")


    if len(fails) > 0 :
      utils.exit_failure("%s test(s) fail(s): %s"%(len(fails), fails))
    else:
      utils.exit_success()

if __name__ == "__main__":
    main()
