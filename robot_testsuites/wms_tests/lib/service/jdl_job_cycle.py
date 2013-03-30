
from Exceptions import *

import commands
import os.path
import os
import glob
import time
import SSH_utils



def target_ces_with_cream_default(utils,custom_requirements):

   CES=[]
   NAMES=[]

   for requirement in custom_requirements:
       NAMES.append(requirement)
       CES.append(custom_requirements[requirement])

   if len(custom_requirements)>0:
         utils.EXTERNAL_REQUIREMENTS=1
   else:
         utils.EXTERNAL_REQUIREMENTS=0
         NAMES.append("Default Test - CREAM")
         CES.append("/cream-")

   return NAMES,CES



def set_allowzipped_jdl(utils,filename):

    utils.run_command("cp %s %s/fileA"%(utils.get_config_file(),utils.get_tmp_dir()))
    utils.run_command("cp %s %s/fileB"%(utils.get_config_file(),utils.get_tmp_dir()))
    utils.run_command("cp %s %s/fileC"%(utils.get_config_file(),utils.get_tmp_dir()))
    utils.run_command("cp %s %s/fileD"%(utils.get_config_file(),utils.get_tmp_dir()))
    
    utils.log_info("Define a jdl with atrribute AllowZippedISB enabled")
    
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

    utils.log_info("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))),'DEBUG')


def set_jdl_data(utils,filename,dir):

    utils.log_info("Define a jdl with data requirements")

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

    utils.log_info("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))),'DEBUG')

    FILE=open("%s/test.sh"%(utils.get_tmp_dir()),"w")
    FILE.write("#!/bin/sh\n")
    FILE.write("lcg-cp --vo %s $1 file:`pwd`/file1.txt\n"%(utils.VO))
    FILE.write("ls -la\n")
    FILE.close()


def set_ISBBase(utils,filename):

    utils.log_info("Define a jdl with ISBBaseURI attribute")

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

    utils.log_info("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))),'DEBUG')

    utils.log_info("Create executable script (test.sh) and test1.txt file at remote host: %s"%(utils.ISB_DEST_HOSTNAME))

    ssh=SSH_utils.open_ssh(utils.ISB_DEST_HOSTNAME,utils.ISB_DEST_USERNAME,utils.ISB_DEST_PASSWORD,utils)

    SSH_utils.execute_remote_cmd(utils,ssh,"rm -f /tmp/%s/isb/*"%(utils.ID))

    SSH_utils.execute_remote_cmd(utils,ssh,"echo \"#!/bin/sh\" > /tmp/%s/isb/test.sh"%(utils.ID))
    SSH_utils.execute_remote_cmd(utils,ssh,"echo $GLITE_WMS_JOBID >> /tmp/%s/isb/test.sh"%(utils.ID))
    SSH_utils.execute_remote_cmd(utils,ssh,"echo \"ls -la\" >> /tmp/%s/isb/test.sh"%(utils.ID))

    SSH_utils.execute_remote_cmd(utils,ssh,"touch /tmp/%s/isb/test1.txt"%(utils.ID))

    SSH_utils.close_ssh(ssh,utils)


def set_OSBBaseDest(utils,filename):

    utils.log_info("Define a jdl with OutputSandboxBaseDestURI attribute")

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

    utils.log_info("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))),'DEBUG')

    utils.log_info("Create executable script (test.sh)")

    FILE=open("%s/test.sh"%(utils.get_tmp_dir()),"w")
    FILE.write("#!/bin/sh\n")
    FILE.write("echo $GLITE_WMS_JOBID\n")
    FILE.write("ls -la\n")
    FILE.close()


def set_OSBDest(utils,filename):

    utils.log_info("Define a jdl with OutputSandboxDestURI attribute")

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

    utils.log_info("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))),'DEBUG')

    utils.log_info("Create executable script (test.sh)")

    FILE=open("%s/test.sh"%(utils.get_tmp_dir()),"w")
    FILE.write("#!/bin/sh\n")
    FILE.write("echo $GLITE_WMS_JOBID\n")
    FILE.write("ls -la\n")
    FILE.close()


def set_environment_jdl(utils,filename):

    utils.log_info("Define a jdl with Environment attribute")

    FILE=open(filename,"w")

    FILE.write("Executable = \"test.sh\";\n")
    FILE.write("StdOutput = \"std.out\";\n")
    FILE.write("StdError = \"std.err\";\n") 
    FILE.write("InputSandbox = {\"%s/test.sh\"};\n"%(utils.get_tmp_dir()))
    FILE.write("OutputSandbox = {\"std.out\", \"std.err\"};\n")
    FILE.write("RetryCount = 1;\n")
    FILE.write("ShallowRetryCount = 2;\n")
    FILE.write("Environment = {\"MY_TEST_VARIABLE=WMS-Service\"};\n")

    FILE.close()

    utils.log_info("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))),'DEBUG')

    utils.log_info("Create executable script (test.sh)")

    FILE=open("%s/test.sh"%(utils.get_tmp_dir()),"w")
    FILE.write("#!/bin/sh\n")
    FILE.write("echo $MY_TEST_VARIABLE\n")
    FILE.close()

    utils.log_info("The saved script is:\n%s"%(commands.getoutput("cat %s/test.sh"%(utils.get_tmp_dir()))),'DEBUG')


def set_jdl_for_perusalTimeInterval_test(utils,filename):

    utils.log_info("Define the sleeper script, which write 150 messages one every 20sec")

    FILE = open("%s/sleeper.sh"%(utils.MYTMPDIR),"w")

    FILE.write("#!/bin/sh\n")
    FILE.write("echo \"This is sleeper\"\n")
    FILE.write("echo \"This is sleeper\" > $1\n")
    FILE.write("for((i=1;i<=150;i++))\n")
    FILE.write("do \n")
    FILE.write("    echo \"message $i\" >> $1 \n")
    FILE.write("    sleep 20 \n")
    FILE.write("done \n")
    FILE.write("echo \"Stop sleeping!\" >> $1 \n")
    FILE.write("echo \"Stop sleeping!\" \n")

    FILE.close()

    utils.log_info("The saved script is:\n%s"%(commands.getoutput("cat %s/sleeper.sh"%(utils.MYTMPDIR))),'DEBUG')

    utils.log_info("Define a jdl with file perusal enabled")

    FILE = open(filename,"w")

    FILE.write("Executable = \"sleeper.sh\";\n")
    FILE.write("Arguments = \"out.txt\";\n")
    FILE.write("StdOutput = \"std.out\";\n")
    FILE.write("StdError = \"std.err\";\n")
    FILE.write("InputSandbox = \"%s/sleeper.sh\";\n"%(utils.MYTMPDIR))
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\",\"out.txt\"};\n")
    FILE.write("PerusalFileEnable = true;\n")

    FILE.close()

    utils.log_info("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))),'DEBUG')




def get_ids(message):

    JOBID=''
    ZippedISB=''

    for line in message.split("\n"):
       if line.find("ISB ZIPPED file successfully created:")!=-1:
          ZippedISB=line.split('/tmp/')[1].strip(' \n')

       if line.find("The JobId is:")!=-1:
          JOBID=line.split('The JobId is:')[1].strip(' \n')

    return (JOBID,ZippedISB)


def check_zipped_jdl_output(utils,jobid):

    
   utils.log_info("Try to get the job output")

   status=utils.get_job_status(jobid)

   files=['fileA','fileB','fileC','fileD']

   if status.find("Done") != -1 :

       utils.remove(utils.get_tmp_file())

       utils.log_info("Retrieve the output")

       utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid, utils.get_tmp_file()))

       utils.log_info("Check if output files are correctly retrieved")

       if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
           utils.log_info("Output files are correctly retrieved")

           utils.log_info("Check std output to see if all the files are transferred to the CE")

           output=utils.run_command("cat %s/std.out"%(utils.get_job_output_dir()))

           for file in files:

              utils.log_info("Check for file %s to std.out"%(file))

              if output.find(file)==-1:
                   utils.log_info("File %s is not transferred to the CE"%(file))
                   raise GeneralError("Check for files","File %s is not transferred to the CE"%(file))
              else:
                   utils.log_info("File %s is successfully transferred to the CE"%(file))
       
       else:
            utils.log_info("ERROR: Output files are not correctly retrieved")
            raise GeneralError("","Output files are not correctly retrieved")

   else:
         utils.log_info("ERROR: Job finishes with status: %s cannot retrieve output"%(status))
         raise GeneralError("Check job's output","Job finishes with status: %s cannot retrieve output"%(status))   



def datarequirements_test(utils,target,dir):

   set_jdl_data(utils,utils.get_jdl_file(),dir)
   
   if utils.EXTERNAL_REQUIREMENTS==0:
        utils.set_requirements("%s"%utils.DEFAULTREQ)
   else:
        utils.set_requirements("%s && %s"%(target,utils.DEFAULTREQ))

   utils.log_info("Check for matched CEs")

   output=utils.run_command("glite-wms-job-list-match %s --config %s %s"%(utils.get_delegation_options(), utils.get_config_file(), utils.get_jdl_file()))

   if output.find("No Computing Element matching your job requirements has been found")!=-1:
         utils.log_info("ERROR: Unable to find any CEs matching the job requirements")
         raise GeneralError("","Unable to find any CEs matching the job requirements")

   utils.log_info("Submit job and wait to finish")

   JOBID=utils.run_command("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

   utils.wait_until_job_finishes(JOBID)

   utils.log_info("Check job's output")

   status=utils.get_job_status(JOBID)

   if status.find("Done") != -1 :

        utils.remove(utils.get_tmp_file())

        utils.log_info("Retrieve the output")

        utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

        utils.log_info("Check if the output files are correctly retrieved")

        if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
             utils.log_info("Output files are correctly retrieved")
        else:
             utils.log_info("ERROR: Output files are not correctly retrieved")
             raise GeneralError("Check output files","Output files are not correctly retrieved")
            
        utils.log_info("Check if file 'file1.txt' exists at job output")

        output=utils.run_command("cat %s/std.out"%(utils.get_job_output_dir()))

        if output.find("file1.txt")!=-1:
             utils.log_info("Check OK, file 'file1.txt' found at job output")
        else:
             utils.log_info("ERROR: Unable to find file 'file1.txt' at job output")
             raise GeneralError("Check job ouput","Unable to find file 'file1.txt' at job output")
                
   else:
        utils.log_info("ERROR: Job finishes with status: %s cannot retrieve output"%(status))
        raise GeneralError("Check final job status","Job finishes with status: %s cannot retrieve output"%(status))
        
   utils.log_info("TEST CASE PASS.")

  

def isbbaseuri_test(utils,target_ce):

    set_ISBBase(utils,utils.get_jdl_file())

    if utils.EXTERNAL_REQUIREMENTS==0:
        utils.set_requirements("%s"%utils.DEFAULTREQ)
    else:
        utils.set_requirements("%s && %s"%(target_ce,utils.DEFAULTREQ))

    utils.log_info("Submit job")

    JOBID=utils.run_command("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Wait until job finishes")

    utils.wait_until_job_finishes(JOBID)

    utils.log_info("Check job's output")

    status=utils.get_job_status(JOBID)

    if status.find("Done") != -1 :

          utils.remove(utils.get_tmp_file())

          utils.log_info("Retrieve the output")

          utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(), JOBID, utils.get_tmp_file()))

          utils.log_info("Check if the output files are correctly retrieved")

          if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
                utils.log_info("Output files are correctly retrieved")
          else:
                utils.log_info("ERROR: Output files are not correctly retrieved")
                raise GeneralError("Check if output files are correctly retrieved","Output files are not correctly retrieved")

          utils.log_info("Check for test1.txt file in std.out")

          output=utils.run_command("cat %s/std.out"%(utils.get_job_output_dir()))

          if output.find("test1.txt")!=-1:
                utils.log_info("test1.txt found in std.out")
          else:
                utils.log_info("ERROR: Unable to find file 'test1.txt' in std.out")
                raise GeneralError("Check for file test1.txt in std.out","Unable to find file 'test1.txt' in std.out")

    else:
          utils.log_info("ERROR: Job finishes with status: %s cannot retrieve output"%(status))
          raise GeneralError("Check job's final status","Job finishes with status: %s cannot retrieve output"%(status))


   
def osbbasedesturi_test(utils,target_ce,ssh):    
   
   SSH_utils.execute_remote_cmd(utils,ssh,"rm -f /tmp/%s/osbbase/*"%(utils.ID))

   set_OSBBaseDest(utils,utils.get_jdl_file())

   if utils.EXTERNAL_REQUIREMENTS==0:
        utils.set_requirements("%s"%utils.DEFAULTREQ)
   else:
        utils.set_requirements("%s && %s"%(target_ce,utils.DEFAULTREQ))

   utils.log_info("Submit job")

   JOBID=utils.run_command("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(), utils.get_jdl_file()))

   utils.log_info("Wait until job finishes")

   utils.wait_until_job_finishes(JOBID)

   utils.log_info("Check job's output")

   status=utils.get_job_status(JOBID)

   if status.find("Done") != -1 :

         utils.remove(utils.get_tmp_file())

         utils.log_info("Retrieve the output")

         utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID, utils.get_tmp_file()))

         utils.log_info("Check UI for output files")

         if len(os.listdir(utils.get_job_output_dir()))==0:
              utils.log_info("Output files have not been transferred to UI as expected")
         else:
              utils.log_info("ERROR: Output files have been transferred to UI")
              raise GeneralError("Check if output files have been transferred to UI","Output files have been transferred to UI")

         utils.log_info("Check if output files have been transferred to remote host %s"%(utils.OSB_DEST_HOSTNAME))
              
         files=SSH_utils.execute_remote_cmd(utils,ssh,"ls /tmp/%s/osbbase/"%(utils.ID)).split(" ")

         files = map(lambda s: s.strip(), files)

         expected=['std.out','std.err']

         if len(files)!=len(expected):
               utils.log_info("ERROR: Wrong number of output files. Find %s while expected %s"%(len(files),len(expected)))
               raise GeneralError("Check number of ouput files","Wrong number of output files. Find %s while expected %s"%(len(files),len(expected)))
                
         if len(set(files)&set(expected))!=len(expected):
               utils.log_info("ERROR: Unable to find all the expected output files. Find: %s , expected : %s"%(' , '.join(files),' , '.join(expected)))
               raise GeneralError("Check output files","Unable to find all the expected output files. Find: %s , expected : %s"%(' , '.join(files),' , '.join(expected)))


         utils.log_info("Check content of std.out file")

         output=SSH_utils.execute_remote_cmd(utils,ssh,"cat /tmp/%s/osbbase/std.out"%(utils.ID))

         values=[JOBID,'std.out','std.err','test.sh']

         for value in values:
              if output.find(value)!=-1:
                   utils.log_info("Find: %s"%(value))
              else:
                   utils.log_info("ERROR: Unable to find '%s' in std.out"%(value))
                   raise GeneralError("Check content of std.out file","Unable to find '%s' in std.out"%(value))

   else:
         utils.log_info("ERROR: Job finishes with status: %s cannot retrieve output"%(status))
         raise GeneralError("Check job status","Job finishes with status: %s cannot retrieve output"%(status))



def osbdesturi_test(utils,target_ce,ssh):

    SSH_utils.execute_remote_cmd(utils,ssh,"rm -f /tmp/%s/osbdest/*"%(utils.ID))

    set_OSBDest(utils,utils.get_jdl_file())

    if utils.EXTERNAL_REQUIREMENTS==0:
        utils.set_requirements("%s"%utils.DEFAULTREQ)
    else:
        utils.set_requirements("%s && %s"%(target_ce,utils.DEFAULTREQ))

    utils.log_info("Submit job")

    JOBID=utils.run_command("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Wait until job finishes")

    utils.wait_until_job_finishes(JOBID)

    utils.log_info("Check job's output")

    status=utils.get_job_status(JOBID)

    if status.find("Done") != -1 :

          utils.remove(utils.get_tmp_file())

          utils.log_info("Retrieve the output")

          utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID, utils.get_tmp_file()))

          utils.log_info("Check UI for std.err file")

          if len(os.listdir(utils.get_job_output_dir()))==1:

                utils.log_info("Find 1 file as expected , check its name")

                if os.path.isfile("%s/std.err"%(utils.get_job_output_dir())):
                      utils.log_info("OK for std.err file")
                else:
                      utils.log_info("ERROR: One file transferred to UI but not the expected (std.err)")
                      raise GeneralError("","One file has been transferred to UI but not the expected (std.err)")

          else:
               utils.log_info("ERROR: Wrong number of files have been transferred to UI")
               raise GeneralError("Check UI for std.err file","Wrong number of files have been transferred to UI")


          utils.log_info("Check if file std.out has been transferred to remote host %s"%(utils.OSB_DEST_HOSTNAME))

          files=SSH_utils.execute_remote_cmd(utils,ssh,"ls /tmp/%s/osbdest/"%(utils.ID)).split(" ")

          files = map(lambda s: s.strip(), files)

          expected=['std.out']

          if len(files)!=len(expected):
                utils.log_info("ERROR: Wrong number of output files. Find %s while expected only %s"%(len(files),len(expected)))
                raise GeneralError("Check number of ouput files","Wrong number of output files. Find %s while expected only %s"%(len(files),len(expected)))


          if len(set(files)&set(expected))!=len(expected):
                utils.log_info("ERROR: Unable to find all the expected output files. Find: %s , expected : %s"%(','.join(files),','.join(expected)))
                raise GeneralError("Check output files","Unable to find all the expected output files. Find: %s , expected : %s"%(','.join(files),','.join(expected)))


          utils.log_info("Check content of std.out file")

          output=SSH_utils.execute_remote_cmd(utils,ssh,"cat /tmp/%s/osbdest/std.out"%(utils.ID))

          values=[JOBID,'std.out','std.err','test.sh']
          
          for value in values:
              if output.find(value)!=-1:
                   utils.log_info("Find: %s"%(value))
              else:
                   utils.log_info("ERROR: Unable to find '%s' in std.out"%(value))
                   raise GeneralError("Check content of std.out file","Unable to find '%s' in std.out"%(value))

    else:
         utils.log_info("ERROR: Job finishes with status: %s cannot retrieve output"%(status))
         raise GeneralError("Check job status","Job finishes with status: %s cannot retrieve output"%(status))



