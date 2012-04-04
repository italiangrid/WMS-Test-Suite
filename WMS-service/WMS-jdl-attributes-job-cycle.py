#! /usr/bin/python

import sys
import signal
import os
import os.path
import time
import commands
import traceback

import Test_utils
import Job_utils
import SSH_utils

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



def set_jdl_data(utils,filename,dir):

    utils.info("Define a jdl with data requirements")

    FILE=open(filename,"w")

    FILE.write("Executable = \"test.sh\";\n")
    FILE.write("StdOutput = \"std.out\";\n")
    FILE.write("StdError = \"std.err\";\n")
    FILE.write("Arguments = \"lfn:%s/file1.txt\";\n"%(dir))
    FILE.write("FuzzyRank = true;\n")
    FILE.write("Environment={\"LFC_HOST=%s\",\"LFC_HOME=%s:%s\"};\n"%(utils.LFC,utils.LFC,dir))
    FILE.write("InputSandbox = {\"%s/test.sh\"};\n"%(utils.get_tmp_dir()))
    FILE.write("OutputSandbox = {\"std.out\", \"std.err\",\"test.out\"};\n")

    FILE.write("DataRequirements = {\n")
    FILE.write("[\n")
    FILE.write("DataCatalogType = \"DLI\";\n")
    FILE.write("DataCatalog =\"%s:8085/\";\n"%(utils.LFC))
    FILE.write("InputData = { \"lfn:%s/file1.txt\" };\n"%(dir))
    FILE.write("]\n")
    FILE.write("};\n")

    FILE.write("DataAccessProtocol = \"gsiftp\";\n")
    FILE.write("AllowZippedISB=true;\n")
    FILE.write("RetryCount = 1;\n")
    FILE.write("ShallowRetryCount = 2;\n")

    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))

    FILE=open("%s/test.sh"%(utils.get_tmp_dir()),"w")
    FILE.write("#!/bin/sh\n")
    FILE.write("lcg-cp --vo %s $1 file:`pwd`/file1.txt\n"%(utils.VO))
    FILE.write("ls -la\n")
    FILE.close()


def set_jdl_outputdata(utils,filename,dir):

    utils.info("Define a jdl with outputdata requirements")

    FILE=open(filename,"w")

    FILE.write("Executable = \"outputdata.sh\";\n")
    FILE.write("StdOutput = \"std.out\";\n")
    FILE.write("StdError = \"std.err\";\n")
    FILE.write("FuzzyRank = true;\n")
    FILE.write("Environment={\"LFC_HOST=%s\",\"LFC_HOME=%s:%s\"};\n"%(utils.LFC,utils.LFC,dir))
    FILE.write("InputSandbox = {\"%s/outputdata.sh\"};\n"%(utils.get_tmp_dir()))
    FILE.write("OutputSandbox = {\"std.out\", \"std.err\"};\n")

    FILE.write("OutputData = {\n")

    FILE.write("[\n")
    FILE.write("Outputfile = \"\";\n")
    FILE.write("LogicalFileName =\"%s\";\n")
    FILE.write("],\n")
    FILE.write("[\n")
    FILE.write("Outputfile = \"\";\n")
    FILE.write("StorageElement = \"%s\";\n")
    FILE.write("],\n")
    FILE.write("[\n")
    FILE.write("Outputfile = \"\";\n")
    FILE.write("StorageElement = \"%s\";\n")
    FILE.write("LogicalFileName =\"%s\";\n")
    FILE.write("],\n")
    FILE.write("[\n")
    FILE.write("Outputfile = \"\";\n")
    FILE.write("]\n")
    FILE.write("};\n")

    FILE.write("DataAccessProtocol = \"gsiftp\";\n")
    FILE.write("AllowZippedISB=true;\n")
    FILE.write("RetryCount = 1;\n")
    FILE.write("ShallowRetryCount = 2;\n")

    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))

    FILE=open("%s/outputdata.sh"%(utils.get_tmp_dir()),"w")    
    FILE.write("#!/bin/sh\n")
    FILE.write("files=(result_1.txt result_2.txt result_3.txt result_4.txt) \n")
    FILE.write("for i in \"${files[@]}\" \n")
    FILE.write("do \n")
    FILE.write("    echo \"=============================\" >$i \n")
    FILE.write("    echo \"\" >> $i \n")
    FILE.write("    date >> $i \n")
    FILE.write("    echo \"\" >> $i \n")
    FILE.write("    echo \"=============================\" >$i \n")
    FILE.write("done \n")
    FILE.close()


