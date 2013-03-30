#! /usr/bin/python

import sys
import signal
import time
import os
import commands
import logging
import traceback

from Exceptions import *

import Test_utils


def checkstatus(utils,jobid):

    time.sleep (5)

    utils.info ("Check if the status is correct")

    logging.info("Check if status is correct for the job: %s",jobid)

    logging.info("Execute command: grep \"Warning - JobPurging not allowed\" %s",utils.get_tmp_file())

    result=commands.getstatusoutput("grep \"Warning - JobPurging not allowed\" %s"%(utils.get_tmp_file()))

    if result[0]!=0 :
       utils.job_status(jobid)

       if utils.get_job_status().find("Cleared") != -1 :
            logging.warning("Job %s not cleared!",jobid)
            utils.info ("WARNING Job %s not cleared!"%(jobid))
            return 1
        
    else:
       logging.warning("WMS is not recognized by the LB, JobPurging not allowed!")
       utils.info ("Warning: WMS is not recognized by the LB, JobPurging not allowed!")
    
    return 0


def checkoutput(utils):

    utils.info ("Check if the output files are correctly retrieved")

    logging.info("Check if the output files are correctly retrieved")

    dir=utils.run_command_continue_on_error ("grep -A 1 'have been successfully retrieved' %s | grep -v 'have been successfully retrieved'"%(utils.get_tmp_file()))

    logging.info("Look if in %s there are the output files std.out and std.err",dir)

    utils.info ("Look if in %s there are the output files std.out and std.err"%(dir))

    utils.run_command_continue_on_error ("ls %s/std.out"%(dir))
    utils.run_command_continue_on_error ("ls %s/std.err"%(dir))
    utils.remove ("%s/std.err"%(dir))
    utils.remove ("%s/std.out"%(dir))
    os.rmdir("%s"%(dir))

def check(utils,jobid):

    result=checkstatus (utils,jobid)

    if result == 0:
        checkoutput(utils)
    

