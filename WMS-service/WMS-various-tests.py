#! /usr/bin/python

import sys
import signal
import traceback
import commands
import os.path
import time

from Exceptions import *

import Test_utils
import SSH_utils
import Job_utils


def set_huge_jdl(utils,filename):

    utils.info("Define a jdl with big output file")

    FILE=open(filename,"w")

    FILE.write("Executable = \"/bin/dd\";\n")
    FILE.write("Arguments = \"if=/dev/zero of=./huge bs=1024 count=100000\";\n")
    FILE.write("InputSandbox = {};\n")
    FILE.write("OutputSandbox = {\"huge\"};\n")
    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


    
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

        utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))



def test1(utils, title):

    names,ces=utils.get_target_ces()

    fails=0

    if len(names)==0:
        names.append("Default Test , Submit to CREAM")
        ces.append("")

    for i in range(len(names)):

        utils.show_progress("%s - %s"%(title,names[i]))

        utils.info("%s - %s"%(title,names[i]))

        try:

            utils.info("Set MaxOuputSandboxSize=50M; to glite_wms.conf at WMS")

            ssh=SSH_utils.open_ssh(utils.get_WMS(),utils.WMS_USERNAME,utils.WMS_PASSWORD)

            SSH_utils.change_remote_file(utils,ssh,"/etc/glite-wms/glite_wms.conf", ['MaxOutputSandboxSize'],['*'],['50M'])

            utils.info("Restart workload manager glite-wms-wm")

            SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

            utils.info("Submit the job to CE and wait to finish")

            set_huge_jdl(utils,utils.get_jdl_file())

            if len(ces[i])>0:
                 utils.set_requirements("%s && %s"%(ces[i],utils.DEFAULTREQ))
            else:
                 utils.set_requirements("%s"%utils.DEFAULTREQ)

            utils.run_command_continue_on_error("rm -rf %s/*"%(utils.get_job_output_dir()))

            res=Job_utils.submit_only_normal_job(utils,ces[i])

            JOBID=res[1]

            utils.info("Wait until job finished")

            utils.wait_until_job_finishes(JOBID)

            utils.info("Check logging info")

            result=utils.run_command_continue_on_error("glite-wms-job-logging-info -v 3 --event UserTag %s"%(JOBID))

            if result.find("OSB quota exceeded for") == -1:
                utils.error("Not found message 'OSB quota exceeded for' at UserTag")
                raise GeneralError("Check UserTag event","Not found message 'OSB quota exceeded for' at UserTag")
            else:
                utils.info("Find message 'OSB quota exceeded for' at UserTag event")

            if result.find("Truncated last 52428800 bytes for file") == -1:
                utils.error("Not found message 'Truncated last 52428800 bytes for file")
                raise GeneralError("Check UserTag event","Not found message 'Truncated last 52428800 bytes for file' at UserTag")
            else:
                utils.info("Find message 'Truncated last 52428800 bytes for file' at UserTag event")

            utils.info("Get job output")

            utils.job_status(JOBID)

            if utils.get_job_status().find("Done") != -1 :

                utils.remove(utils.get_tmp_file())

                utils.info("Retrieve the output")

                utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

                if os.path.isfile("%s/huge.tail"%(utils.get_job_output_dir())) :
                    utils.info("Output file (huge.tail) is correctly retrieved")
                else:
                    utils.error("Output file (huge.tail) is not correctly retrieved")
                    raise GeneralError("Check output file","Output file (huge.tail) is not correctly retrieved")

                utils.info("Check the size of the output file")

                output=utils.run_command_continue_on_error("ls -l %s/"%(utils.get_job_output_dir()))

                if output.find("52428800")!=-1:
                   utils.info("huge.tail size is 52428800 bytes as expected")
                else:
                   utils.error("huge.tail size is not 52428800 bytes as expected. We get %s"%(ouput))
                   raise GeneralError("Check the size of the ouput file","huge.tail size is not 52428800 bytes as expected")

            else:
                utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
                raise GeneralError("Check final job status","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))


            SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
            SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
            SSH_utils.close_ssh(ssh)


        except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
            SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
            SSH_utils.close_ssh(ssh)
            fails=fails+1


    return fails
    


def test2(utils, title):

    utils.show_progress(title)
    utils.info(title)

    try:

        ssh=SSH_utils.open_ssh(utils.get_WMS(),utils.WMS_USERNAME,utils.WMS_PASSWORD)

        set_test2_jdl(utils,utils.get_jdl_file())

        utils.info("Submit a job")

        JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Set WMS in draining mode")

        SSH_utils.execute_remote_cmd(ssh,"touch /var/.drain")

        utils.info("Try to submit jobs")

        output=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()),1)

        utils.info("Check error message")

        if output.find("Unable to find any endpoint where to perform service request")==-1:
          utils.error("Failed reason is not 'Unable to find any endpoint where to perform service request'")
          raise GeneralError("Check error message","Failed reason is not 'Unable to find any endpoint where to perform service request'")
        else:
          utils.info("Failed reason is 'Unable to find any endpoint where to perform service request' as expected")

        utils.info("Try list-match")

        output=utils.run_command_continue_on_error("glite-wms-job-list-match %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()),1)

        if output.find("Unable to find any endpoint where to perform service request")==-1:
          utils.error("Failed reason is not 'Unable to find any endpoint where to perform service request'")
          raise GeneralError("Check error message","Failed reason is not 'Unable to find any endpoint where to perform service request'")
        else:
          utils.info("Failed reason is 'Unable to find any endpoint where to perform service request' as expected")
        
        utils.info("Check status of previously submitted job")

        utils.wait_until_job_finishes(JOBID)

        utils.info("Get job output")

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

        else:
            utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            raise GeneralError("Check final job status","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))


        utils.info("Unset WMS from draining mode")
        SSH_utils.execute_remote_cmd(ssh,"rm -f /var/.drain")
        SSH_utils.close_ssh(ssh)

        utils.info("TEST PASS")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        utils.info("Unset WMS from draining mode")
        SSH_utils.execute_remote_cmd(ssh,"rm -f /var/.drain")
        SSH_utils.close_ssh(ssh)
        return 1

    return 0


def test3(utils, title):

    utils.show_progress(title)
    utils.info(title)

    try:

        ssh=SSH_utils.open_ssh(utils.get_WMS(),utils.WMS_USERNAME,utils.WMS_PASSWORD)

        utils.info("Get last access date for script /opt/lcg/sbin/grid_monitor.sh before submission")

        output=SSH_utils.execute_remote_cmd(ssh, "ls -lu --time-style=full-iso `locate grid_mon`")

        before_access=''

        for line in output.split("\n"):
            if line.find("/opt/lcg/sbin/grid_monitor.sh")!=-1 and line.find("/usr/sbin/grid_monitor.sh")==-1:
                before_access=line

        if len(before_access)==0:
            utils.error("Unable to find script /opt/lcg/sbin/grid_monitor.sh")
            raise GeneralError("Check if script /opt/lcg/sbin/grid_monitor.sh has been used during the job submission","Unable to find script /opt/lcg/sbin/grid_monitor.sh")

        utils.info("Wait 10 secs")
        time.sleep(10)

        utils.info("Submit a job to GRAM CE")
        utils.set_jdl(utils.get_jdl_file())
        utils.set_destination_ce(utils.get_jdl_file(),"2119/jobmanager")

        JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.job_status(JOBID)

        while utils.get_job_status().find("Ready")!=-1 or utils.get_job_status().find("Waiting")!=-1:
            utils.info("Wait 30 secs")
            time.sleep(30)
            utils.job_status(JOBID)

        utils.info("Get last access date for script /opt/lcg/sbin/grid_monitor.sh after submission")

        output=SSH_utils.execute_remote_cmd(ssh, "ls -lu  --time-style=full-iso `locate grid_mon`")

        SSH_utils.close_ssh(ssh)

        after_access=''

        for line in output.split("\n"):
            if line.find("/opt/lcg/sbin/grid_monitor.sh")!=-1 and line.find("/usr/sbin/grid_monitor.sh")==-1:
                after_access=line

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

        utils.info("Check if script /opt/lcg/sbin/grid_monitor.sh has been used during the job submission")

        if after>before:
            utils.info("Check OK, script /opt/lcg/sbin/grid_monitor.sh has been used during the job submission")
        else:
            utils.error("Test failed, script /opt/lcg/sbin/grid_monitor.sh hasn't been used during the job submission")
            utils.error("Access details before submission: %s %s"%(before_date,before_time))
            utils.error("Access details after submission: %s %s"%(after_date,after_time))
            raise GeneralError("Check if script /opt/lcg/sbin/grid_monitor.sh has been used during the job submission","Test failed, script /opt/lcg/sbin/grid_monitor.sh hasn't been used during the job submission")

        utils.info("TEST PASS")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        SSH_utils.close_ssh(ssh)
        return 1

    return 0


    
def main():

    fails=[]

    utils = Test_utils.Test_utils(sys.argv[0],"WMS Various Tests")

    tests=["Test 1: Test OSB truncation"]
    tests.append("Test 2: Test drain operation")
    tests.append("Test 3: Test the usage of grid_monitor.sh script ")

    utils.prepare(sys.argv[1:],tests)

    if utils.WMS_USERNAME=='' or utils.WMS_PASSWORD=='':
       utils.warn("Please set the required variables WMS_USERNAME , WMS_PASSWORD in test's configuration file")
       utils.show_progress("Please set the required variables WMS_USERNAME , WMS_PASSWORD in test's configuration file")
       sys.exit(0)

    utils.info("WMS Various Tests")

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
