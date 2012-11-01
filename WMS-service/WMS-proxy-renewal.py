#! /usr/bin/python

import sys
import signal
import commands
import traceback
import os.path

from Exceptions import *

import Test_utils


def test1(utils, title):

    names,ces=utils.get_target_ces()

    fails=0

    if len(names)==0:
        names.append("Default Test")
        ces.append("")

    for i in range(len(names)):

        utils.show_progress("%s - %s"%(title,names[i]))

        try:

            utils.info("%s - %s"%(title,names[i]))

            utils.set_long_jdl(utils.get_jdl_file())
            utils.add_jdl_attribute("StdOutput", "std.out")
            utils.add_jdl_attribute("StdError", "std.err")
            utils.add_jdl_general_attribute("OutputSandbox","{\"std.out\",\"std.err\"}")

            if len(ces[i])>0:
                utils.set_requirements("%s && %s"%(ces[i],utils.DEFAULTREQ))
            else:
                utils.set_requirements("%s"%utils.DEFAULTREQ)

            utils.add_jdl_attribute("MyProxyServer", utils.get_MYPROXY_SERVER())

            utils.info("Submit a job with a short proxy")
            utils.set_proxy(utils.get_PROXY(),"00:14")

            JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit --nomsg --config %s -a %s"%(utils.get_config_file(),utils.get_jdl_file()))

            utils.dbg ("Check if the job has been submitted with the right proxy")

            output=utils.run_command_continue_on_error ("glite-wms-job-info -p %s"%(JOBID))

            for line in output.splitlines():
                if line.split(":")[0].strip() == "Timeleft":
                    token=line.split(":")[1].strip()
                    if ( (token.split(" ")[1] == "hours") or
                       (int(token.split(" ")[0]) > 14 ) ):
                        utils.error("The proxy of the submitted job has not the expected duration")
                        raise GeneralError("Check proxy of the submitted job","Wrong duration")

            utils.dbg ("Wait until job finishes (more than 15 minutes)")

            # we now need a long proxy to check job status
            utils.set_proxy(utils.get_PROXY(),"12:00")

            utils.wait_until_job_finishes(JOBID)

            utils.job_status(JOBID)

            if utils.get_job_status().find('Aborted')!=-1:

                OUTPUT=commands.getstatusoutput("glite-wms-job-status %s"%(JOBID))

                if OUTPUT[1].find("the user proxy expired") != -1:
                    utils.error("TEST FAILS. Proxy expired")
                    raise GeneralError("Check failed reason","Proxy expired")

                else:
                    utils.error("TEST FAILS. Unexpected failed reason")
                    raise GeneralError("Check failed reason","Unexpected failed reason")

            utils.remove(utils.get_tmp_file())

            utils.info("Retrieve the output")

            utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

            utils.info("Check if the output files are correctly retrieved")

            if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
                utils.info("Output files are correctly retrieved")
            else:
                utils.error("Output files are not correctly retrieved")
                raise GeneralError("Check output files","Output files are not correctly retrieved")
                
            utils.info("TEST PASS")

        except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            fails=fails+1


    if fails==0:
        return 0
    else:
        return 1


def test2(utils, title):

    names,ces=utils.get_target_ces()

    fails=0

    if len(names)==0:
        names.append("Default Test")
        ces.append("")

    for i in range(len(names)):

        utils.show_progress("%s - %s"%(title,names[i]))

        try:

            utils.info("%s - %s"%(title,names[i]))

            utils.set_long_jdl(utils.get_jdl_file())

            if len(ces[i])>0:
                utils.set_requirements("%s && %s"%(ces[i],utils.DEFAULTREQ))
            else:
                utils.set_requirements("%s"%utils.DEFAULTREQ)

            utils.add_jdl_attribute("MyProxyServer", "")

            utils.info("Submit a job with a short proxy")
            utils.set_proxy(utils.get_PROXY(),"00:14")

            JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit --nomsg --config %s -a %s"%(utils.get_config_file(),utils.get_jdl_file()))

            utils.dbg ("Check if the job has been submitted with the right proxy")

            output=utils.run_command_continue_on_error ("glite-wms-job-info -p %s"%(JOBID))

            for line in output.splitlines():
                if line.split(":")[0].strip() == "Timeleft":
                    token=line.split(":")[1].strip()
                    if ( (token.split(" ")[1] == "hours") or
                       (int(token.split(" ")[0]) > 14 ) ):
                        utils.error("The proxy of the submitted job has not the expected duration")
                        raise GeneralError("Check proxy of the submitted job","Wrong duration")

            utils.dbg ("Wait until job finishes (more than 15 minutes)")

            # we now need a long proxy to check job status
            utils.set_proxy(utils.get_PROXY(),"12:00")

            utils.wait_until_job_finishes(JOBID)

            utils.job_status(JOBID)

            if utils.get_job_status().find('Aborted')!=-1 or utils.get_job_status().find('Done (Failed)')!=-1:

                OUTPUT=commands.getstatusoutput("glite-wms-job-status -v 2 %s | grep 'Failure reasons'"%(JOBID))

                if OUTPUT[1].find('expired')!=-1:
                    utils.info("TEST PASS")

                else:
                    utils.warn("Unexpected failed reason: %s"%(OUTPUT[1]))

            else:
                utils.error("TEST FAILS. Job not failed")
                raise GeneralError("Job finished with a unexpected status: %s."%(utils.get_job_status()),"Wrong job's final status")

        except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            fails=fails+1

    if fails==0:
        return 0
    else:
        return 1


def main():

    fails=[]

    tests=["Test 1: Test proxy renewal"]
    tests.append("Test 2: Test proxy renewal without setting MYPROXYSERVER")
    
    utils = Test_utils.Test_utils(sys.argv[0],"WMS test proxy renewal operation")

    utils.prepare(sys.argv[1:],tests)

    utils.info("WMS test proxy renewal operation")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    if utils.get_NOPROXY()==0 and utils.get_MYPROXY_SERVER():
    
        all_tests=utils.is_all_enabled()

        if all_tests==1 or utils.check_test_enabled(1)==1 :
            if test1(utils, tests[0]):
                fails.append(tests[0])
                
        if all_tests==1 or utils.check_test_enabled(2)==1 :
            if test2(utils, tests[1]):
                fails.append(tests[1])
                
    else:
        if utils.get_NOPROXY()!=0:
            utils.warn("Tests require the user proxy password, please use -i option")
            utils.show_progress("Tests require the user proxy password, please use -i option")
        else:
            utils.warn("Tests require variable MYPROXYSERVER, please set it in the configuration file")
            utils.show_progress("Tests require variable MYPROXYSERVER, please set it in the configuration file")


    if len(fails) > 0 :
      utils.exit_failure("%s test(s) fail(s): %s"%(len(fails), fails))
    else:
      utils.exit_success()

if __name__ == "__main__":
    main()