def set_ISBBase(utils,filename):

    utils.info("Define a jdl with ISBBaseURI attribute")

    FILE=open(filename,"w")

    FILE.write("Executable = \"test.sh\";\n")
    FILE.write("StdOutput = \"std.out\";\n")
    FILE.write("StdError = \"std.err\";\n")
    FILE.write("FuzzyRank = true;\n")

    FILE.write("InputSandboxBaseURI = \"gsiftp://%s:2811/tmp/%s/isb\";\n"%(utils.ISB_DEST_HOSTNAME,utils.ID))

    FILE.write("InputSandbox = {\"test.sh\",\"test1.txt\"};\n")

    FILE.write("OutputSandbox = {\"std.out\", \"std.err\"};\n")

    FILE.write("DataAccessProtocol = \"gsiftp\";\n")
    FILE.write("RetryCount = 1;\n")
    FILE.write("ShallowRetryCount = 2;\n")

    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))

    utils.info("Create executable script (test.sh) and test1.txt file at remote host: %s"%(utils.ISB_DEST_HOSTNAME))

    ssh=SSH_utils.open_ssh(utils.ISB_DEST_HOSTNAME,utils.ISB_DEST_USERNAME,utils.ISB_DEST_PASSWORD)

    SSH_utils.execute_remote_cmd(ssh,"rm -f /tmp/%s/isb/*"%(utils.ID))

    SSH_utils.execute_remote_cmd(ssh,"echo \"#!/bin/sh\" > /tmp/%s/isb/test.sh"%(utils.ID))
    SSH_utils.execute_remote_cmd(ssh,"echo $GLITE_WMS_JOBID >> /tmp/%s/isb/test.sh"%(utils.ID))
    SSH_utils.execute_remote_cmd(ssh,"echo \"ls -la\" >> /tmp/%s/isb/test.sh"%(utils.ID))

    SSH_utils.execute_remote_cmd(ssh,"touch /tmp/%s/isb/test1.txt"%(utils.ID))

    SSH_utils.close_ssh(ssh)



def set_OSBBaseDest(utils,filename):

    utils.info("Define a jdl with OutputSandboxBaseDestURI attribute")

    FILE=open(filename,"w")

    FILE.write("Executable = \"test.sh\";\n")
    FILE.write("StdOutput = \"std.out\";\n")
    FILE.write("StdError = \"std.err\";\n")
    FILE.write("FuzzyRank = true;\n")

    FILE.write("InputSandbox = {\"%s/test.sh\"};\n"%(utils.get_tmp_dir()))

    FILE.write("OutputSandbox = {\"std.out\", \"std.err\"};\n")

    FILE.write("OutputSandboxBaseDestURI = \"gsiftp://%s:2811/tmp/%s/osbbase/\";\n"%(utils.OSB_DEST_HOSTNAME,utils.ID))

    FILE.write("DataAccessProtocol = \"gsiftp\";\n")
    FILE.write("RetryCount = 1;\n")
    FILE.write("ShallowRetryCount = 2;\n")

    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))

    utils.info("Create executable script (test.sh)")

    FILE=open("%s/test.sh"%(utils.get_tmp_dir()),"w")
    FILE.write("#!/bin/sh\n")
    FILE.write("echo $GLITE_WMS_JOBID\n")
    FILE.write("ls -la\n")
    FILE.close()


