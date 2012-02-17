#! /usr/bin/python

import sys
import signal
import os
import time
import commands

import Test_utils
import Job_utils

from Exceptions import *

def set_zipped_jdl(utils,filename):

    utils.run_command_continue_on_error("cp %s %s/fileA"%(utils.get_config_file(),utils.get_tmp_dir()))
    utils.run_command_continue_on_error("cp %s %s/fileB"%(utils.get_config_file(),utils.get_tmp_dir()))
    utils.run_command_continue_on_error("cp %s %s/fileC"%(utils.get_config_file(),utils.get_tmp_dir()))
    utils.run_command_continue_on_error("cp %s %s/fileD"%(utils.get_config_file(),utils.get_tmp_dir()))

    utils.run_command_continue_on_error("tar czf %s/test_zipped_isb.tgz %s/file*"%(utils.get_tmp_dir(),utils.get_tmp_dir()))

    utils.info("Define a jdl with atrribute ZippedISB enabled")
    
    FILE=open(filename,"w")

    FILE.write("Executable = \"/bin/ls\";\n")
    FILE.write("Arguments = \"-la\";\n")
    FILE.write("StdOutput = \"std.out\";\n")
    FILE.write("StdError = \"std.err\";\n")
    FILE.write("InputSandbox = {\"%s/fileA\", \"%s/fileB\", \"%s/fileC\", \"%s/fileD\" , \"%s/test_zipped_isb.tgz\"};\n"%(utils.get_tmp_dir(),utils.get_tmp_dir(),utils.get_tmp_dir(),utils.get_tmp_dir(),utils.get_tmp_dir()))
    FILE.write("OutputSandbox = {\"std.out\", \"std.err\"};\n")
    FILE.write("ZippedISB = \"%s/test_zipped_isb.tgz\";\n"%(utils.get_tmp_dir()))
    FILE.write("RetryCount = 1;\n")
    FILE.write("ShallowRetryCount = 2;\n")

    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


def set_allowzipped_jdl(utils,filename):

    utils.run_command_continue_on_error("cp %s %s/fileA"%(utils.get_config_file(),utils.get_tmp_dir()))
    utils.run_command_continue_on_error("cp %s %s/fileB"%(utils.get_config_file(),utils.get_tmp_dir()))
    utils.run_command_continue_on_error("cp %s %s/fileC"%(utils.get_config_file(),utils.get_tmp_dir()))
    utils.run_command_continue_on_error("cp %s %s/fileD"%(utils.get_config_file(),utils.get_tmp_dir()))
    
    utils.info("Define a jdl with atrribute AllowZippedISB enabled")
    
    FILE=open(filename,"w")

    FILE.write("Executable = \"/bin/ls\";\n")
    FILE.write("Arguments = \"-la\";\n")
    FILE.write("StdOutput = \"std.out\";\n")
    FILE.write("StdError = \"std.err\";\n")
    FILE.write("InputSandbox = {\"%s/fileA\", \"%s/fileB\", \"%s/fileC\", \"%s/fileD\"};\n"%(utils.get_tmp_dir(),utils.get_tmp_dir(),utils.get_tmp_dir(),utils.get_tmp_dir()))
    FILE.write("OutputSandbox = {\"std.out\", \"std.err\"};\n")
    FILE.write("AllowZippedISB=true;\n")
    FILE.write("RetryCount = 1;\n")
    FILE.write("ShallowRetryCount = 2;\n")

    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))



def set_jdl_data(utils, filename,VO,LFC,dir):

    utils.info("Define a jdl with data requirements")

    FILE=open(filename,"w")

    FILE.write("Executable = \"/bin/ls\";\n")
    FILE.write("Arguments = \"-la\";\n")
    FILE.write("StdOutput = \"std.out\";\n")
    FILE.write("StdError = \"std.err\";\n")
    FILE.write("FuzzyRank = true;\n")
    FILE.write("Environment={\"LFC_HOST=prod-lfc-shared-central.cern.ch\",\"LFC_HOME=prod-lfc-shared-central.cern.ch:/grid/dteam/aleph\"};\n")
    FILE.write("OutputSandbox = {\"std.out\", \"std.err\",\"prologue.out\", \"file.txt\"};\n")

    FILE.write("DataRequirements = {\n")
    FILE.write("[\n")
    FILE.write("DataCatalogType = \"DLI\";\n")
    FILE.write("DataCatalog =\"http://prod-lfc-shared-central.cern.ch:8085/\";\n")
    FILE.write("InputData = { \"guid:17c667b7-9622-4c95-be68-3d15d1eacadb\" };\n")
    FILE.write("]\n")
    FILE.write("};\n")

    FILE.write("DataAccessProtocol = \"gsiftp\";\n")
    FILE.write("AllowZippedISB=true;\n")
    FILE.write("RetryCount = 1;\n")
    FILE.write("ShallowRetryCount = 2;\n")

    FILE.close()
    
    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


