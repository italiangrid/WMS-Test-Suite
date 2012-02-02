#! /usr/bin/python

import sys
import signal
import os.path
import traceback
import commands
import re

from Exceptions import *

import Test_utils

# Check the correctness of the prologue output or raise GeneralError exception
def check_prologue(utils):

    utils.info("Check prologue output")
    FILE=open("%s/prologue.out"%(utils.get_job_output_dir()),"r")
    prolog=FILE.read()
    FILE.close()
    utils.dbg("Prologue output is: \n%s"%(prolog))
    if ( prolog.find("Prologue Arguments") == -1 or 
         prolog.find("TestVariable") == -1 ):
        utils.error("TEST FAILS. Prologue output is not correct.")
        raise GeneralError("Check the output files","prologue.out is not correct.")
        
# Check the correctness of the std output or raise GeneralError exception
def check_stdout(utils, prolog=0):  

    utils.info("Check executable output")
    FILE=open("%s/std.out"%(utils.get_job_output_dir()),"r")
    exe=FILE.read()
    FILE.close()
    utils.dbg("Executable output is: \n%s"%(exe))
    if ( exe.find("Executable Arguments") == -1 or 
         exe.find("TestVariable") == -1 or
         ( prolog and not len(re.findall("-rw-r--r-- .* prologue", exe)))):
        utils.error("TEST FAILS. Std output is not correct.")
        raise GeneralError("Check the output files","std.out is not correct.")           

# Check the correctness of the epilogue output or raise GeneralError exception
def check_epilogue(utils, prolog=0):  

    utils.info("Check epilogue output")
    FILE=open("%s/epilogue.out"%(utils.get_job_output_dir()),"r")
    epilogue=FILE.read()
    FILE.close()
    utils.dbg("Epilogue output is: \n%s"%(epilogue))
    if ( epilogue.find("Epilogue Arguments") == -1 or 
         epilogue.find("TestVariable") == -1  or 
         ( prolog and not len(re.findall("-rw-r--r-- .* prologue", epilogue))) or
         not len(re.findall("-rw-r--r-- .* executable", epilogue))):
        utils.error("TEST FAILS. Epilogue output is not correct.")
        raise GeneralError("Check the output files","epilogue.out is not correct.")   


def test1(utils, title):

    utils.show_progress(title)
    utils.info(title)

    try:

        utils.set_prologue_jdl(utils.get_jdl_file())

        JOBID = utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.wait_until_job_finishes(JOBID)

        utils.job_status(JOBID)

        if utils.get_job_status().find("Done (Success)")==-1:
            utils.error("TEST FAILS. Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            raise GeneralError("Check job final status","Job finishes with status %s cannot retrieve output"%(utils.get_job_status()))

        else:

            utils.dbg("Retrieve the output")
            utils.run_command_continue_on_error ("glite-wms-job-output --dir %s --noint --nosubdir %s"%(utils.get_job_output_dir(),JOBID))
            utils.info("Check if the output files are correctly retrieved")

            if( os.path.isfile("%s/prologue.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) ):

                utils.info("All output files are retrieved")

                # Check prologue output
                check_prologue(utils)

                # Check executable output
                check_stdout(utils,1)

                utils.dbg("Output files are as expected")

            else:
                utils.error("TEST FAILS. Output files are not retrieved")
                raise GeneralError("Check the output files","Output files are not retrieved")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    ## remove used files
    utils.remove("%s/prologue.sh"%(utils.get_tmp_dir()))
    utils.remove("%s/exe.sh"%(utils.get_tmp_dir()))
    os.system("rm -rf %s/*"%(utils.get_job_output_dir()))

    return 0



def test2(utils, title):

    utils.show_progress(title)
    utils.info(title)

    try:

        utils.set_epilogue_jdl(utils.get_jdl_file())

        JOBID = utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.wait_until_job_finishes(JOBID)

        utils.job_status(JOBID)

        if utils.get_job_status().find("Done (Success)")==-1:

            utils.error("TEST FAILS. Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            raise GeneralError("Check job final status","Job finishes with status %s cannot retrieve output"%(utils.get_job_status()))

        else:

            utils.info ("Retrieve the output")
            utils.run_command_continue_on_error ("glite-wms-job-output --dir %s --noint --nosubdir %s"%(utils.get_job_output_dir(),JOBID))
            utils.dbg ("Check if the output files are correctly retrieved")

            if( os.path.isfile("%s/epilogue.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.out"%(utils.get_job_output_dir()))) :

                utils.info ("All output files are retrieved")

                # Check executable output
                check_stdout(utils)

                # Check epilogue output
                check_epilogue(utils)

                utils.dbg("Output files are as expected")

            else:
                utils.error("TEST FAILS. Output files are not retrieved")
                raise GeneralError("Check the output files","Output files are not retrieved")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    ## remove used files
    utils.remove("%s/epilogue.sh"%(utils.get_tmp_dir()))
    utils.remove("%s/exe.sh"%(utils.get_tmp_dir()))
    os.system("rm -rf %s/*"%(utils.get_job_output_dir()))

    return 0


def test3(utils, title):


    utils.show_progress(title)
    utils.info(title)

    try:

        utils.set_prologue_epilogue_jdl(utils.get_jdl_file())

        JOBID = utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.wait_until_job_finishes(JOBID)

        utils.job_status(JOBID)

        if utils.get_job_status().find("Done (Success)")==-1:

            utils.error("TEST FAILS. Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            raise GeneralError("Check job final status","Job finishes with status %s cannot retrieve output"%(utils.get_job_status()))

        else:
    
            utils.dbg ("Retrieve the output")
            utils.run_command ("glite-wms-job-output --dir %s --noint --nosubdir %s"%(utils.get_job_output_dir(),JOBID))
            utils.info ("Check if the output files are correctly retrieved")

            if( os.path.isfile("%s/prologue.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/epilogue.out"%(utils.get_job_output_dir()))):

                utils.info("All output files are retrieved")

                # Check prologue output
                check_prologue(utils)

                # Check executable output
                check_stdout(utils,1)
             
                # Check epilogue output
                check_epilogue(utils,1)             

                utils.dbg ("Output files are as expected")

            else:
                utils.error("TEST FAILS. Output files are not retrieved")
                raise GeneralError("Check the output files","Output files are not retrieved")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    ## remove used files
    utils.remove("%s/prologue.sh"%(utils.get_tmp_dir()))
    utils.remove("%s/exe.sh"%(utils.get_tmp_dir()))
    utils.remove("%s/epilogue.sh"%(utils.get_tmp_dir()))
    os.system("rm -rf %s"%(utils.get_job_output_dir()))
   
    return 0



def main():

    fails=[]
   
    tests=["Test 1: Test prologue attribute"]
    tests.append("Test 2: Test epilogue attribute")
    tests.append("Test 3: Test prologue and epilogue attributes")

    utils = Test_utils.Test_utils(sys.argv[0],"WMS test prologue and epilogue attributes")

    utils.prepare(sys.argv[1:],tests)

    utils.info("WMS test prologue and epilogue attributes")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

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

    if len(fails) > 0 :
      utils.exit_failure("%s test(s) fail(s): %s"%(len(fails), fails))
    else:
      utils.exit_success()  
  

if __name__ == "__main__":
    main()
