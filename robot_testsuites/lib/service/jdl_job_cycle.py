
from Exceptions import *

import commands
import os.path
import os
import SSH_utils


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

   utils.set_destination_ce(utils.get_jdl_file(),target)

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

    utils.set_destination_ce(utils.get_jdl_file(),target_ce)

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

   utils.set_destination_ce(utils.get_jdl_file(),target_ce)

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

    utils.set_destination_ce(utils.get_jdl_file(),target_ce)

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


