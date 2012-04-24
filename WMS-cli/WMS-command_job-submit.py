#! /usr/bin/python

import sys
import signal
import commands
import os
import time
import string
import logging
import traceback

from Exceptions import *

import Test_utils


def main():

    fails=0

    utils = Test_utils.Test_utils(sys.argv[0],"test glite-wms-job-submit commmad")

    utils.prepare(sys.argv[1:])

    logging.info("Test glite-wms-job-submit command")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    COMMAND="glite-wms-job-submit"

    utils.show_progress("Test 1")
    logging.info("Test 1: Check if command %s exists",COMMAND)
    utils.info ("Check if command %s exists"%(COMMAND))
    utils.run_command ("which %s"%(COMMAND))


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


    # Test --autm-delegaiton (-a) option
    utils.show_progress("Test 3")

    try:

        logging.info("Test 3: Check --autm-delegation option")
        utils.remove(utils.get_tmp_file())
        utils.info ("")
        utils.info ("Test --autm-delegation option")
        utils.run_command_continue_on_error ("%s --autm-delegation %s >> %s"%(COMMAND,utils.get_jdl_file(),utils.get_tmp_file()))
        utils.info ("Check the command's output")
        logging.info ("Check the command's output")
        utils.run_command_continue_on_error("cat %s"%(utils.get_tmp_file()))

        JOBID=utils.run_command_continue_on_error("grep ':9000' %s"%(utils.get_tmp_file()))
        logging.info ("Cancel submitted job with id: %s",JOBID)
        utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))
        utils.remove(utils.get_tmp_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    # Test --delegationid option
    utils.show_progress("Test 4")

    try:

        logging.info("Test 4: Check --delegationid option")

        Delegation="DelegationTest"
        logging.info("Set delegationid to %s",Delegation)
        utils.run_command_continue_on_error("glite-wms-job-delegate-proxy -d %s"%(Delegation))
    
        utils.remove(utils.get_tmp_file())
        utils.info ("")
        utils.info ("Test --delegationid option")
        utils.run_command_continue_on_error ("%s --delegationid %s %s >> %s"%(COMMAND,Delegation,utils.get_jdl_file(),utils.get_tmp_file()))
        utils.info ("Check the command's output")
        logging.info("Check the command's output")
        utils.run_command_continue_on_error("cat %s"%(utils.get_tmp_file()))
    
        JOBID=utils.run_command_continue_on_error("grep ':9000' %s"%(utils.get_tmp_file()))
        logging.info ("Cancel submitted job with id: %s",JOBID)
        utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))
        utils.remove(utils.get_tmp_file())
    
    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    # Test --config option
    utils.show_progress("Test 5")

    try:

        logging.info("Test 5: Check --config option")
        utils.remove(utils.get_tmp_file())
        utils.info ("")
        utils.info ("Test --config option")
        utils.run_command_continue_on_error ("%s %s --config %s %s >> %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file(),utils.get_tmp_file()))
        utils.info ("Check the output command")
        logging.info("Check the command's output")
        utils.run_command_continue_on_error("cat %s"%(utils.get_tmp_file()))

        JOBID=utils.run_command_continue_on_error("grep ':9000' %s"%(utils.get_tmp_file()))
        logging.info ("Cancel submitted job with id: %s",JOBID)
        utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))
        utils.remove(utils.get_tmp_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    # Test option --endpoint
    utils.show_progress("Test 6")

    try:

        logging.info("Test 6: Check --endpoint option")
        utils.remove(utils.get_tmp_file())
        utils.info ("")
        utils.info ("Test --endpoint option")
        utils.run_command_continue_on_error ("%s %s --endpoint https://%s:7443/glite_wms_wmproxy_server %s >> %s"%(COMMAND,utils.get_delegation_options(),utils.get_WMS(),utils.get_jdl_file(),utils.get_tmp_file()))
        utils.info ("Check the connected endpoint")
        logging.info("Check the connected endpoint")
        endpoint=utils.run_command_continue_on_error("grep \"Connecting to the service\"  %s"%(utils.get_tmp_file()))
        utils.info("Connected Endpoint: %s"%(endpoint))
        logging.info("Connected Endpoint: %s",endpoint)
        utils.info ("Check the output command")
        logging.info("Check the command's output")
        utils.run_command_continue_on_error("cat %s"%(utils.get_tmp_file()))
    
        JOBID=utils.run_command_continue_on_error("grep ':9000' %s"%(utils.get_tmp_file()))
        logging.info ("Cancel submitted job with id: %s",JOBID)
        utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))
        utils.remove(utils.get_tmp_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
        

    # Test option --output
    utils.show_progress("Test 7")

    try:

        logging.info("Test 7: Check --output option")
        utils.info ("")
        utils.info ("Test --output option")
        utils.run_command_continue_on_error ("%s %s --output %s %s "%(COMMAND,utils.get_delegation_options(),utils.get_output_file(),utils.get_jdl_file()))
        utils.info ("Check the output file")
        logging.info("Check the output file")
        utils.run_command_continue_on_error("cat %s"%(utils.get_output_file()))

        JOBID=utils.run_command_continue_on_error("grep ':9000' %s"%(utils.get_output_file()))
        logging.info ("Cancel submitted job with id: %s",JOBID)
        utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))
        utils.remove(utils.get_output_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
    
    # Test option --logfile
    utils.show_progress("Test 8")

    try:

        logging.info("Test 8: Check --logfile option")
        utils.info ("")
        utils.info ("Test --logfile option")
        JOBID=utils.run_command_continue_on_error ("%s %s --nomsg --logfile %s %s "%(COMMAND,utils.get_delegation_options(),utils.get_log_file(),utils.get_jdl_file()))
        utils.info ("Check the log file")
        logging.info("Check the log file")
        utils.run_command_continue_on_error("cat %s"%(utils.get_log_file()))

        logging.info ("Cancel submitted job with id: %s",JOBID)
        utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    
    # Test option --nomsg
    utils.show_progress("Test 9")

    try:

        logging.info("Test 9: Check --nomsg option")
        utils.info ("")
        utils.info ("Test --nomsg option")
        JOBID=utils.run_command_continue_on_error ("%s %s --nomsg --config %s %s "%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
        utils.dbg ("Job Id is %s"%(JOBID))
        utils.info ("Check the job status")
        logging.info("Check the job status")
        utils.run_command_continue_on_error ("glite-wms-job-status %s"%(JOBID))
        logging.info ("Cancel submitted job with id: %s",JOBID)
        utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    # Test all options together
    utils.show_progress("Test 10")

    try:

        logging.info("Test 10: Check all options together")
        utils.info ("")
        utils.info ("Test all options together")
        utils.run_command_continue_on_error ("%s %s --noint --logfile %s --output %s --endpoint https://%s:7443/glite_wms_wmproxy_server %s"%(COMMAND,utils.get_delegation_options(),utils.get_log_file(),utils.get_output_file(),utils.get_WMS(),utils.get_jdl_file()))
        utils.info ("Check the output file")
        logging.info("Check the output file")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_output_file()))
        utils.info ("Check the log file")
        logging.info("Check the log file")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))

        JOBID=utils.run_command_continue_on_error("grep ':9000' %s"%(utils.get_output_file()))
        logging.info ("Cancel submitted job with id: %s",JOBID)
        utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
    
    utils.remove ("%s"%(utils.get_log_file()))
    utils.remove ("%s"%(utils.get_output_file()))


    # Test --input option
    utils.show_progress("Test 11")

    try:

        logging.info("Test 11: Check --input option")
        utils.info ("")
        utils.info ("Test --input option")
        utils.info ("Build CE file")
        logging.info("Build CE file")
        utils.run_command_continue_on_error ("glite-wms-job-list-match %s --config %s --rank --output %s  %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_output_file(),utils.get_jdl_file()))

        logging.info("Execute the command: grep \"No Computing Element\" %s",utils.get_output_file())

        result=commands.getstatusoutput("grep \"No Computing Element\" %s"%(utils.get_output_file()))

        if result != 0 :

            utils.remove(utils.get_tmp_file())

            utils.run_command_continue_on_error("awk -F ' ' '/:[[:digit:]]*\// {print $2}' %s > %s"%(utils.get_output_file(),utils.get_tmp_file()))

            JOBID=utils.run_command_continue_on_error ("%s %s --config %s --noint --input %s --nomsg %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_tmp_file(),utils.get_jdl_file()))
       
            CENAME=utils.get_CE (JOBID)
         
            utils.info ("Check if it has used the right CE")

            logging.info("Check if it has used the right CE")

            CE=utils.run_command_continue_on_error("head -1 %s"%(utils.get_tmp_file()))
         
            if CE != CENAME :
                logging.error("Job has been submitted to wrong CE: %s instead of %s",CENAME,CE)
                raise GeneralError("Check destination","Job has been submitted to wrong CE: %s (instead of %s)"%(CENAME,CE))
            else:
                logging.info("Check success")
                utils.info ("Check success")

            utils.remove(utils.get_tmp_file())

            logging.info ("Cancel submitted job with id: %s",JOBID)
            utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))
          
        else:
            logging.warning("No matching found. TEST SKIPPED")
            utils.info ("No matching found. Test skipped.")

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
    
    utils.remove (utils.get_tmp_file())
    utils.remove (utils.get_output_file())

 
    # Test --resource option
    utils.show_progress("Test 12")

    try:

        logging.info("Test 12: Check --resource option")
        utils.info ("")
        utils.info ("Test --resource option")
        utils.info ("Look for a usable CE")
        logging.info("Look for a usable CE")
        utils.run_command_continue_on_error ("glite-wms-job-list-match --noint --config %s %s --rank --output %s %s"%(utils.get_config_file(),utils.get_delegation_options(),utils.get_output_file(),utils.get_jdl_file()))

        logging.info("Execute command: grep \"No Computing Element\" %s",utils.get_output_file())

        result=commands.getstatusoutput("grep \"No Computing Element\" %s"%(utils.get_output_file()))

        if result != 0 :

            CE_ID=utils.run_command_continue_on_error("awk -F ' ' '/:[[:digit:]]*\// {print $2}' %s | head -1"%(utils.get_output_file()))

            JOBID=utils.run_command_continue_on_error ("%s %s --config %s --noint --resource %s --nomsg %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),CE_ID,utils.get_jdl_file()))
              
            CENAME=utils.get_CE(JOBID)

            utils.info ("Check if it has used the right CE")

            if CE_ID != CENAME :
                logging.error("Job has been submitted to the wrong CE: %s (instead of %s)",CENAME,CE_ID)
                raise GeneralError ("Check destination ","Job has been submitted to the wrong CE: %s (instead of %s)"%(CENAME,CE_ID))
            else:
                logging.info("Check success")
                utils.info ("Check success")

            logging.info ("Cancel submitted job with id: %s",JOBID)
            utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))
       
        else:
            logging.warning("No matching found, TEST SKIPPED")
            utils.info ("No matching found. Test skipped.")
    

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    utils.remove (utils.get_output_file())


    # Test option --register-only
    utils.show_progress("Test 13")

    try:

        utils.remove (utils.get_tmp_file())
        logging.info("Test 13: Check --register-only option")
        utils.info ("")
        utils.info ("Test --register-only option")

        utils.run_command_continue_on_error ("%s %s --config %s --register-only --output %s %s >> %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jobid_file(),utils.get_jdl_file(),utils.get_tmp_file()))

        JOBID=utils.run_command_continue_on_error ("tail -1 %s"%(utils.get_jobid_file()))

        utils.info ("Check if the output of the command is as expected")
        logging.info ("Check if the output of the command is as expected")

        utils.run_command_continue_on_error ("grep \"\--start %s\" %s"%(JOBID,utils.get_tmp_file()))

        utils.remove (utils.get_tmp_file())

        utils.info("wait 10 secs ...")
        time.sleep(10)

        utils.job_status(JOBID)

        if utils.get_job_status().find("Submitted")==-1:
            logging.warning("The job %s is not in the correct status. It's status is %s",JOBID,utils.get_job_status())
            utils.info ("WARNING: The job %s is not in the correct status. It's status is %s ."%(JOBID,utils.get_job_status()))
        else:
            logging.info("Check success")
            utils.info ("Check success")

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
  
    # Test option --start
    utils.show_progress("Test 14")

    try:

        logging.info("Test 14: Check --start option")
        utils.info ("")
        utils.info ("Test --start option")

        utils.run_command_continue_on_error ("%s --start %s"%(COMMAND,JOBID))

        utils.wait_until_job_finishes(JOBID)

        utils.job_status(JOBID)

        if utils.get_job_status().find("Done") == -1 :
            logging.warning("The job %s fails. Its final status is %s",JOBID,utils.get_job_status())
            utils.info ("WARNING: The job %s fails. Its final status is %s."%(JOBID,utils.get_job_status()))
        else:
            logging.info("Check success")
            utils.info ("Check success")

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    
    # Test option --transfer-files
    utils.show_progress("Test 15")

    try:

        logging.info("Test 15: Check --transfer-files and --proto options")
        utils.info ("")
        utils.info ("Test --transfer-files and --proto options")

        utils.set_isb_jdl(utils.get_jdl_file())
    
        JOBID=utils.run_command_continue_on_error ("%s %s --config %s --register-only --transfer-files --proto gsiftp --nomsg %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
    
        utils.job_status(JOBID)

        if utils.get_job_status().find("Submitted") ==-1 :
            logging.warning("The job %s is not in the correct status. Its status is %s",JOBID,utils.get_job_status())
            utils.info ("WARNING: The job %s is not in the correct status. Its status is %s."%(JOBID,utils.get_job_status()))
        else:
            logging.info("Check success")
            utils.info ("Check success")

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
  
    
    # Test option --start
    utils.show_progress("Test 16")

    try:

        logging.info("Test 16: Check --start option (after using submit command with options --register-only and transfer-files)")
        utils.info ("")
        utils.info ("Test --start option (after using submit command with options --register-only and transfer-files)")
        utils.run_command_continue_on_error ("%s --start %s"%(COMMAND,JOBID))

        # ... wait loop with job-status calls
        utils.wait_until_job_finishes (JOBID)

        utils.info ("Retrieve the output")
        logging.info("Retrieve the output")
        utils.run_command_continue_on_error ("glite-wms-job-output --noint --nosubdir --dir %s %s"%(utils.get_job_output_dir(),JOBID))

        utils.info ("Check the output file")
        logging.info("Check the output file")

        if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) and os.path.isfile("%s/std.err"%(utils.get_job_output_dir())):
            utils.run_command_continue_on_error ("grep \"example.jdl\" %s/std.out"%(utils.get_job_output_dir()))
        else:
            logging.error("Job output is not correct")
            raise GeneralError("Check output","Job output is not correct")

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    #Test --valid option
    utils.show_progress("Test 17")

    try:

        logging.info("Test 17: Check --valid option")
        utils.info ("")
        utils.info ("Test --valid option")

        # we ask 60 seconds of validity
        NOW=time.strftime('%s')
        MYEXPIRY=time.strftime('%s', time.localtime(time.time() + 60))

        utils.remove(utils.get_tmp_file())

        # we need a jdl which doesn't match
        utils.set_requirements("\"false\"")
        # ... submit a jdl valid for max 1 minute from NOW
        JOBID=utils.run_command_continue_on_error("%s %s --config %s --nomsg --valid 00:01 %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        #wait for job submission
        utils.info("Wait 30 secs ...")
        time.sleep(30)

        # Check the status
        utils.remove(utils.get_tmp_file())

        utils.run_command_continue_on_error ("glite-wms-job-status %s >> %s"%(JOBID,utils.get_tmp_file()))

        STATUS=utils.run_command_continue_on_error ("grep -m 1 \'Current Status\' %s | awk -F: \'{print $2}\'"%(utils.get_tmp_file()))

        STATUS = string.strip(STATUS)

        if STATUS.find("Waiting") != -1 :
            utils.run_command_continue_on_error ("grep \"BrokerHelper: no compatible resources\" %s"%(utils.get_tmp_file()))
            logging.info("Job doesn;t match as expected")
            utils.info ("Job doesn't match as expected")
        else:
            logging.error("Job is in a wrong state: %s",STATUS)
            raise GeneralError ("Check job state","Job is in a wrong state: %s"%(STATUS))

   
        # Check the jdl
        utils.info ("Check the job's jdl")
        logging.info("Check the job's jdl")
        utils.remove(utils.get_tmp_file())

        utils.run_command_continue_on_error ("glite-wms-job-info --noint -j --output %s %s"%(utils.get_tmp_file(),JOBID))

        JDLEXPIRY = utils.run_command_continue_on_error ("grep ExpiryTime %s | awk -F= '{print $2}' | sed -e \"s/;//\""%(utils.get_tmp_file()))

        ## MYEXPIRY and JDLEXPIRY should be equal
        if int(MYEXPIRY) < int(JDLEXPIRY) :
            logging.error("Expiry time has not be set correctly! (%s != %s)",MYEXPIRY,JDLEXPIRY)
            raise GeneralError ("Check expriry time","Expiry time has not be set correctly! (%s != %s)"%(MYEXPIRY,JDLEXPIRY))
        else:
            logging.info("Attribute ExpiryTime has been correctly set in jdl")
            utils.info ("Attribute ExpiryTime has been correctly set in jdl")
    
        # wait until expiration
        utils.info("Wait 30 secs ...")
        time.sleep (30)

        utils.info ("Wait until job aborts... this will take some minutes..")

        utils.wait_until_job_finishes (JOBID)

        utils.remove(utils.get_tmp_file())

        utils.run_command_continue_on_error ("glite-wms-job-status %s >> %s"%(JOBID,utils.get_tmp_file()))

        STATUS=utils.run_command_continue_on_error ("grep -m 1 \'Current Status\' %s | awk -F: \'{print $2}\'"%(utils.get_tmp_file()))

        STATUS = string.strip(STATUS)

        if STATUS.find("Aborted") != -1 :
            utils.run_command_continue_on_error ("grep \"request expired\" %s"%(utils.get_tmp_file()))
            logging.info("Job correctly aborts")
            utils.info ("Job correctly aborts")
        else:
            logging.error("Job is in a wrong state: %s",STATUS)
            raise GeneralError("Check job state","Job is in a wrong state: %s"%(STATUS))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    utils.remove(utils.get_tmp_file())

    
    # Test option --to
    utils.show_progress("Test 18")

    try:

        logging.info("Test 18: Check --to option")
        utils.info ("")
        utils.info ("Test --to option")

        # ... make a timestamp which is 1 minute (max) from now
        currenttime=time.time()
        NOW = time.strftime('%H:%M',time.localtime(currenttime+60))
        NOW_EPOCH=time.strftime("%Y-%m-%d %H:%M:00",time.localtime(currenttime+60))

        # we need a jdl which doesn't match
        utils.set_requirements ("\"false\"")

        #.. submit a jdl valid for max 1 minute from NOW
        JOBID=utils.run_command_continue_on_error ("%s %s --nomsg --config %s --to %s %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),NOW,utils.get_jdl_file()))
  
        # wait for job submission
        utils.info("Wait 30 secs ...")
        time.sleep (30)

        # Check the status
        utils.remove(utils.get_tmp_file())

        utils.run_command_continue_on_error ("glite-wms-job-status %s >> %s"%(JOBID,utils.get_tmp_file()))

        STATUS=utils.run_command_continue_on_error("grep -m 1 \'Current Status\' %s | awk -F: \'{print $2}\'"%(utils.get_tmp_file()))

        STATUS = string.strip(STATUS)

        if STATUS.find("Waiting") != -1 :
            utils.run_command_continue_on_error ("grep \"BrokerHelper: no compatible resources\" %s"%(utils.get_tmp_file()))
        else:
            logging.error("Job is in a wrong state: %s",STATUS)
            raise GeneralError("","Job is in a wrong state: %s"%(STATUS))
    

        utils.info ("Check the job's jdl")
        logging.info ("Check the job's jdl")
    
        utils.run_command_continue_on_error ("glite-wms-job-info --noint -j --output %s %s"%(utils.get_tmp_file(),JOBID))

        JDLEXPIRY=utils.run_command_continue_on_error ("grep ExpiryTime %s | awk -F= '{print $2}' | sed -e \"s/;//\" "%(utils.get_tmp_file()))
        JDLEXPIRY=string.strip(JDLEXPIRY)

        MYEXPIRY=int(time.mktime(time.strptime(NOW_EPOCH, '%Y-%m-%d %H:%M:%S')))

        if MYEXPIRY != int(JDLEXPIRY) :
            logging.error("Expiry time has not been set correctly! (%s != %s)",MYEXPIRY,JDLEXPIRY)
            raise GeneralError ("Check expiry time","Expiry time has not been set correctly! ( %s != %s )"%(MYEXPIRY,JDLEXPIRY))
        else:
            logging.info ("Attribute ExpiryTime has been correctly set in jdl")
            utils.info  ("Attribute ExpiryTime has been correctly set in jdl")

        # wait until expiration
        utils.info("Wait 30 secs...")
        time.sleep (30)

        utils.info ("Wait until job aborts... this will take some minutes..")

        utils.wait_until_job_finishes (JOBID)

        utils.remove(utils.get_tmp_file())

        utils.run_command_continue_on_error ("glite-wms-job-status %s >> %s"%(JOBID,utils.get_tmp_file()))

        STATUS=utils.run_command_continue_on_error ("grep -m 1 \'Current Status\' %s | awk -F: \'{print $2}\'"%(utils.get_tmp_file()))

        STATUS = string.strip(STATUS)
 
        if STATUS.find("Aborted") != -1 :
            utils.run_command_continue_on_error ("grep \"request expired\" %s"%(utils.get_tmp_file()))
            utils.info ("Job correctly aborts")
            logging.info("Job correctly aborts")
        else:
            logging.error("Job is in a wrong state %s",STATUS)
            raise GeneralError("Check job state","Job is in a wrong state: %s"%(STATUS))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
    
    
    # Test option --default-jdl
    utils.show_progress("Test 19")

    try:

        logging.info("Test 19: Check --default-jdl option")
        utils.info ("")
        utils.info ("Test --default-jdl option")

        utils.remove(utils.get_tmp_file())

        # ... make a test default JDL file
        os.system("echo \"Attribute = 'Test default jdl';\" >  %s"%(utils.get_tmp_file()))

        JOBID=utils.run_command_continue_on_error ("%s %s --config %s --nomsg --default-jdl %s %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_tmp_file(),utils.get_jdl_file()))

        utils.dbg ("Job ID is %s"%(JOBID))
        utils.info ("Check the jdl")
        utils.remove(utils.get_tmp_file())
        utils.run_command_continue_on_error ("glite-wms-job-info -j %s >> %s"%(JOBID,utils.get_tmp_file()))
        utils.run_command_continue_on_error ("grep \"Attribute = 'Test default jdl';\" %s"%(utils.get_tmp_file()))
        utils.remove(utils.get_tmp_file())
        logging.info ("Cancel submitted job with id: %s",JOBID)
        utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    
    # Test option --json
    utils.show_progress("Test 20")

    try:

        logging.info("Test 20: Check --json option")
        utils.info ("")
        utils.info ("Test --json option")

        utils.remove(utils.get_tmp_file())

        utils.run_command_continue_on_error ("%s %s --config %s --json %s >> %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file(),utils.get_tmp_file()))
        utils.dbg ("Get job ID")

        message=utils.run_command_continue_on_error("awk '{print $4}' %s"%(utils.get_tmp_file()))
        message=message.split("\"")

        JOBID=message[1]

        utils.info("Check job status")
        #utils.remove(utils.get_tmp_file())
        utils.run_command_continue_on_error ("glite-wms-job-status %s >> %s"%(JOBID,utils.get_tmp_file()))
        utils.info ("Check command's output")
        logging.info("Check command's output")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_tmp_file()))
        utils.remove(utils.get_tmp_file())
        logging.info ("Cancel submitted job with id: %s",JOBID)
        utils.run_command_continue_on_error ("glite-wms-job-cancel --noint %s"%(JOBID))
        

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    # Test option --collection
    utils.show_progress("Test 21")

    try:

        logging.info("Test 21: Check --collection option")
        utils.info ("")
        utils.info ("Test --collection option")

        utils.remove(utils.get_tmp_file())

        # create 3 jdl files based on basic jdl file
        logging.info("Create collection's jdl files")
        os.mkdir("%s/collection_jdls"%(utils.get_tmp_dir()))
        os.system("cp %s %s/collection_jdls/1.jdl"%(utils.get_jdl_file(),utils.get_tmp_dir()))
        os.system("cp %s %s/collection_jdls/2.jdl"%(utils.get_jdl_file(),utils.get_tmp_dir()))
        os.system("cp %s %s/collection_jdls/3.jdl"%(utils.get_jdl_file(),utils.get_tmp_dir()))

        JOBID=utils.run_command_continue_on_error ("%s %s --config %s --nomsg --collection %s/collection_jdls"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_tmp_dir()))

        utils.dbg ("Job ID is %s"%(JOBID))
        utils.info ("Check the collection status")
        logging.info("Check the collection status")
        utils.run_command_continue_on_error ("glite-wms-job-status %s >> %s"%(JOBID,utils.get_tmp_file()))
        utils.info ("Check command's output")
        logging.info("Check command's output")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_tmp_file()))

        utils.remove(utils.get_tmp_file())
        os.system("rm -rf %s/collection_jdls/"%(utils.get_tmp_dir()))
        logging.info ("Cancel submitted job with id: %s",JOBID)
        utils.run_command_continue_on_error ("glite-wms-job-cancel --noint %s"%(JOBID))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
    
    

    """
    # Test option --dag
    utils.show_progress("Test 22")
    logging.info("Test 22: Check --dag option")
    utils.info ("")
    utils.info ("Test --dag option")

    utils.remove(utils.get_tmp_file())

    # create dag nodes jdl files
    JOBID=utils.run_command ("%s %s --config %s --nomsg --dag %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.debug ("Job ID is %s"%(JOBID))
    utils.info ("Check the dag status")
    utils.run_command ("glite-wms-job-status %s >> %s"%(JOBID,utils.get_tmp_file()))
    utils.info ("Check command output")
    utils.run_command("cat %s"%(utils.get_tmp_file()))
    utils.remove(utils.get_tmp_file())
    utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))

    """

    # Test option --nodes-resource
    utils.show_progress("Test 22")

    try:

        logging.info("Test 22: Check --nodes-resource option")
        utils.info ("")
        utils.info ("Test --nodes-resource option")

        utils.info ("Look for a usable CE")

        utils.set_jdl("%s/list.jdl"%(utils.get_tmp_dir()))

        FILE=open("%s/list.jdl"%(utils.get_tmp_dir()),"a")
        FILE.write("Requirements=RegExp(\"2119/jobmanager\",other.GlueCEUniqueID);\n")
        FILE.close()

        output=utils.run_command_continue_on_error ("glite-wms-job-list-match --noint --config %s %s %s/list.jdl"%(utils.get_config_file(),utils.get_delegation_options(),utils.get_tmp_dir()))

        if output.find("No Computing Element")!=-1:
            logging.warning("No matching CE found. TEST SKIPPED")
            utils.info ("No matching CE found. Test skipped.")
            utils.show_critical("No matching CE found. TEST SKIPPED")
        else:

            for line in output.split("\n"):
                if line.find(" - ")!=-1:
                    CE_ID=line.split(" - ")[1].strip()
                    break

            if utils.has_external_jdl() == 0 :
                utils.set_dag_jdl(utils.get_jdl_file())
      
            JOBID=utils.run_command_continue_on_error ("%s %s --config %s --nomsg --nodes-resource %s %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),CE_ID,utils.get_jdl_file()))

            CENAME=utils.get_dag_CE(JOBID)

            utils.info ("Check if it has used the right CE")

            logging.info("Check if it has used the right CE")

            if CE_ID != CENAME :
                logging.error("Job has been submitted to the wrong CE: %s (instead of %s)",CENAME,CE_ID)
                raise GeneralError("Check destination","Job has been submitted to the wrong CE: %s (instead of %s)"%(CENAME,CE_ID))
            else:
                logging.info("Check success (%s)",CE_ID)
                utils.info ("Check success (%s)"%(CE_ID))

            logging.info ("Cancel submitted job with id: %s",JOBID)

            utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))


    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    utils.remove (utils.get_output_file())
    
    
    if fails > 0 :
      utils.exit_failure("%s test(s) fail(s)"%(fails))
    else:
      utils.exit_success()



if __name__ == "__main__":
    main()
