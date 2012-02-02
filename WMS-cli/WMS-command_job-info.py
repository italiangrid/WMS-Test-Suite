#! /usr/bin/python

import sys
import signal
import string
import logging
import traceback

from Exceptions import *

import Test_utils


def main():

    fails=0

    utils = Test_utils.Test_utils(sys.argv[0],"test glite-wms-job-info commmad")

    utils.prepare(sys.argv[1:])

    logging.info("Test glite-wms-job-info command")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    COMMAND="glite-wms-job-info"

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



    # Submit a job

    utils.define_delegation()

    utils.info ("Submit a job")
    logging.info("Submit a job")

    JOBID=utils.run_command ("glite-wms-job-submit %s -c %s --nomsg --output %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jobid_file(),utils.get_jdl_file()))

    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

    # Test manadatory options --jdl --jdl-original --proxy
    # combined with differents extra options

    logging.info("Start testing mandatory options --jdl --jdl-original --proxy")

    utils.info("Start testing mandatory options --jdl --jdl-original --proxy")

    options = ['--jdl', '--jdl-original', '--proxy']

    counter=2

    for opt in options :

        counter=counter+1

        utils.show_progress("Test %d"%(counter))

        try:

            logging.info("Test %d",counter)
        
            utils.info ("")
            logging.info("Test %s %s with --config option",COMMAND,opt)
            utils.info ("Test %s  %s with --config option"%(COMMAND,opt))
            utils.run_command_continue_on_error("%s --config %s %s %s"%(COMMAND,utils.get_config_file(),opt,JOBID))
        
            utils.info ("")
            logging.info("Test %s %s with --output option",COMMAND,opt)
            utils.info ("Test %s %s with --output option"%(COMMAND,opt))
            utils.run_command_continue_on_error ("%s --output %s %s %s"%(COMMAND,utils.get_output_file(),opt,JOBID))
            utils.info ("Check the output")
            logging.info("Check the output")
            utils.run_command_continue_on_error ("cat %s"%(utils.get_output_file()))
            utils.remove(utils.get_output_file())
        
            utils.info ("")
            logging.info("Test %s %s with --logfile option",COMMAND,opt)
            utils.info ("Test %s %s with --logfile option"%(COMMAND,opt))
            utils.run_command_continue_on_error ("%s --logfile %s %s %s"%(COMMAND,utils.get_log_file(),opt,JOBID))
            utils.info ("Check the logfile")
            logging.info("Check the logfile")
            utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
            utils.remove(utils.get_log_file())

            utils.info ("")
            logging.info("Test %s %s with --debug and --logfile options",COMMAND,opt)
            utils.info ("Test %s %s with --debug and --logfile options"%(COMMAND,opt))
            utils.run_command_continue_on_error ("%s --debug --logfile %s %s %s"%(COMMAND,utils.get_log_file(),opt,JOBID))
            utils.info ("Check the logfile (with debug option enabled)")
            logging.info("Check the logfile (with debug option enabled)")
            utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
            utils.remove(utils.get_log_file())

            utils.remove(utils.get_tmp_file())
            utils.info ("")
            logging.info("Test %s %s with --input option",COMMAND,opt)
            utils.info ("Test %s %s with --input option"%(COMMAND,opt))
            utils.run_command_continue_on_error ("%s --input %s %s >> %s"%(COMMAND,utils.get_jobid_file(),opt,utils.get_tmp_file()))
            utils.info("Check the command output")
            logging.info("Check the command output")
            utils.run_command_continue_on_error("cat %s"%(utils.get_tmp_file()))
            utils.remove(utils.get_tmp_file())

            utils.remove(utils.get_tmp_file())
            utils.info ("")
            logging.info("Test %s %s with --endpoint option",COMMAND,opt)
            utils.info ("Test %s %s with --endpoint option"%(COMMAND,opt))
            utils.run_command_continue_on_error ("%s --endpoint https://%s:7443/glite_wms_wmproxy_server %s %s "%(COMMAND,utils.get_WMS(),opt,JOBID))
       
        
            utils.info ("")
            logging.info("Test %s %s with all options",COMMAND,opt)
            utils.info ("Test %s %s with all options"%(COMMAND,opt))
            utils.run_command_continue_on_error ("%s --noint --debug --input %s --config %s --output %s --logfile %s %s"%(COMMAND,utils.get_jobid_file(),utils.get_config_file(),utils.get_output_file(),utils.get_log_file(),opt))
            utils.info ("Check the output file")
            logging.info("Check the output file")
            utils.run_command_continue_on_error ("cat %s"%(utils.get_output_file()))
            utils.info ("Check the logfile")
            logging.info("Check the logfile")
            utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
            utils.remove (utils.get_log_file())
            utils.remove (utils.get_output_file())

        except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

        
    logging.info("Start testing mandatory option --delegationid")
    utils.info("Start testing mandatory option --delegationid")
    counter=counter+1
    logging.info("Test %d",counter)
    utils.show_progress("Test %d"%(counter))

    try:

        utils.info ("")
        logging.info("Test %s  --delegationid with --config option",COMMAND)
        utils.info("Test %s  --delegationid with --config option"%(COMMAND))
        utils.run_command_continue_on_error("%s --config %s %s "%(COMMAND,utils.get_config_file(),utils.get_delegation_options()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    try:

        utils.info ("")
        logging.info ("Test %s --delegationid with --output option",COMMAND)
        utils.info ("Test %s --delegationid with --output option"%(COMMAND))
        utils.run_command_continue_on_error ("%s --output %s --config %s %s"%(COMMAND,utils.get_output_file(),utils.get_config_file(),utils.get_delegation_options()))
        utils.info ("Check the output file")
        logging.info ("Check the output file")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_output_file()))
        utils.remove(utils.get_output_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    try:

        utils.info ("")
        logging.info ("Test %s --delegationid with --logfile option",COMMAND)
        utils.info ("Test %s --delegationid with --logfile option"%(COMMAND))
        utils.run_command_continue_on_error ("%s --logfile %s --config %s %s"%(COMMAND,utils.get_log_file(),utils.get_config_file(),utils.get_delegation_options()))
        utils.info ("Check the logfile")
        logging.info ("Check the logfile")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
        utils.remove(utils.get_log_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    try:

        utils.info ("")
        logging.info ("Test %s --delegationid with --debug and --logfile options",COMMAND)
        utils.info ("Test %s --delegationid with --debug and --logfile options"%(COMMAND))
        utils.run_command_continue_on_error ("%s --debug --logfile %s --config %s %s"%(COMMAND,utils.get_log_file(),utils.get_config_file(),utils.get_delegation_options()))
        utils.info ("Check the logfile (with debug option enabled)")
        logging.info ("Check the logfile (with debug option enabled)")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
        utils.remove(utils.get_log_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())


    try:

        utils.info ("")
        logging.info ("Test %s --delegationid with with --endpoint option",COMMAND)
        utils.info ("Test %s --delegationid with with --endpoint option"%(COMMAND))
        utils.run_command_continue_on_error ("%s --endpoint https://%s:7443/glite_wms_wmproxy_server %s"%(COMMAND,utils.get_WMS(),utils.get_delegation_options()))

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())

    try:

        utils.info ("")
        logging.info("Test %s --delegationid with all options",COMMAND)
        utils.info ("Test %s --delegationid with all options"%(COMMAND))
        utils.run_command_continue_on_error ("%s --noint --debug --config %s --output %s --logfile %s --endpoint https://%s:7443/glite_wms_wmproxy_server %s"%(COMMAND,utils.get_config_file(),utils.get_output_file(),utils.get_log_file(),utils.get_WMS(),utils.get_delegation_options()))
        utils.info ("Check the output file")
        logging.info ("Check the output file")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_output_file()))
        utils.info ("Check the logfile")
        logging.info ("Check the logfile")
        utils.run_command_continue_on_error ("cat %s"%(utils.get_log_file()))
        utils.remove (utils.get_log_file())
        utils.remove (utils.get_output_file())

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
   
    ## some ad hoc tests

    counter=counter+1
    utils.show_progress("Test %d"%(counter))

    try:

        logging.info ("Test %d",counter)
        utils.info ("")

        logging.info("Check the edg_jobid parameter in the registered jdl")
        utils.info ("Check the edg_jobid parameter in the registered jdl")

        JID=utils.run_command_continue_on_error("%s --jdl %s | grep edg_jobid | awk -F= '{print $2}'| sed -e 's/\"//g' | sed -e 's/;//'"%(COMMAND,JOBID))

        JID=string.strip(JID)

        logging.info("Returned job id is %s",JID)
    
        if JID !=JOBID :
            logging.error("The registered jdl has not the correct Job Id. Expected JOBID:%s and returned JOBID:%s",JOBID,JID)
            raise GeneralError ("","The registered jdl has not the correct JOBID: %s"%(JID))
        else:
            utils.info (" -> Check success")

    except (RunCommandError,GeneralError,TimeOutError) , e :
            fails=fails+1
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
    
    counter=counter+1
    utils.show_progress("Test %d"%(counter))
    
    try:

        logging.info("Test %d",counter)
        utils.info ("")
        logging.info ("Check the expiration time of the delegation")
        utils.info ("Check the expiration time of the delegation")

        dexp = utils.run_command_continue_on_error ("%s -c %s %s | grep -m 1 Expiration | awk -F\" : \" '{print $2}'"%(COMMAND,utils.get_config_file(),utils.get_delegation_options()))
        pexp = utils.run_command_continue_on_error("%s -p %s | grep -m 1 Expiration | awk -F\" : \" '{print $2}'"%(COMMAND,JOBID))
   
        if  dexp != pexp :
            logging.error("The delegation proxy expires %s instead the user proxy expires %s",dexp,pexp)
            raise GeneralError("","The delegation proxy expires %s instead the user proxy expires %s"%(dexp,pexp))
        else:
            utils.info (" -> Check success")
    

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