def test_FuzzyRank_attribute(utils):
    
    utils.log_info("Submit job")

    JOBID=utils.run_command("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
            
    utils.log_info("Wait until finished")

    utils.wait_until_job_finishes(JOBID)

    utils.log_info("Try to get the output of the normal job")

    status=utils.get_job_status(JOBID)

    if status.find("Done") != -1 :

         utils.remove(utils.get_tmp_file())

         utils.log_info("Retrieve the output")

         utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

         utils.log_info("Check if the output files are correctly retrieved")

         if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
               utils.log_info("Output files are correctly retrieved")
               utils.log_info("Clean output directory")
               utils.run_command("rm -rf %s/*"%(utils.get_job_output_dir()))
         else:
               utils.log_info("ERROR: Output files are not correctly retrieved")
               raise GeneralError("Check if the output files are correctly retrieved","Output files are correctly retrieved")
    else:
         utils.log_info("Job finishes with status: %s cannot retrieve output"%(status))
         raise GeneralError("Check job status","Job finishes with status: %s cannot retrieve output"%(status))
            
        

def test_UserTags_attribute(utils):


    utils.log_info("Submit job")

    JOBID=utils.run_command("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    status=utils.get_job_status(JOBID)

    while status.find("Ready")!=-1 or status.find("Waiting")!=-1:
          utils.log_info("Wait 10 secs until status changed from Waiting or Ready")
          time.sleep(10)
          status=utils.get_job_status(JOBID)

    utils.log_info("Check logging info for defined user tag")

    output=utils.run_command("glite-wms-job-logging-info -v 2 --event UserTag %s"%(JOBID))

    if output.find("WMSTestsuiteTag")!=-1 and output.find("WMS_Testing")!=-1:
          utils.log_info("Find defined user tag")
    else:
          utils.log_info("ERROR: Unable to find defined user tag")
          raise GeneralError("Check logging info for defined user tag","Unable to find defined user tag")

    utils.log_info("Wait until finished")

    utils.wait_until_job_finishes(JOBID)

    utils.log_info("Try to get the output of the normal job")

    status=utils.get_job_status(JOBID)

    if status.find("Done") != -1 :

         utils.remove(utils.get_tmp_file())

         utils.log_info("Retrieve the output")

         utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

         utils.log_info("Check if the output files are correctly retrieved")

         if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
               utils.log_info("Output files are correctly retrieved")
               utils.log_info("Clean output directory")
               utils.run_command("rm -rf %s/*"%(utils.get_job_output_dir()))
         else:
               utils.log_info("ERROR: Output files are not correctly retrieved")
               raise GeneralError("Check if the output files are correctly retrieved","Output files are correctly retrieved")
    else:
         utils.log_info("Job finishes with status: %s cannot retrieve output"%(status))
         raise GeneralError("Check job status","Job finishes with status: %s cannot retrieve output"%(status))


def create_configuration_with_invalid_LBAddress(utils):

    utils.log_info("Create a temporary configuration file with invalid LB Address")

    FILE=open("%s/wms.conf"%(utils.get_tmp_dir()))
    lines=FILE.readlines()
    FILE.close()

    for line in lines:
        if line.find("LBAddresses")!=-1:
           lines[lines.index(line)]="LBAddresses= {\"unknown.hostname.infn.it\"};"

    FILE=open("%s/invalid_wms.conf"%(utils.get_tmp_dir()),"w")
    FILE.write("\n".join(lines))
    FILE.close()


def test_LBAddresses_attribute(utils):

    utils.log_info("Submit job using configuration with invalid LB address")

    JOBID=utils.run_command("glite-wms-job-submit %s -c %s/invalid_wms.conf --nomsg %s"%(utils.get_delegation_options(),utils.get_tmp_dir(),utils.get_jdl_file()))

    utils.log_info("Check returned job id for LB address from jdl file")

    if JOBID.find(utils.LB)==-1:
          utils.log_info("ERROR: Returned job id does not contain the LB address from jdl file")
          raise GeneralError("Check returned job id for LB address from jdl file","Returned job id does not contain the LB address from jdl file")
    else:

          utils.log_info("Returned job id contains the LB address from jdl file")

          utils.log_info("Wait until finished")

          utils.wait_until_job_finishes(JOBID)

          utils.log_info("Try to get the output of the normal job")

          status=utils.get_job_status(JOBID)

          if status.find("Done") != -1 :

                utils.remove(utils.get_tmp_file())

                utils.log_info("Retrieve the output")

                utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

                utils.log_info("Check if the output files are correctly retrieved")

                if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
                      utils.log_info("Output files are correctly retrieved")
                      utils.log_info("Clean output directory")
                      utils.run_command("rm -rf %s/*"%(utils.get_job_output_dir()))
                else:
                      utils.log_info("ERROR: Output files are not correctly retrieved")
                      raise GeneralError("Check if the output files are correctly retrieved","Output files are not correctly retrieved")                     

          else:
                utils.log_info("ERROR: Job finishes with status: %s cannot retrieve output"%(status))
                raise GeneralError("Try to get the output of the normal job","Job finishes with status: %s cannot retrieve output"%(status))                     



def test_environment_attribute(utils):

    utils.log_info("Submit job ")

    JOBID=utils.run_command("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Wait until finished")

    utils.wait_until_job_finishes(JOBID)

    utils.log_info("Try to get job's output")

    status=utils.get_job_status(JOBID)

    if status.find("Done") != -1 :

           utils.remove(utils.get_tmp_file())

           utils.log_info("Retrieve the output")

           utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

           utils.log_info("Check if the output files are correctly retrieved")

           if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :

                  utils.log_info("Output files are correctly retrieved")

                  utils.log_info("Check the output file for the expected value from the defined environment variable")

                  content=utils.run_command("cat %s/std.out"%(utils.get_job_output_dir()))

                  if content.find("WMS-Service")!=-1:
                        utils.log_info("Find the expected value from the defined environment variable")
                  else:
                        utils.log_info("ERROR: Unable to find the expected value from the defined environment variable")
                        raise GeneralError("Check the output file for the expected value from the defined environment variable","Unable to find the expected value from the defined environment variable")

                  utils.log_info("Clear output directory")
                  utils.run_command("rm -rf %s/*"%(utils.get_job_output_dir()))

           else:
                  utils.log_info("ERROR: Output files are not correctly retrieved")
                  raise GeneralError("Check if the output files are correctly retrieved","Output files are not correctly retrieved")
                  
    else:
           utils.log_info("ERROR: Job finishes with status: %s cannot retrieve output"%(status))
           raise GeneralError("Try to get job's output","Job finishes with status: %s cannot retrieve output"%(status))


 
def test_perusalFileEnable_attribute(utils,target):

    utils.log_info("Create a jdl file and disable file perusal operation")

    utils.set_isb_jdl(utils.get_jdl_file())

    if utils.EXTERNAL_REQUIREMENTS==0:
          utils.set_requirements("%s"%utils.DEFAULTREQ)
    else:
          utils.set_requirements("%s && %s"%(target,utils.DEFAULTREQ))

    utils.add_jdl_general_attribute("PerusalFileEnable","false")

    utils.log_info("Submit job")

    JOBID=utils.run_command("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Try to enable files perusal for the submitted job")

    output=utils.run_command("glite-wms-job-perusal --set --filename out.txt -f std.out %s"%(JOBID),1)

    utils.log_info("Operation failed as expected")

    utils.log_info("Check failed reason")

    if output.find("The Operation is not allowed: Perusal not enabled for this job")==-1:
          utils.log_info("ERROR: The reason the job failed is not the expected")
          raise GeneralError("Check failed reason","The reason the job failed is not the expected")
    else:
          utils.log_info("The reason the job failed is the expected. (The Operation is not allowed: Perusal not enabled for this job)")

    utils.log_info("Cancel submitted job")

    utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))

    utils.log_info("Create a jdl file and enable file perusal operation")

    utils.set_perusal_jdl(utils.get_jdl_file())

    utils.log_info("Submit job")

    JOBID=utils.run_command("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Try to enable files perusal for the submitted job")

    utils.run_command("glite-wms-job-perusal --set --filename out.txt -f std.out %s"%(JOBID))

    utils.log_info("Operation executed successfully as expected")

    utils.log_info("Cancel submitted job")

    utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))

    utils.log_info("TEST PASS")