def test1(utils,title):

    utils.show_progress(title)
    utils.info(title)

    set_allowzipped_jdl(utils,utils.get_jdl_file())

    utils.info("Submit job")

    output=utils.run_command_continue_on_error("glite-wms-job-submit %s --debug -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    messages=['File archiving and file compression allowed by user in the JDL']
    messages.append('Archiving the ISB files')
    messages.append('ISB ZIPPED file successfully created')

    utils.info("Check debug output for expected messages")

    for message in messages:

      utils.info("Check for message: %s"%(messages))

      if output.find(message)==-1:
         utils.info("Message %s not found"%(message))
         return 1
      else:
         utils.info("Message found")

    JOBID=''
    ZippedISB=''

    for line in output.split("\n"):
        if line.find("ISB ZIPPED file successfully created:")!=-1:
              ZippedISB=line.split('/tmp/')[1].strip(' \n')

        if line.find("The JobId is:")!=-1:
              JOBID=line.split('The JobId is:')[1].strip(' \n')

    utils.info("Check if AllowZippedISB Attribute is added:")

    output=utils.run_command_continue_on_error("glite-wms-job-info --jdl %s"%(JOBID))

    if output.find("AllowZippedISB = true;")!=-1:
       utils.info("Attribute AllowZippedISB successfully added to the jdl")
    else:
       utils.error("Attribute AllowZippedISB not added to the jdl")
       return 1

    utils.info("Check if ZippedISB Attribute is added:")

    if output.find("ZippedISB = { \"%s\" };"%(ZippedISB))!=-1:
       utils.info("Attribute ZippedISB successfully added to the jdl")
    else:
       utils.error("Unable to find ZippedISB={\"%s\"} to the jdl"%(ZippedISB))
       return 1

    utils.info("Wait until job finishes")

    utils.wait_until_job_finishes(JOBID)

    utils.info("Try to get the job output")

    utils.job_status(JOBID)

    files=['fileA','fileB','fileC','fileD']

    if utils.get_job_status().find("Done") != -1 :

            utils.remove(utils.get_tmp_file())

            utils.info("Retrieve the output")

            utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

            utils.info("Check if output files are correctly retrieved")

            if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :

                utils.info("Output files are correctly retrieved")

                utils.info("Check std output to see if all the files are transfered to the CE")

                output=utils.run_command_continue_on_error("cat %s/std.out"%(utils.get_job_output_dir()))

                for file in files:

                  utils.info("Check for file %s to std.out"%(file))

                  if output.find(file)==-1:
                       utils.error("File %s is not transfered to the CE"%(file))
                       return 1
                  else:
                       utils.info("File %s is successfully transfered to the CE"%(file))
                return 0

            else:
                utils.error("Output files are not correctly retrieved")
                return 1

    else:
        utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
        return 1

    return 0


"""
def test2(utils,title):

    utils.show_progress(title)
    utils.info(title)

    set_zipped_jdl(utils,utils.get_jdl_file())

    return 1
    
    utils.info("Submit job")

    output=utils.run_command_continue_on_error("glite-wms-job-submit %s --debug -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    messages=['File archiving and file compression allowed by user in the JDL']
    messages.append('Archiving the ISB files')
    messages.append('ISB ZIPPED file successfully created')

    utils.info("Check debug output for expected messages")

    for message in messages:

      utils.info("Check for message: %s"%(messages))

      if output.find(message)==-1:
         utils.info("Message %s not found"%(message))
         return 1
      else:
         utils.info("Message found")

    JOBID=''
    ZippedISB=''

    for line in output.split("\n"):
        if line.find("ISB ZIPPED file successfully created:")!=-1:
              ZippedISB=line.split('/tmp/')[1].strip(' \n')

        if line.find("The JobId is:")!=-1:
              JOBID=line.split('The JobId is:')[1].strip(' \n')

    utils.info("Check if AllowZippedISB Attribute is added:")

    output=utils.run_command_continue_on_error("glite-wms-job-info --jdl %s"%(JOBID))

    if output.find("AllowZippedISB = true;")!=-1:
       utils.info("Attribute AllowZippedISB successfully added to the jdl")
    else:
       utils.error("Attribute AllowZippedISB not added to the jdl")
       return 1

    utils.info("Check if ZippedISB Attribute is added:")

    if output.find("ZippedISB = { \"%s\" };"%(ZippedISB))!=-1:
       utils.info("Attribute ZippedISB successfully added to the jdl")
    else:
       utils.error("Unable to find ZippedISB={\"%s\"} to the jdl"%(ZippedISB))
       return 1

    utils.info("Wait until job finishes")

    utils.wait_until_job_finishes(JOBID)

    utils.info("Try to get the job output")

    utils.job_status(JOBID)

    files=['fileA','fileB','fileC','fileD']

    if utils.get_job_status().find("Done") != -1 :

            utils.remove(utils.get_tmp_file())

            utils.info("Retrieve the output")

            utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

            utils.info("Check if output files are correctly retrieved")

            if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :

                utils.info("Output files are correctly retrieved")

                utils.info("Check std output to see if all the files are transfered to the CE")

                output=utils.run_command_continue_on_error("cat %s/std.out"%(utils.get_job_output_dir()))

                for file in files:

                  utils.info("Check for file %s to std.out"%(file))

                  if output.find(file)==-1:
                       utils.error("File %s is not transfered to the CE"%(file))
                       return 1
                  else:
                       utils.info("File %s is successfully transfered to the CE"%(file))
                return 0

            else:
                utils.error("Output files are not correctly retrieved")
                return 1

    else:
        utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
        return 1

    return 0

"""

def test2(utils,title):

    utils.show_progress(title)
    utils.info(title)

    utils.set_isb_jdl(utils.get_jdl_file())
    utils.add_jdl_general_attribute("RetryCount",1)

    # we need a jdl which doesn't match
    utils.set_requirements ("false")

    #set expiry time 2 minutes from now
    utils.add_jdl_general_attribute("ExpiryTime",int(time.time()+120))

    utils.info("Submit job")

    JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --nomsg --config %s  %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.info("Wait until job finishes")

    utils.wait_until_job_finishes(JOBID)

    utils.info("Check job's final status")

    utils.job_status(JOBID)

    if utils.get_job_status().find("Aborted")!=-1:

       utils.info("Job's final status is Aborted as expected")

       utils.info("Check failed reason")

       if utils.get_job_status_reason(JOBID).find("request expired")!=-1:
          utils.info("Aborted reason is 'request expired' as expected")
          return 0

       else:
          utils.error("Error: Job's final status is aborted by failed reason is '%s' , while expected is 'request expired'"%(utils.get_job_status_reason(JOBID)))
          return 1

    else:
       utils.error("Test Failed. Job's final status is not Aborted as expected , instead we get %s"%(utils.get_job_status()))
       return 1

    return 0


def test3(utils,title):

    utils.show_progress(title)
    utils.info(title)

    ###Create jdl with ShortDeadlineJob attribute enabled
    utils.set_isb_jdl(utils.get_jdl_file())
    utils.add_jdl_general_attribute("RetryCount",1)
    utils.add_jdl_general_attribute("ShortDeadlineJob","true")

    fails=0

    utils.show_progress("Case A: Submit to an LCG-CE")
    utils.info("\tCase A: Submit to an LCG-CE")

    utils.set_destination_ce(utils.get_jdl_file(),"2119/jobmanager")

    return 1

    result=Job_utils.submit_normal_job(utils,"2119/jobmanager")

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))

    utils.show_progress("Case B: Submit to a CREAM CE")
    utils.info("\tCase B: Submit to a CREAM CE")

    utils.set_isb_jdl(utils.get_jdl_file())
    utils.add_jdl_general_attribute("RetryCount",1)
    utils.add_jdl_general_attribute("ShortDeadlineJob","true")

    utils.set_destination_ce(utils.get_jdl_file(),"/cream-")

    result=Job_utils.submit_normal_job(utils,"/cream-")

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))

    utils.show_progress("Case C: Submit without restrictions")
    utils.info("\tCase C: Submit without restrictions")

    utils.set_isb_jdl(utils.get_jdl_file())
    utils.add_jdl_general_attribute("RetryCount",1)
    utils.add_jdl_general_attribute("ShortDeadlineJob","true")

    result=Job_utils.submit_normal_job(utils)

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))

    return fails


def test4(utils,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        if utils.ISB_DEST_HOSTNAME=='' or utils.ISB_DEST_USERNAME=='' or utils.ISB_DEST_PASSWORD=='':
            utils.warn("Please set the required variables in test's configuration file")
            utils.show_progress("Please set the required variables in test's configuration file")
            return 1

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
        SSH_utils.close_ssh(ssh)
        return 1

    return 0
        


def main():
    	
    utils = Test_utils.Test_utils(sys.argv[0],"Test a complete job cycle for normal job with non default jdl files")

    tests=["Test 1: Jdl with AllowZippedISB"]
    tests.append("Test 2: Jdl with ExpiryTime")
    tests.append("Test 3: Jdl with ShortDeadlineJob")
    #tests.append("Test 4: Jdl with ISBBaseURI and OSBDestURI")
    #tests.append("Test 5: Jdl with ISBBaseURI and OSBBaseDestURI")
    #tests.append("Test 4: Jdl with DataRequirements")
    
    utils.prepare(sys.argv[1:],tests)

    utils.info("Test a complete job cycle: from submission to get output")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    fails=[]

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
