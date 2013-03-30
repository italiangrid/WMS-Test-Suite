import commands
import os.path
import SSH_utils
import time

from Exceptions import *



def set_huge_jdl(utils,filename):

    utils.log_info("Define a jdl with big output file")

    FILE=open(filename,"w")

    FILE.write("Executable = \"/bin/dd\";\n")
    FILE.write("Arguments = \"if=/dev/zero of=./huge bs=1024 count=100000\";\n")
    FILE.write("InputSandbox = {};\n")
    FILE.write("OutputSandbox = {\"huge\"};\n")
    FILE.close()

    utils.log_info("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))),"DEBUG")


    
def set_test2_jdl(utils,filename):

      FILE = open("%s/test.sh"%(utils.get_tmp_dir()),"w")
      FILE.write("#!/bin/sh\n")
      FILE.write("echo \"##########################\"\n")
      FILE.write("echo \"This is the executable\"\n")
      FILE.write("echo \"Start running at `date +%H:%M:%S`\"\n")
      FILE.write("echo \"Sleep 300 secs\"\n")
      FILE.write("sleep 300\n")
      FILE.write("echo \"Finish running at `date +%H:%M:%S`\"\n")
      FILE.write("echo \"##########################\"\n")
      FILE.close()

      FILE = open(filename,"w")

      FILE.write("Executable = \"/bin/sh\";\n")
      FILE.write("Arguments = \"test.sh\";\n")
      FILE.write("StdOutput = \"std.out\";\n")
      FILE.write("StdError = \"std.err\";\n")
      FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n")
      FILE.write("ShallowRetryCount = 2;\n")
      FILE.write("InputSandbox = \"%s/test.sh\";\n"%(utils.get_tmp_dir()))

      FILE.close()

      utils.log_info("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))),"DEBUG")



def set_drain(utils,ssh):

     utils.log_info("Set WMS in draining mode")

     SSH_utils.execute_remote_cmd(utils,ssh,"touch /var/.drain")


def unset_drain(utils,ssh):

     utils.log_info("Unset WMS from draining mode")

     SSH_utils.execute_remote_cmd(utils,ssh,"rm -f /var/.drain")


def check_message(utils,ssh,message):   

    if message.find("Unable to find any endpoint where to perform service request")==-1:
          utils.log_info("ERROR: Failed reason is not 'Unable to find any endpoint where to perform service request'")
          raise GeneralError("Check error message","Failed reason is not 'Unable to find any endpoint where to perform service request'")
    else:
          utils.log_info("Failed reason is 'Unable to find any endpoint where to perform service request' as expected")



def check_job_output(utils,jobid):

    utils.log_info("Get job output")

    status=utils.get_job_status(jobid)   

    if status.find("Done") != -1 :

         utils.remove(utils.get_tmp_file())

         utils.log_info("Retrieve the output")

         utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))

         utils.log_info("Check if the output files are correctly retrieved")

         if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
               utils.log_info("Output files are correctly retrieved")
         else:
               utils.log_info("ERROR: Output files are not correctly retrieved")
               raise GeneralError("Check output files","Output files are not correctly retrieved")

    else:
          utils.log_info("ERROR: Job finishes with status: %s cannot retrieve output"%(status))
          raise GeneralError("Check final job status","Job finishes with status: %s cannot retrieve output"%(status))


def restore_configuration(utils,ssh):

    SSH_utils.execute_remote_cmd(utils,ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
    SSH_utils.execute_remote_cmd(utils,ssh,"/etc/init.d/glite-wms-wm restart")
      

def set_MaxOSB(utils,ssh):

    SSH_utils.change_remote_file(utils,ssh,"/etc/glite-wms/glite_wms.conf",["MaxOutputSandboxSize"],["*"],["50M"])


def check_osb_truncation_output(utils,jobid):

    status=utils.get_job_status(jobid)

    if status.find("Done") != -1 :

         utils.remove(utils.get_tmp_file())

         utils.log_info("Retrieve the output")

         utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))

         if os.path.isfile("%s/huge.tail"%(utils.get_job_output_dir())) :
              utils.log_info("Output file (huge.tail) is correctly retrieved")
         else:
              utils.log_info("ERROR: Output file (huge.tail) is not correctly retrieved")
              raise GeneralError("Check output file","Output file (huge.tail) is not correctly retrieved")

         utils.log_info("Check the size of the output file")

         output=utils.run_command("ls -l %s/"%(utils.get_job_output_dir()))

         if output.find("52428800")!=-1:
              utils.log_info("huge.tail size is 52428800 bytes as expected")
         else:
              utils.log_info("ERROR: huge.tail size is not 52428800 bytes as expected. We get %s"%(ouput))
              raise GeneralError("Check the size of the ouput file","huge.tail size is not 52428800 bytes as expected")

    else:
          utils.log_info("ERROR: Job finishes with status: %s cannot retrieve output"%(status))
          raise GeneralError("Check final job status","Job finishes with status: %s cannot retrieve output"%(status))



def script_access_time(data):

   access_time=''

   for line in data.split("\n"):
       if line.find("/opt/lcg/sbin/grid_monitor.sh")!=-1 and line.find("/usr/sbin/grid_monitor.sh")==-1:
          access_time=line
   
   if len(access_time)==0:
       utils.log_info("ERROR: Unable to find script /opt/lcg/sbin/grid_monitor.sh")
       raise GeneralError("Check if script /opt/lcg/sbin/grid_monitor.sh has been used during the job submission","Unable to find script /opt/lcg/sbin/grid_monitor.sh")

   return access_time


def wait_before_check_script(utils,jobid):

   while utils.get_job_status(jobid).find("Ready")!=-1 or utils.get_job_status(jobid).find("Waiting")!=-1:
        utils.log_info("Wait 30 secs")
        time.sleep(30)


def compare_access_time(utils,before_access,after_access):

   for value in before_access.split(" "):
       if value.find(":")!=-1:
           before_time=value.split(".")[0]

       if value.find("-")!=-1 and value.find("->")==-1:
           before_date=value

   for value in after_access.split(" "):
       if value.find(":")!=-1:
           after_time=value.split(".")[0]

       if value.find("-")!=-1 and value.find("->")==-1:
           after_date=value

   before=time.mktime(time.strptime("%s %s"%(before_date,before_time),"%Y-%m-%d %H:%M:%S"))
   after=time.mktime(time.strptime("%s %s"%(after_date,after_time),"%Y-%m-%d %H:%M:%S"))

   utils.log_info("Check if script /opt/lcg/sbin/grid_monitor.sh has been used during the job submission")

   if after>before:
         utils.log_info("Test OK, script /opt/lcg/sbin/grid_monitor.sh has been used during the job submission")
   else:
         utils.log_info("ERROR: Test failed, script /opt/lcg/sbin/grid_monitor.sh hasn't been used during the job submission")
         utils.log_info("ERROR: Access details before submission: %s %s"%(before_date,before_time))
         utils.log_info("ERRPR: Access details after submission: %s %s"%(after_date,after_time))
         raise GeneralError("Check if script /opt/lcg/sbin/grid_monitor.sh has been used during the job submission","Test failed, script /opt/lcg/sbin/grid_monitor.sh hasn't been used during the job submission")