def set_OSBDest(utils,filename):

    utils.info("Define a jdl with OutputSandboxDestURI attribute")

    FILE=open(filename,"w")

    FILE.write("Executable = \"test.sh\";\n")
    FILE.write("StdOutput = \"std.out\";\n")
    FILE.write("StdError = \"std.err\";\n")
    FILE.write("FuzzyRank = true;\n")

    FILE.write("InputSandbox = {\"%s/test.sh\"};\n"%(utils.get_tmp_dir()))

    FILE.write("OutputSandbox = {\"std.out\", \"std.err\"};\n")

    FILE.write("OutputSandboxDestURI = {\"gsiftp://%s:2811/tmp/%s/osbdest/\",\"std.err\"};\n"%(utils.OSB_DEST_HOSTNAME,utils.ID))

    FILE.write("DataAccessProtocol = \"gsiftp\";\n")
    FILE.write("RetryCount = 1;\n")
    FILE.write("ShallowRetryCount = 2;\n")

    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))

    utils.info("Create executable script (test.sh)")

    FILE=open("%s/test.sh"%(utils.get_tmp_dir()),"w")
    FILE.write("#!/bin/sh\n")
    FILE.write("echo $GLITE_WMS_JOBID\n")
    FILE.write("ls -la\n")
    FILE.close()


def test1(utils,title):

    utils.show_progress(title)
    utils.info(title)

    try:

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
                utils.error("Message %s not found"%(message))
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

                utils.info("Check std output to see if all the files are transferred to the CE")

                output=utils.run_command_continue_on_error("cat %s/std.out"%(utils.get_job_output_dir()))

                for file in files:

                  utils.info("Check for file %s to std.out"%(file))

                  if output.find(file)==-1:
                       utils.error("File %s is not transferred to the CE"%(file))
                       return 1
                  else:
                       utils.info("File %s is successfully transferred to the CE"%(file))
                return 0

            else:
                utils.error("Output files are not correctly retrieved")
                return 1

        else:
            utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            return 1

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
    utils.info(title)

    try:

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


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0



