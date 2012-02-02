#! /usr/bin/python

import sys
import signal
import commands
import os.path
import time
import string
import logging
import traceback

from Exceptions import *

import Test_utils


def main():


    fails=0

    utils = Test_utils.Test_utils(sys.argv[0],"test glite-wms-job-persual commmad")

    utils.prepare(sys.argv[1:])

    logging.info("Test glite-wms-job-perusal command")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    COMMAND="glite-wms-job-perusal"

    utils.show_progress("Test 1")
    logging.info ("Test 1: Check if command %s exists",COMMAND)
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

    if utils.has_external_jdl() == 0 :
      utils.set_perusal_jdl(utils.get_jdl_file())

    utils.create_sleeper()

    ## ... submit a job
    utils.info ("Submit the job")
    logging.info("Submit the job")
    JOBID=utils.run_command ("glite-wms-job-submit %s --nomsg %s"%(utils.get_delegation_options(),utils.get_jdl_file()))
    utils.dbg ("JobID is %s"%(JOBID))
    logging.info("JobID is %s",JOBID)

    ## ... enable file perusal for out.txt and std.out

    utils.show_progress("Test 3")

    try:

        logging.info("Test 3: Check --set option")
        utils.info ("")
        utils.info ("Test --set option")
        utils.run_command_continue_on_error ("%s --set --filename out.txt -f std.out %s"%(COMMAND,JOBID))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    #Test option --unset
    utils.show_progress("Test 4")

    try:

        logging.info("Test 4: Check --unset option")
        utils.info ("")
        utils.info ("Test --unset option")
        utils.run_command_continue_on_error ("%s --unset %s"%(COMMAND,JOBID))
        utils.info("Disable file perusal")

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    
    #Test options --set and --config
    utils.show_progress("Test 5")

    try:

        logging.info("Test 5: Check --set and --config options")
        utils.info ("")
        utils.info ("Test --set and --config options")
        utils.run_command_continue_on_error("%s --set -f std.out --config %s %s"%(COMMAND,utils.get_config_file(),JOBID))
        utils.info("Disable file perusal")
        logging.info("Disable file perusal")
        utils.run_command_continue_on_error ("%s --unset %s"%(COMMAND,JOBID))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    #Test options --set and --output
    utils.show_progress("Test 6")

    try:

        utils.remove(utils.get_output_file())
        logging.info("Test 6: Check --set and --output options")
        utils.info ("")
        utils.info ("Test --set and --output options")
        utils.run_command_continue_on_error("%s --set -f std.out --output %s %s"%(COMMAND,utils.get_output_file(),JOBID))
        utils.info("Check the output file")
        logging.info("Check the output file")
        utils.run_command_continue_on_error("cat %s"%(utils.get_output_file()))
        utils.info("Disable file perusal")
        logging.info("Disable file perusal")
        utils.run_command_continue_on_error ("%s --unset %s"%(COMMAND,JOBID))
        utils.remove(utils.get_output_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    #Test options --set and --logfile
    utils.show_progress("Test 7")

    try:

        utils.remove(utils.get_log_file())
        logging.info("Test 7: Check --set and --logfile options")
        utils.info ("")
        utils.info ("Test --set and --logfile options")
        utils.run_command_continue_on_error("%s --set -f std.out --logfile %s %s"%(COMMAND,utils.get_log_file(),JOBID))
        utils.info("Check the log file")
        logging.info("Check the log file")
        utils.run_command_continue_on_error("cat %s"%(utils.get_log_file()))
        utils.info("Disable file perusal")
        logging.info("Disable file perusal")
        utils.run_command_continue_on_error ("%s --unset %s"%(COMMAND,JOBID))
        utils.remove(utils.get_log_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    #Test options --set --logfile and --debug
    utils.show_progress("Test 8")

    try:

        utils.remove(utils.get_log_file())
        logging.info("Test 8: Check --set , --logfile and --debug options")
        utils.info ("")
        utils.info ("Test --set --logfile and --debug option")
        utils.run_command_continue_on_error("%s --set -f std.out --debug --logfile %s %s"%(COMMAND,utils.get_log_file(),JOBID))
        utils.info("Check the log file with debug option enabled")
        logging.info("Check the log file with debug option enabled")
        utils.run_command_continue_on_error("cat %s"%(utils.get_log_file()))
        utils.info("Disable file perusal")
        logging.info("Disable file perusal")
        utils.run_command_continue_on_error ("%s --unset %s"%(COMMAND,JOBID))
        utils.remove(utils.get_log_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    #Test options --set --nodisplay
    utils.show_progress("Test 9")

    try:

        logging.info("Test 9: Check --set and --nodisplay options")
        utils.info ("")
        utils.info ("Test --set and --nodisplay options")
        utils.run_command_continue_on_error ("%s --unset %s"%(COMMAND,JOBID))

        # ....
        utils.info ("")
        utils.info ("Test --set option")
        utils.run_command_continue_on_error ("%s --set --filename out.txt -f std.out %s"%(COMMAND,JOBID))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
    
    # Test option --get
    utils.show_progress("Test 10")

    try:

        logging.info("Test 10: Check --get option")
        utils.info ("")
        utils.show_critical("BEWARE default min perusal interval is 1000 secs, so this phase could take many minutes")
        utils.info ("Test --get option")

        while utils.job_is_finished(JOBID) == 0:
            utils.info("Wait 60 secs ...")
            logging.info("Wait 60 secs ...")
            time.sleep(60)
            utils.run_command_continue_on_error ("%s --get -f out.txt --dir %s %s"%(COMMAND,utils.get_job_output_dir(),JOBID))
    

        utils.info ("List the retrieved parts of out.txt")
        logging.info("List the retrieved parts of out.txt")
        utils.run_command_continue_on_error ("ls -l %s | grep out.txt"%(utils.get_job_output_dir()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    utils.show_progress("Test 11")

    try:

        logging.info("Test 11: Check --get and --dir options")
        utils.info ("")
        utils.info ("Test --get option with --dir")
        utils.run_command_continue_on_error ("%s --get -f std.out --dir %s/perusal %s"%(COMMAND,utils.get_job_output_dir(),JOBID))

        logging.info("Execute command: ls %s/perusal/std.out-*",utils.get_job_output_dir())

        OUTPUT=commands.getstatusoutput("ls %s/perusal/std.out-*"%(utils.get_job_output_dir()))
   
        if OUTPUT[0] != 0 :
            logging.error("No output seem to be obtained using glite-wms-job-perusal!")
            raise GeneralError("","No output seem to be obtained using glite-wms-job-perusal !")


    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    utils.show_progress("Test 12")

    try:

        logging.info("Test 12: Check --get, --nodisplay and --all options")
        utils.info ("")
        utils.info ("Test --get option with --nodisplay and --all")
        utils.run_command_continue_on_error ("%s --get -f out.txt --noint --nodisplay --all --dir %s/perusal %s"%(COMMAND,utils.get_job_output_dir(),JOBID))

        logging.info("Execute command: ls %s/perusal/out.txt-*",utils.get_job_output_dir())

        OUTPUT=commands.getstatusoutput("ls %s/perusal/out.txt-*"%(utils.get_job_output_dir()))

        if OUTPUT[0] != 0 :
            logging.error("No output seem to be obtained using glite-wms-job-perusal!")
            raise GeneralError ("","No output seem to be obtained using glite-wms-job-perusal !")

        utils.info ("Concatenate retrieved chunckes")

        logging.info("Concatenate retrieved chunckes")

        logging.info("Execute command: ls %s/perusal/out.txt-*",utils.get_job_output_dir())

        OUTPUT=commands.getstatusoutput("ls %s/perusal/out.txt-*"%(utils.get_job_output_dir()))

        lists=string.split(OUTPUT[1],'\n')

        for chunck in lists :
            utils.dbg("Next chunck is %s"%(chunck))
            logging.info("Next chunck is %s",chunck)
            utils.run_command_continue_on_error("cat %s >> %s/perusal/out.txt"%(chunck,utils.get_job_output_dir()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    utils.show_progress("Test 13")

    try:

        logging.info("Test 13: Retrieve the output")
        utils.info ("")
        utils.info ("Retrieve the output")
        utils.run_command_continue_on_error ("glite-wms-job-output --noint --nosubdir --dir %s %s"%(utils.get_job_output_dir(),JOBID))

        utils.info ("Check if the output file differs from the previous retrieved ones")
        logging.info("Check if the output file differs from the previous retrieved ones")
        utils.run_command_continue_on_error ("diff %s/perusal/std.out-* %s/std.out"%(utils.get_job_output_dir(),utils.get_job_output_dir()))
        utils.run_command_continue_on_error ("diff %s/perusal/out.txt %s/out.txt"%(utils.get_job_output_dir(),utils.get_job_output_dir()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
        
    ## cleaning files
    utils.remove ("%s/sleeper.sh"%(utils.get_tmp_dir()))

    OUTPUT = commands.getstatusoutput("ls %s/perusal/"%(utils.get_job_output_dir()))

    list=string.split(OUTPUT[1],'\n')

    for file in list :
        utils.remove("%s/perusal/%s"%(utils.get_job_output_dir(),file))

    OUTPUT = commands.getstatusoutput("ls %s/out.txt-*"%(utils.get_job_output_dir()))

    list=string.split(OUTPUT[1],'\n')

    for file in list :
        utils.remove ("%s"%(file))
    
    os.rmdir("%s/perusal"%(utils.get_job_output_dir()))

    
    if fails > 0 :
      utils.exit_failure("%s test(s) fail(s)"%(fails))
    else:
      utils.exit_success()



if __name__ == "__main__":
    main()