def main():

    fails=0

    utils = Test_utils.Test_utils(sys.argv[0],"test glite-wms-job-output commmad")

    utils.prepare(sys.argv[1:])

    logging.info("Test glite-wms-job-output command")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    COMMAND="glite-wms-job-output"

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

    # submit some jobs

    logging.info("Submit a job")
    JOBID1=utils.run_command ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID1)

    logging.info("Submit a job")
    JOBID2=utils.run_command ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID2)

    logging.info("Submit a job")
    JOBID3=utils.run_command ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID3)

    logging.info("Submit a job")
    JOBID4=utils.run_command ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID4)

    logging.info("Submit a job")
    JOBID5=utils.run_command ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID5)

    logging.info("Submit a job")
    JOBID6=utils.run_command ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID6)

    logging.info("Submit a job")
    JOBID7=utils.run_command ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID7)

    logging.info("Submit a job")
    JOBID8=utils.run_command ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID8)

    logging.info("Submit a job")
    JOBID9=utils.run_command ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID9)

    #Test --config option
    utils.show_progress("Test 3")

    try:

        utils.wait_until_job_finishes (JOBID1)

        utils.remove("%s/tmp.output"%(utils.get_tmp_dir()))
        logging.info("Test 3: Check --config option")
        utils.info ("")
        utils.info ("Test --config option")
        utils.run_command_continue_on_error ("%s --config %s %s >> %s/tmp.output"%(COMMAND,utils.get_config_file(),JOBID1,utils.get_tmp_dir()))
        check (utils,JOBID1)
        utils.info ("Check the command output")
        utils.run_command_continue_on_error ("cat %s/tmp.output"%(utils.get_tmp_dir()))
        utils.info ("")
        utils.info ("Try to purge a Cleared job")
        logging.info("Try to purge a Cleared job")
        utils.run_command_continue_on_error ("%s --noint %s"%(COMMAND,JOBID1),1)
        utils.remove("%s/tmp.output"%(utils.get_tmp_dir()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())



    #Test --logfile option
    utils.show_progress("Test 5")
    
    try:

        utils.wait_until_job_finishes (JOBID2)

        logging.info("Test 5: Check --logfile option")
        utils.info ("")
        utils.info ("Test --logfile option")
        utils.run_command_continue_on_error ("%s --logfile %s %s"%(COMMAND,utils.get_log_file(),JOBID2))
        check (utils,JOBID2)
        utils.info ("Check the logfile")
        logging.info("Check the logfile")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
        utils.info ("")
        utils.info ("Try to purge a Cleared job")
        logging.info("Try to purge a Cleared job")
        utils.run_command_continue_on_error ("%s --noint %s"%(COMMAND,JOBID2),1)

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
    

    #Test --debug and --logfile options
    utils.show_progress("Test 6")

    try:

        utils.wait_until_job_finishes (JOBID3)

        logging.info("Test 6: Check --debug and --logfile options")
        utils.info ("")
        utils.info ("Test --debug and --logfile options")
        utils.run_command_continue_on_error ("%s --debug --logfile %s %s"%(COMMAND,utils.get_log_file(),JOBID3))
        check (utils,JOBID3)
        utils.info ("Check the logfile with debug option enabled")
        logging.info("Check the logfile with debug option enabled")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
        utils.info ("")
        utils.info ("Try to purge a Cleared job")
        logging.info("Try to purge a Cleared job")
        utils.run_command_continue_on_error ("%s --noint %s"%(COMMAND,JOBID3),1)

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    # Test --dir option
    utils.show_progress("Test 7")

    try:

        utils.wait_until_job_finishes (JOBID4)

        logging.info("Test 7: Check --dir option")
        utils.info ("")
        utils.info ("Test --dir option")
        utils.run_command_continue_on_error ("%s --noint --dir %s %s "%(COMMAND,utils.get_job_output_dir(),JOBID4))
        check(utils,JOBID4)

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

   
    # Test --nosubdir option
    utils.show_progress("Test 8")

    try:

        utils.wait_until_job_finishes (JOBID5)

        logging.info("Test 8: Check --nosubdir option")
        utils.info ("")
        utils.info ("Test --nosubdir option")
        utils.run_command_continue_on_error ("%s --noint --nosubdir --dir %s %s "%(COMMAND,utils.get_job_output_dir(),JOBID5))
        check(utils,JOBID5)

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

   
    # Test --list-only option
    utils.show_progress("Test 9")

    try:

        utils.remove(utils.get_tmp_file())
        utils.wait_until_job_finishes (JOBID6)

        logging.info("Test 9: Check --list-only option")
        utils.info ("")
        utils.info ("Test --list-only option")
        utils.run_command_continue_on_error ("%s --list-only %s >> %s"%(COMMAND,JOBID6,utils.get_tmp_file()))
        utils.run_command_continue_on_error ("grep std.out %s"%(utils.get_tmp_file()))
        utils.run_command_continue_on_error ("grep std.err %s"%(utils.get_tmp_file()))
        utils.remove(utils.get_tmp_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    # Test --nopurge option
    utils.show_progress("Test 10")

    try:

        logging.info("Test 10: Check --nopurge option")
        utils.info ("")
        utils.info ("Test --nopurge option")
        utils.run_command_continue_on_error ("%s --nopurge %s"%(COMMAND,JOBID6))
        utils.job_status(JOBID6)

        if utils.get_job_status().find("Cleared")==-1 :
            utils.info ("Try again to retrieve the output")
            logging.info("Try again to retrieve the output")
            utils.run_command_continue_on_error ("%s --noint --nopurge %s"%(COMMAND,JOBID6))
        else:
            logging.error("Job %s has been purged",JOBID6)
            raise GeneralError ("","Job %s has been purged"%(JOBID6))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    # Test --input option
    utils.show_progress("Test 11")

    try:

        utils.wait_until_job_finishes (JOBID7)
        utils.wait_until_job_finishes (JOBID8)

        logging.info("Test 11: Check --input option")
        utils.info ("")
        utils.info ("Test --input option")

        logging.info("Write job ids to file %s",utils.get_jobid_file())

        os.system("echo %s >> %s"%(JOBID6,utils.get_jobid_file()))
        os.system("echo %s >> %s"%(JOBID7,utils.get_jobid_file()))
        os.system("echo %s >> %s"%(JOBID8,utils.get_jobid_file()))

        utils.run_command_continue_on_error ("%s --noint --input %s"%(COMMAND,utils.get_jobid_file()))

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