def test3(utils,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        ###Create jdl with ShortDeadlineJob attribute enabled
        utils.set_isb_jdl(utils.get_jdl_file())
        utils.add_jdl_general_attribute("RetryCount",1)
        utils.add_jdl_general_attribute("ShortDeadlineJob","true")

        fails=0

        utils.show_progress("Case A: Submit to an LCG-CE")
        utils.info("\tCase A: Submit to an LCG-CE")

        utils.set_destination_ce(utils.get_jdl_file(),"2119/jobmanager")

        output=utils.run_command_continue_on_error("glite-wms-job-list-match %s -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        if output.find("No Computing Element matching your job requirements has been found!")!=-1:
            utils.error("No Computing Element matching your job requirements has been found!")
            fails=fails+1
        else:
            result=Job_utils.submit_normal_job(utils,"2119/jobmanager")

            if result[0] == 1 :
                utils.error(result[1])
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

        output=utils.run_command_continue_on_error("glite-wms-job-list-match %s -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        if output.find("No Computing Element matching your job requirements has been found!")!=-1:
            utils.error("No Computing Element matching your job requirements has been found!")
            fails=fails+1
        else:

            result=Job_utils.submit_normal_job(utils,"/cream-")

            if result[0] == 1 :
                utils.error(result[1])
                fails=fails+1
            else:
                utils.dbg("Clean job output directory")
                os.system("rm -rf %s"%(utils.get_job_output_dir()))

        utils.show_progress("Case C: Submit without restrictions")
        utils.info("\tCase C: Submit without restrictions")

        utils.set_isb_jdl(utils.get_jdl_file())
        utils.add_jdl_general_attribute("RetryCount",1)
        utils.add_jdl_general_attribute("ShortDeadlineJob","true")

        output=utils.run_command_continue_on_error("glite-wms-job-list-match %s -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        if output.find("No Computing Element matching your job requirements has been found!")!=-1:
            utils.error("No Computing Element matching your job requirements has been found!")
            fails=fails+1
        else:

            result=Job_utils.submit_normal_job(utils)

            if result[0] == 1 :
                utils.error(result[1])
                fails=fails+1
            else:
                utils.dbg("Clean job output directory")
                os.system("rm -rf %s"%(utils.get_job_output_dir()))


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return fails

    return fails



def datarequirements_test(utils,target,dir):

  try:

        set_jdl_data(utils,utils.get_jdl_file(),dir)

        utils.set_destination_ce(utils.get_jdl_file(),target)

        utils.info("Check for matched CEs")

        output=utils.run_command_continue_on_error("glite-wms-job-list-match %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        if output.find("No Computing Element matching your job requirements has been found")!=-1:
            utils.error("Unable to find any CEs matching the job requirements")
            raise GeneralError("","Unable to find any CEs matching the job requirements")

        utils.info("Submit job and wait to finish")

        JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.wait_until_job_finishes(JOBID)

        utils.info("Check job's output")

        utils.job_status(JOBID)

        if utils.get_job_status().find("Done") != -1 :

            utils.remove(utils.get_tmp_file())

            utils.info("Retrieve the output")

            utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

            utils.info("Check if the output files are correctly retrieved")

            if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
                utils.info("Output files are correctly retrieved")
            else:
                utils.error("Output files are not correctly retrieved")
                raise GeneralError("Check output files","Output files are not correctly retrieved")
            

            utils.info("Check if file 'file1.txt' exists at job output")

            output=utils.run_command_continue_on_error("cat %s/std.out"%(utils.get_job_output_dir()))

            if output.find("file1.txt")!=-1:
                utils.info("Check OK, file 'file1.txt' found at job output")
            else:
                utils.error("Unable to find file 'file1.txt' at job output")
                raise GeneralError("Check job ouput","Unable to find file 'file1.txt' at job output")
                

        else:
            utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            raise GeneralError("Check final job status","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
        

        utils.info("TEST CASE PASS.")

  except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

  return 0


def test4(utils,title):

    utils.show_progress(title)
    utils.info(title)

    fails=0

    try:

            if utils.LFC=='' or utils.SE=='':
                utils.warn("To run this test you have to set LFC and SE attributes at configuration file")
                utils.show_progress("To run this test you have to set LFC and SE attributes at configuration file")
                return 1

            dir="/grid/%s/%s"%(utils.VO,utils.ID)

            utils.info("Create the directory %s"%(dir))

            os.environ['LFC_HOST']=utils.LFC

            utils.run_command_continue_on_error("lfc-mkdir %s"%(dir))

            utils.info("Create the file file1.txt")

            utils.run_command_continue_on_error("lcg-cr --vo %s -d %s -l lfn:%s/file1.txt file://%s/file1.txt"%(utils.VO,utils.SE,dir,os.getcwd()))

            target_ces=['/cream-','2119/jobmanager']
            target_info=['Submit to CREAM CE','Submit to LCG CE']

            
            for target in target_ces:

                utils.show_progress(target_info[target_ces.index(target)])

                utils.info("TEST CASE: %s"%(target_info[target_ces.index(target)]))

                utils.run_command_continue_on_error("rm -rf %s/*"%(utils.get_job_output_dir()))

                if datarequirements_test(utils,target,dir)==1:
                    fails=fails+1


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        fails=fails+1
        return fails
        
    return fails


def isbbaseuri_test(utils,target_ce):

    try:

            set_ISBBase(utils,utils.get_jdl_file())

            utils.set_destination_ce(utils.get_jdl_file(),target_ce)

            utils.info("Submit job")

            JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

            utils.info("Wait until job finishes")

            utils.wait_until_job_finishes(JOBID)

            utils.info("Check job's output")

            utils.job_status(JOBID)

            if utils.get_job_status().find("Done") != -1 :

                utils.remove(utils.get_tmp_file())

                utils.info("Retrieve the output")

                utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

                utils.info("Check if the output files are correctly retrieved")

                if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
                    utils.info("Output files are correctly retrieved")
                else:
                    utils.error("Output files are not correctly retrieved")
                    raise GeneralError("Check if output files are correctly retrieved","Output files are not correctly retrieved")


                utils.info("Check for test1.txt file in std.out")

                output=utils.run_command_continue_on_error("cat %s/std.out"%(utils.get_job_output_dir()))

                if output.find("test1.txt")!=-1:
                    utils.info("test1.txt found in std.out")
                else:
                    utils.error("Unable to find file 'test1.txt' in std.out")
                    raise GeneralError("Unable to find file 'test1.txt' in std.out")

            else:
                utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
                raise GeneralError("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1


    return 0



def test5(utils,title):

    utils.show_progress(title)
    utils.info(title)

    fails=0

    try:

        if utils.ISB_DEST_HOSTNAME=='' or utils.ISB_DEST_USERNAME=='' or utils.ISB_DEST_PASSWORD=='' :
            utils.warn("Please set the required variables for ISB node in test's configuration file")
            utils.show_progress("Please set the required variables for ISB node in test's configuration file")
            return 1


        ssh=SSH_utils.open_ssh(utils.ISB_DEST_HOSTNAME,utils.ISB_DEST_USERNAME,utils.ISB_DEST_PASSWORD)
        SSH_utils.execute_remote_cmd(ssh,"mkdir -p /tmp/%s/isb"%(utils.ID))
        SSH_utils.close_ssh(ssh)

        target_ces=['/cream-','2119/jobmanager']

        target_info=['Submit to CREAM CE','Submit to LCG CE']


        for target in target_ces:

            utils.show_progress(target_info[target_ces.index(target)])

            utils.info("TEST CASE: %s"%(target_info[target_ces.index(target)]))

            utils.run_command_continue_on_error("rm -rf %s/*"%(utils.get_job_output_dir()))

            if isbbaseuri_test(utils,target)==1:
                    fails=fails+1

                 
    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        fails=fails+1

    return fails



def osbbasetdesturi_test(utils,target_ce,ssh):
    
    try:

            SSH_utils.execute_remote_cmd(ssh,"rm -f /tmp/%s/osbbase/*"%(utils.ID))

            set_OSBBaseDest(utils,utils.get_jdl_file())

            utils.set_destination_ce(utils.get_jdl_file(),target_ce)

            utils.info("Submit job")

            JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

            utils.info("Wait until job finishes")

            utils.wait_until_job_finishes(JOBID)

            utils.info("Check job's output")

            utils.job_status(JOBID)

            if utils.get_job_status().find("Done") != -1 :

                utils.remove(utils.get_tmp_file())

                utils.info("Retrieve the output")

                utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

                utils.info("Check UI for output files")

                if len(os.listdir(utils.get_job_output_dir()))==0:
                    utils.info("Output files have not been transferred to UI as expected")
                else:
                    utils.error("Output files have been transferred to UI")
                    raise GeneralError("Check if output files have been transferred to UI","Output files have been transferred to UI")


                utils.info("Check if output files have been transferred to remote host %s"%(utils.OSB_DEST_HOSTNAME))
              
                files=SSH_utils.execute_remote_cmd(ssh,"ls /tmp/%s/osbbase/"%(utils.ID)).split(" ")

                files = map(lambda s: s.strip(), files)

                expected=['std.out','std.err']

                if len(files)!=len(expected):
                    utils.error("Wrong number of output files. Find %s while expected %s"%(len(files),len(expected)))
                    raise GeneralError("Check number of ouput files","Wrong number of output files. Find %s while expected %s"%(len(files),len(expected)))
                
                if len(set(files)&set(expected))!=len(expected):
                    utils.error("Unable to find all the expected output files. Find: %s , expected : %s"%(' , '.join(files),' , '.join(expected)))
                    raise GeneralError("Check output files","Unable to find all the expected output files. Find: %s , expected : %s"%(' , '.join(files),' , '.join(expected)))


                utils.info("Check content of std.out file")

                output=SSH_utils.execute_remote_cmd(ssh,"cat /tmp/%s/osbbase/std.out"%(utils.ID))

                values=[JOBID,'std.out','std.err','test.sh']

                for value in values:
                    if output.find(value)!=-1:
                        utils.info("Find: %s"%(value))
                    else:
                        utils.error("Unable to find '%s' in std.out"%(value))
                        raise GeneralError("Check content of std.out file","Unable to find '%s' in std.out"%(value))

            else:
                utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
                raise GeneralError("Check job status","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0



def test6(utils,title):

    utils.show_progress(title)
    utils.info(title)

    fails=0

    try:

        if utils.OSB_DEST_HOSTNAME=='' or utils.OSB_DEST_USERNAME=='' or utils.OSB_DEST_PASSWORD=='' :
            utils.warn("Please set the required variables for OSB node in test's configuration file")
            utils.show_progress("Please set the required variables for OSB node in test's configuration file")
            return 1

        target_ces=['/cream-','2119/jobmanager']

        target_info=['Submit to CREAM CE','Submit to LCG CE']

        ssh=SSH_utils.open_ssh(utils.OSB_DEST_HOSTNAME,utils.OSB_DEST_USERNAME,utils.OSB_DEST_PASSWORD)
        SSH_utils.execute_remote_cmd(ssh,"mkdir -p -m 0777 /tmp/%s/osbbase"%(utils.ID))
        
        for target in target_ces:

            utils.show_progress(target_info[target_ces.index(target)])

            utils.info("TEST CASE: %s"%(target_info[target_ces.index(target)]))

            utils.run_command_continue_on_error("rm -rf %s/*"%(utils.get_job_output_dir()))

            if osbbasetdesturi_test(utils,target,ssh)==1:
                    fails=fails+1


        SSH_utils.close_ssh(ssh)

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        fails=fails+1

    SSH_utils.close_ssh(ssh)

    return fails


def osbdesturi_test(utils,target_ce,ssh):

    try:

            SSH_utils.execute_remote_cmd(ssh,"rm -f /tmp/%s/osbdest/*"%(utils.ID))

            set_OSBDest(utils,utils.get_jdl_file())

            utils.set_destination_ce(utils.get_jdl_file(),target_ce)

            utils.info("Submit job")

            JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

            utils.info("Wait until job finishes")

            utils.wait_until_job_finishes(JOBID)

            utils.info("Check job's output")

            utils.job_status(JOBID)

            if utils.get_job_status().find("Done") != -1 :

                utils.remove(utils.get_tmp_file())

                utils.info("Retrieve the output")

                utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

                utils.info("Check UI for std.err file")

                if len(os.listdir(utils.get_job_output_dir()))==1:

                    utils.info("Find 1 file as expected , check its name")

                    if os.path.isfile("%s/std.err"%(utils.get_job_output_dir())):
                        utils.info("OK for std.err file")
                    else:
                        utils.error("One file transferred to UI but not the expected (std.err)")
                        raise GeneralError("","One file has been transferred to UI but not the expected (std.err)")

                else:
                    utils.error("Wrong number of files have been transferred to UI")
                    raise GeneralError("Check UI for std.err file","Wrong number of files have been transferred to UI")


                utils.info("Check if file std.out has been transferred to remote host %s"%(utils.OSB_DEST_HOSTNAME))

                files=SSH_utils.execute_remote_cmd(ssh,"ls /tmp/%s/osbdest/"%(utils.ID)).split(" ")

                files = map(lambda s: s.strip(), files)

                expected=['std.out']

                if len(files)!=len(expected):
                    utils.error("Wrong number of output files. Find %s while expected only %s"%(len(files),len(expected)))
                    raise GeneralError("Check number of ouput files","Wrong number of output files. Find %s while expected only %s"%(len(files),len(expected)))


                if len(set(files)&set(expected))!=len(expected):
                    utils.error("Unable to find all the expected output files. Find: %s , expected : %s"%(','.join(files),','.join(expected)))
                    raise GeneralError("Check output files","Unable to find all the expected output files. Find: %s , expected : %s"%(','.join(files),','.join(expected)))


                utils.info("Check content of std.out file")

                output=SSH_utils.execute_remote_cmd(ssh,"cat /tmp/%s/osbdest/std.out"%(utils.ID))

                values=[JOBID,'std.out','std.err','test.sh']

                for value in values:
                    if output.find(value)!=-1:
                        utils.info("Find: %s"%(value))
                    else:
                        utils.error("Unable to find '%s' in std.out"%(value))
                        raise GeneralError("Check content of std.out file","Unable to find '%s' in std.out"%(value))

            else:
                utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
                raise GeneralError("Check job status","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0


def test7(utils,title):

    utils.show_progress(title)
    utils.info(title)

    fails=0

    try:

        if utils.OSB_DEST_HOSTNAME=='' or utils.OSB_DEST_USERNAME=='' or utils.OSB_DEST_PASSWORD=='' :
            utils.warn("Please set the required variables for OSB node in test's configuration file")
            utils.show_progress("Please set the required variables for OSB node in test's configuration file")
            return 1

        target_ces=['/cream-','2119/jobmanager']

        target_info=['Submit to CREAM CE','Submit to LCG CE']

        ssh=SSH_utils.open_ssh(utils.OSB_DEST_HOSTNAME,utils.OSB_DEST_USERNAME,utils.OSB_DEST_PASSWORD)
        SSH_utils.execute_remote_cmd(ssh,"mkdir -p -m 0777 /tmp/%s/osbdest"%(utils.ID))

        for target in target_ces:

            utils.show_progress(target_info[target_ces.index(target)])

            utils.info("TEST CASE: %s"%(target_info[target_ces.index(target)]))

            utils.run_command_continue_on_error("rm -rf %s/*"%(utils.get_job_output_dir()))

            if osbdesturi_test(utils,target,ssh)==1:
                    fails=fails+1


        SSH_utils.close_ssh(ssh)

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        fails=fails+1

    SSH_utils.close_ssh(ssh)

    return fails




def test8(utils,title):


    utils.show_progress(title)
    utils.info(title)

    try:


        utils.info("TEST PASS.")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0




def main():
    	
    utils = Test_utils.Test_utils(sys.argv[0],"Test a complete job cycle for normal job with non default jdl files")

    tests=["Test 1: Jdl with AllowZippedISB"]
    tests.append("Test 2: Jdl with ExpiryTime")
    tests.append("Test 3: Jdl with ShortDeadlineJob")
    tests.append("Test 4: Jdl with DataRequirements")
    tests.append("Test 5: Jdl with InputSandboxBaseURI")
    tests.append("Test 6: Jdl with OutputSandboxBaseDestURI")
    tests.append("Test 7: Jdl with OutputSandboxDestURI")
    #tests.append("Test 8: Jdl with OutputData")
    
    
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

    if all_tests==1 or utils.check_test_enabled(4)==1 :
         if test4(utils, tests[3]):
            fails.append(tests[3])

    if all_tests==1 or utils.check_test_enabled(5)==1 :
         if test5(utils, tests[4]):
            fails.append(tests[4])
            
    if all_tests==1 or utils.check_test_enabled(6)==1 :
         if test6(utils, tests[5]):
                fails.append(tests[5])

    
    if all_tests==1 or utils.check_test_enabled(7)==1 :
         if test7(utils, tests[6]):
               fails.append(tests[6])

    """
    if all_tests==1 or utils.check_test_enabled(8)==1 :
         if test8(utils, tests[7]):
              fails.append(tests[7])
    """
    
    if len(fails) > 0 :
      utils.exit_failure("%s test(s) fail(s): %s"%(len(fails), fails))
    else:
      utils.exit_success()


if __name__ == "__main__":
    main()