def test_perusalTimeInterval_attribute(utils,target):

    utils.log_info("Create jdl file")

    set_jdl_for_perusalTimeInterval_test(utils,utils.get_jdl_file())

    if utils.EXTERNAL_REQUIREMENTS==0:
         utils.set_requirements("%s"%utils.DEFAULTREQ)
    else:
         utils.set_requirements("%s && %s"%(target,utils.DEFAULTREQ))

    utils.add_jdl_general_attribute("PerusalTimeInterval","1300")

    utils.log_info("Submit job")

    JOBID=utils.run_command("glite-wms-job-submit %s --nomsg -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Enable files perusal for the submitted job")

    utils.run_command("glite-wms-job-perusal --set --filename out.txt -f std.out %s"%(JOBID))

    utils.log_info("Wait until job's state is Running")

    status=utils.get_job_status(JOBID)

    while status.find("Running")==-1 and utils.job_is_finished(JOBID)==0:
         time.sleep(30)
         status=utils.get_job_status(JOBID)

    time_before_first_try=int(time.time())

    utils.log_info("Wait for 1340 secs")

    time.sleep(1340)

    utils.run_command("glite-wms-job-perusal --get -f out.txt --dir %s %s"%(utils.get_job_output_dir(),JOBID))
        
    utils.log_info("Check if some chunkes have been retrieved")

    filespec="out.txt-*"

    first_try_chunk=glob.glob(os.path.join(utils.get_job_output_dir(),filespec))

    if len(first_try_chunk)>0:
         utils.log_info("These chunks have been retrieved: %s"%(first_try_chunk))
    else:
         utils.log_info("ERROR: No chunks have been retrieved")
         raise GeneralError("glite-wms-job-perusal --get","No chunks have been retrieved.")

    first_try_size=os.stat(first_try_chunk[0]).st_size

    first_chunk_ctime=os.stat(first_try_chunk[0]).st_ctime

    utils.log_info("Wait for another 1340 secs")

    time.sleep(1340)

    utils.run_command("glite-wms-job-perusal --get -f out.txt --dir %s %s"%(utils.get_job_output_dir(),JOBID))

    utils.log_info("Check if some chunks have been retrieved")

    second_try_chunk=glob.glob(os.path.join(utils.get_job_output_dir(),filespec))

    if len(second_try_chunk)>len(first_try_chunk):
         utils.log_info("These chunks have been retrieved: %s"%(second_try_chunk))
    else:
         utils.log_info("ERROR: No chunks have been retrieved")
         raise GeneralError("glite-wms-job-perusal --get","No chunks have been retrieved.")

    second_try_chunk.remove(first_try_chunk[0])

    second_try_size=os.stat(second_try_chunk[0]).st_size

    second_chunk_ctime=os.stat(second_try_chunk[0]).st_ctime

    utils.log_info("Check the size for the retrieved chunks")

    if second_try_size <= first_try_size :
         utils.log_info("ERROR: The size of the second chunk is not bigger than the size of the first chunk as expected. First chunk size:%s  Second chunk size: %s"%(first_try_size,second_try_size))
         raise GeneralError("Check the size for the retrieved chunks","The size of the second chunk is not bigger than the size of the first chunk as expected. First chunk size:%s  Second chunk size: %s"%(first_try_size,second_try_size))

    else:
         utils.log_info("The size of the second chunk is bigger than its of the first chunk as expected")

    utils.log_info("Check the time difference between the retrieved chunks")

    utils.log_info("Time before first try: %s"%(time_before_first_try))
    utils.log_info("Creation time for the first chunk: %s"%(first_chunk_ctime))
    utils.log_info("Creation time for the second chunk: %s"%(second_chunk_ctime))

    if int(time_before_first_try)-int(first_chunk_ctime) < 1300 or int(second_chunk_ctime)-int(first_chunk_ctime) < 1300:
         utils.log_info("ERROR: Time difference between chunks is shorter than the PerusalTimeInterval value (1300 secs)")
         raise GeneralError("Check the time difference between the retrieved chunks","Time difference between chunks is shorter than the PerusalTimeInterval value (1300 secs)")
    else:
         utils.log_info("Time difference between chunks is the expected")
                             
    utils.log_info("TEST PASS")

            
