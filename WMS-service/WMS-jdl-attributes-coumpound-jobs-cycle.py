#!/usr/bin/python

import sys
import signal
import os
import os.path
import commands
import time

import traceback

import Test_utils
import Job_utils


from Exceptions import *

def dag_with_dags_jdl(utils,filename):

    utils.info("Define a DAG jdl which contains other DAG")

    utils.error("This test is not yet implemented")
    
    raise GeneralError("","This test is not yet implemented")

def dag_resubmission_jdl(utils,filename,resubmission_type):

    utils.info("Define a DAG jdl")

    FILE = open(filename,"w")

    FILE.write("Type = \"dag\";\n")
    FILE.write("nodes = [\n")

    FILE.write("nodeA = [\n")
    FILE.write("description = [\n")
    FILE.write("JobType = \"Normal\";\n")
    FILE.write("Executable = \"/bin/date\";\n")

    if resubmission_type=="shallow":
         FILE.write("Prologue = \"/bin/false\";\n")
    else:
         FILE.write("Epilogue = \"/bin/false\";\n")

    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("];\n");
    FILE.write("];\n");
    
    FILE.write("nodeB = [\n");
    FILE.write("description = [\n");
    FILE.write("JobType = \"Normal\";\n");
    FILE.write("Executable = \"/bin/date\";\n");

    if resubmission_type=="shallow":
         FILE.write("Prologue = \"/bin/false\";\n")
    else:
         FILE.write("Epilogue = \"/bin/false\";\n")

    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("];\n");
    FILE.write("];\n");

    FILE.write("nodeC = [\n");
    FILE.write("description = [\n");
    FILE.write("JobType = \"Normal\";\n");
    FILE.write("Executable = \"/bin/date\";\n");
    
    if resubmission_type=="shallow":
         FILE.write("Prologue = \"/bin/false\";\n")
    else:
         FILE.write("Epilogue = \"/bin/false\";\n")

    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("];\n");
    FILE.write("];\n");
    
    FILE.write("];\n");
    FILE.write("dependencies = { { nodeA, nodeB },{  nodeA, nodeC } };\n");

    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))



def collection_resubmission_jdl(utils,filename,resubmission_type):

    utils.info("Define a collection jdl")

    FILE = open(filename,"w")

    FILE.write("Type = \"collection\";\n")
    FILE.write("nodes = {\n")

    for i in range(3):

      FILE.write("[\n")
      FILE.write("NodeName=\"Node_%s_jdl\";\n"%(i+1));
      FILE.write("JobType = \"Normal\";\n")
      FILE.write("Executable = \"/bin/hostname\";\n")

      if resubmission_type=="shallow":
           FILE.write("Prologue = \"/bin/false\";\n")
      else:
           FILE.write("Epilogue = \"/bin/false\";\n")
           
      FILE.write("StdOutput  = \"std.out\";\n");
      FILE.write("StdError   = \"std.err\";\n");
      FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
      FILE.write("],\n");

    FILE.write("[\n")
    FILE.write("NodeName=\"Node_4_jdl\";\n");
    FILE.write("JobType = \"Normal\";\n")
    FILE.write("Executable = \"/bin/hostname\";\n")

    if resubmission_type=="shallow":
         FILE.write("Prologue = \"/bin/false\";\n")
    else:
         FILE.write("Epilogue = \"/bin/false\";\n")

    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("]\n");


    FILE.write("};\n");

    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


def dag_allowzipped_jdl(utils,filename):

    utils.info("Define a DAG jdl with AllowZippedISB attribute")

    utils.run_command_continue_on_error("cp %s %s/fileA"%(utils.get_config_file(),utils.get_tmp_dir()))
    utils.run_command_continue_on_error("cp %s %s/fileB"%(utils.get_config_file(),utils.get_tmp_dir()))
    utils.run_command_continue_on_error("cp %s %s/fileC"%(utils.get_config_file(),utils.get_tmp_dir()))

    FILE = open(filename,"w")

    FILE.write("Type = \"dag\";\n")
    FILE.write("nodes = [\n")

    FILE.write("nodeA = [\n")
    FILE.write("description = [\n")
    FILE.write("JobType = \"Normal\";\n")
    FILE.write("Executable = \"/bin/ls\";\n")
    FILE.write("Arguments = \"-la\";\n")
    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("InputSandbox = {\"%s/fileA\"};\n"%(utils.get_tmp_dir()));
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("];\n");
    FILE.write("];\n");

    FILE.write("nodeB = [\n");
    FILE.write("description = [\n");
    FILE.write("JobType = \"Normal\";\n");
    FILE.write("Executable = \"/bin/ls\";\n");
    FILE.write("Arguments = \"-la\";\n")
    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("InputSandbox = {\"%s/fileB\"};\n"%(utils.get_tmp_dir()));
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("];\n");
    FILE.write("];\n");

    FILE.write("nodeC = [\n");
    FILE.write("description = [\n");
    FILE.write("JobType = \"Normal\";\n");
    FILE.write("Executable = \"/bin/ls\";\n");
    FILE.write("Arguments = \"-la\";\n")
    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("InputSandbox = {\"%s/fileC\"};\n"%(utils.get_tmp_dir()));
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("];\n");
    FILE.write("];\n");

    FILE.write("];\n");
    FILE.write("dependencies = { { nodeA, nodeB },{  nodeA, nodeC } };\n");
    FILE.write("AllowZippedISB = true;\n")

    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


def collection_allowzipped_jdl(utils,filename):

    utils.info("Define a collection jdl with AllowzippedISB attribute")

    utils.run_command_continue_on_error("cp %s %s/fileA"%(utils.get_config_file(),utils.get_tmp_dir()))
    utils.run_command_continue_on_error("cp %s %s/fileB"%(utils.get_config_file(),utils.get_tmp_dir()))
    utils.run_command_continue_on_error("cp %s %s/fileC"%(utils.get_config_file(),utils.get_tmp_dir()))
    utils.run_command_continue_on_error("cp %s %s/fileD"%(utils.get_config_file(),utils.get_tmp_dir()))

    FILE = open(filename,"w")

    FILE.write("Type = \"collection\";\n")
    FILE.write("nodes = {\n")

    for i in range(3):

      FILE.write("[\n")
      FILE.write("NodeName=\"Node_%s_jdl\";\n"%(i+1));
      FILE.write("JobType = \"Normal\";\n")
      FILE.write("Executable = \"/bin/ls\";\n")
      FILE.write("Arguments = \"-la\";\n")
      FILE.write("StdOutput  = \"std.out\";\n");
      FILE.write("StdError   = \"std.err\";\n");
      FILE.write("InputSandbox = {\"%s/fileA\",\"%s/fileB\"};\n"%(utils.get_tmp_dir(),utils.get_tmp_dir()));
      FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
      FILE.write("],\n");

    FILE.write("[\n")
    FILE.write("NodeName=\"Node_4_jdl\";\n");
    FILE.write("JobType = \"Normal\";\n")
    FILE.write("Executable = \"/bin/ls\";\n")
    FILE.write("Arguments = \"-la\";\n")
    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("InputSandbox = {\"%s/fileC\",\"%s/fileD\"};\n"%(utils.get_tmp_dir(),utils.get_tmp_dir()));
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("]\n");

    FILE.write("};\n");

    FILE.write("AllowZippedISB = true;\n")

    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


def dag_usertags_jdl(utils,filename):

    utils.info("Define a DAG jdl with UserTags attribute")

    FILE = open(filename,"w")

    FILE.write("Type = \"dag\";\n")
    FILE.write("nodes = [\n")

    FILE.write("nodeA = [\n")
    FILE.write("description = [\n")
    FILE.write("JobType = \"Normal\";\n")
    FILE.write("Executable = \"/bin/hostname\";\n")
    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("UserTags = [ WMSTestsuiteTag = \"Hello from nodeA\"; ];\n")
    FILE.write("];\n");
    FILE.write("];\n");

    FILE.write("nodeB = [\n");
    FILE.write("description = [\n");
    FILE.write("JobType = \"Normal\";\n");
    FILE.write("Executable = \"/bin/hostname\";\n");
    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("UserTags = [ WMSTestsuiteTag = \"Hello from nodeB\"; ];\n")
    FILE.write("];\n");
    FILE.write("];\n");

    FILE.write("nodeC = [\n");
    FILE.write("description = [\n");
    FILE.write("JobType = \"Normal\";\n");
    FILE.write("Executable = \"/bin/hostname\";\n");
    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("UserTags = [ WMSTestsuiteTag = \"Hello from nodeC\"; ];\n")
    FILE.write("];\n");
    FILE.write("];\n");

    FILE.write("];\n");
    FILE.write("dependencies = { { nodeA, nodeB },{  nodeA, nodeC } };\n");
    FILE.write("UserTags = [ WMSTestsuiteTag = \"Hello from DAG\"; ];\n")

    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))



def collection_usertags_jdl(utils,filename):

    utils.info("Define a collection jdl with UserTags attribute")

    FILE = open(filename,"w")

    FILE.write("Type = \"collection\";\n")
    FILE.write("nodes = {\n")

    for i in range(3):

      FILE.write("[\n")
      FILE.write("NodeName=\"Node_%s_jdl\";\n"%(i+1));
      FILE.write("JobType = \"Normal\";\n")
      FILE.write("Executable = \"/bin/hostname\";\n")
      FILE.write("StdOutput  = \"std.out\";\n");
      FILE.write("StdError   = \"std.err\";\n");
      FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
      FILE.write("UserTags = [ WMSTestsuiteTag = \"Hello from Node_%s_jdl\"; ];\n"%(i+1))
      FILE.write("],\n");

    FILE.write("[\n")
    FILE.write("NodeName=\"Node_4_jdl\";\n");
    FILE.write("JobType = \"Normal\";\n")
    FILE.write("Executable = \"/bin/hostname\";\n")
    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("UserTags = [ WMSTestsuiteTag = \"Hello from Node_4_jdl\"; ];\n")
    FILE.write("]\n");

    FILE.write("};\n");

    FILE.write("UserTags = [ WMSTestsuiteTag = \"Hello from collection\"; ];\n")
    
    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))



def dag_expirytime_jdl(utils,filename):

    utils.info("Define a DAG jdl with ExpiryTime attribute")

    FILE = open(filename,"w")

    FILE.write("Type = \"dag\";\n")
    FILE.write("nodes = [\n")

    FILE.write("nodeA = [\n")
    FILE.write("description = [\n")
    FILE.write("JobType = \"Normal\";\n")
    FILE.write("Executable = \"/bin/hostname\";\n")
    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("ExpiryTime = %s;\n"%int(time.time()+120))
    FILE.write("Requirements = false; \n")
    FILE.write("];\n");
    FILE.write("];\n");

    FILE.write("nodeB = [\n");
    FILE.write("description = [\n");
    FILE.write("JobType = \"Normal\";\n");
    FILE.write("Executable = \"/bin/hostname\";\n");
    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("ExpiryTime = %s;\n"%int(time.time()+120))
    FILE.write("Requirements = false; \n")
    FILE.write("];\n");
    FILE.write("];\n");

    FILE.write("nodeC = [\n");
    FILE.write("description = [\n");
    FILE.write("JobType = \"Normal\";\n");
    FILE.write("Executable = \"/bin/hostname\";\n");
    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("Requirements = false; \n")
    FILE.write("];\n");
    FILE.write("];\n");

    FILE.write("];\n");
    FILE.write("dependencies = { { nodeA, nodeB },{  nodeA, nodeC } };\n");
    FILE.write("RetryCount = 1; \n")
    FILE.write("ExpiryTime = %s;\n"%int(time.time()+180))

    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


def collection_expirytime_jdl(utils,filename):

    utils.info("Define a collection jdl with ExpiryTime attribute")

    FILE = open(filename,"w")

    FILE.write("Type = \"collection\";\n")
    FILE.write("nodes = {\n")

    for i in range(3):

      FILE.write("[\n")
      FILE.write("NodeName=\"Node_%s_jdl\";\n"%(i+1));
      FILE.write("JobType = \"Normal\";\n")
      FILE.write("Executable = \"/bin/hostname\";\n")
      FILE.write("StdOutput  = \"std.out\";\n");
      FILE.write("StdError   = \"std.err\";\n");
      FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
      FILE.write("ExpiryTime = %s;\n"%int(time.time()+120))
      FILE.write("Requirements = false; \n")
      FILE.write("],\n");

    FILE.write("[\n")
    FILE.write("NodeName=\"Node_4_jdl\";\n");
    FILE.write("JobType = \"Normal\";\n")
    FILE.write("Executable = \"/bin/hostname\";\n")
    FILE.write("StdOutput  = \"std.out\";\n");
    FILE.write("StdError   = \"std.err\";\n");
    FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
    FILE.write("Requirements = false; \n")
    FILE.write("]\n");

    FILE.write("};\n");

    FILE.write("RetryCount = 1; \n")
    FILE.write("ExpiryTime = %s;\n"%int(time.time()+180))

    FILE.close()

    utils.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))





def test1(utils,title):

    names,ces=utils.get_target_ces()

    fails=0

    if len(names)==0:
        names.append("Default Test")
        ces.append("")

    for i in range(len(names)):

        utils.show_progress("%s - %s"%(title,names[i]))

        utils.info("%s - %s"%(title,names[i]))

        try:

            dag_with_dags_jdl(utils,utils.get_jdl_file())

            if len(ces[i])>0:
                 utils.set_requirements("%s && %s"%(ces[i],utils.DEFAULTREQ))
            else:
                 utils.set_requirements("%s"%utils.DEFAULTREQ)

            utils.info("Submit DAG job")

            JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

            utils.info("Wait until job finishes")

            utils.wait_until_job_finishes(JOBID)

            utils.info("Check final status")

            utils.job_status(JOBID)

            if utils.get_job_status().find("Done") != -1 :
                utils.info("Job's final status is Done")
                    
            else:
                utils.error("TEST FAILED: Job finishes with status: %s"%(utils.get_job_status()))
                raise GeneralError("Check job's final status","Job finishes with status: %s"%(utils.get_job_status()))

        except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            fails=fails+1


    return fails


def test2(utils,title):

    names,ces=utils.get_target_ces()

    fails=0

    if len(names)==0:
        names.append("Default Test")
        ces.append("")

    for i in range(len(names)):

        utils.show_progress("%s - %s"%(title,names[i]))

        utils.info("%s - %s"%(title,names[i]))

        try:

            dag_resubmission_jdl(utils,utils.get_jdl_file(),"deep")

            NodeRetryCount = 1

            utils.add_jdl_general_attribute("DefaultNodeRetryCount",NodeRetryCount)

            if len(ces[i])>0:
                 utils.set_requirements("%s && %s"%(ces[i],utils.DEFAULTREQ))
            else:
                 utils.set_requirements("%s"%utils.DEFAULTREQ)

            utils.info("Submit coumpound job")

            JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

            utils.info("Wait until job finishes")

            utils.wait_until_job_finishes(JOBID)

            utils.job_status(JOBID)

            deep_counter=[]
            status=[]
            status_reason=[]

            if utils.get_job_status().find("Aborted") != -1 :

                ids = utils.get_from_coumpound_job_all_nodes_ids(JOBID)

                for id in ids:

                    utils.info("Get final status for job: %s"%(id))
                    utils.job_status(id)
                    status.append(utils.get_job_status())

                    utils.info("Get status reason for job: %s"%(id))
                    reason = utils.get_job_status_reason(id)
                    status_reason.append(reason)

                    if reason.find("hit job retry count (%s)"%(NodeRetryCount)) != -1:
                        deep_counter.append(id)

                utils.info("Check status reason for all jobs")

                if len(deep_counter)!= len(ids) :
                     utils.error("TEST FAILS: Coumpound job %s hasn't be correctlly resubmitted"%(JOBID))
                     utils.error("TEST FAILS: Only %s / %s of jobs have aborted reason 'hit job retry count (%s)'"%(len(deep_counter),len(ids),NodeRetryCount))
                     utils.error("TEST FAILS: Final status for all jobs: %s"%(status))
                     utils.error("TEST FAILS: Status reason for all jobs: %s"%(status_reason))
                     raise GeneralError("Check the number of resubmissions","Coumpound job %s hasn't be correctly resubmitted"%(JOBID))
                else:
                    utils.info("Test OK")

            else:
                utils.error("TEST FAILS. Problem , coumpound job's final status is %s"%(utils.get_job_status()))
                raise GeneralError("Check if final status is Aborted","Problem , coumpound job's final status is %s"%(utils.get_job_status()))


        except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            fails=fails+1


    return fails



def test3(utils,title):

    names,ces=utils.get_target_ces()

    fails=0

    if len(names)==0:
        names.append("Default Test")
        ces.append("")

    for i in range(len(names)):

        utils.show_progress("%s - %s"%(title,names[i]))

        utils.info("%s - %s"%(title,names[i]))

        try:

            collection_resubmission_jdl(utils,utils.get_jdl_file(),"deep")

            NodeRetryCount = 1
            
            utils.add_jdl_general_attribute("DefaultNodeRetryCount",NodeRetryCount)

            if len(ces[i])>0:
                 utils.set_requirements("%s && %s"%(ces[i],utils.DEFAULTREQ))
            else:
                 utils.set_requirements("%s"%utils.DEFAULTREQ)

            utils.info("Submit coumpound job")

            JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

            utils.info("Wait until job finishes")

            utils.wait_until_job_finishes(JOBID)

            utils.job_status(JOBID)

            deep_counter=[]
            status=[]
            status_reason=[]

            if utils.get_job_status().find("Aborted") != -1 :

                ids = utils.get_from_coumpound_job_all_nodes_ids(JOBID)

                for id in ids:

                    utils.info("Get final status for job: %s"%(id))
                    utils.job_status(id)
                    status.append(utils.get_job_status())

                    utils.info("Get status reason for job: %s"%(id))
                    reason = utils.get_job_status_reason(id)
                    status_reason.append(reason)

                    if reason.find("hit job retry count (%s)"%(NodeRetryCount)) != -1:
                        deep_counter.append(id)

                utils.info("Check status reason for all jobs")

                if len(deep_counter)!= len(ids) :
                     utils.error("TEST FAILS: Coumpound job %s hasn't be correctlly resubmitted"%(JOBID))
                     utils.error("TEST FAILS: Only %s / %s of jobs have aborted reason 'hit job retry count (%s)'"%(len(deep_counter),len(ids),NodeRetryCount))
                     utils.error("TEST FAILS: Final status for all jobs: %s"%(status))
                     utils.error("TEST FAILS: Status reason for all jobs: %s"%(status_reason))
                     raise GeneralError("Check the number of resubmissions","Coumpound job %s hasn't be correctly resubmitted"%(JOBID))
                else:
                    utils.info("Test OK")

            else:
                utils.error("TEST FAILS. Problem , coumpound job's final status is %s"%(utils.get_job_status()))
                raise GeneralError("Check if final status is Aborted","Problem , coumpound job's final status is %s"%(utils.get_job_status()))


        except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            fails=fails+1


    return fails


def test4(utils,title):

    names,ces=utils.get_target_ces()

    fails=0

    if len(names)==0:
        names.append("Default Test")
        ces.append("")

    for i in range(len(names)):

        utils.show_progress("%s - %s"%(title,names[i]))

        utils.info("%s - %s"%(title,names[i]))

        try:

            dag_resubmission_jdl(utils,utils.get_jdl_file(),"shallow")

            NodeShallowRetryCount = 1
                                             
            utils.add_jdl_general_attribute("DefaultNodeShallowRetryCount",NodeShallowRetryCount)

            if len(ces[i])>0:
                 utils.set_requirements("%s && %s"%(ces[i],utils.DEFAULTREQ))
            else:
                 utils.set_requirements("%s"%utils.DEFAULTREQ)

            utils.info("Submit DAG job")

            JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

            utils.info("Wait until job finishes")

            utils.wait_until_job_finishes(JOBID)

            utils.job_status(JOBID)

            shallow_counter=[]

            if utils.get_job_status().find("Aborted") != -1 :

                ids = utils.get_from_coumpound_job_all_nodes_ids(JOBID)

                for id in ids:

                    utils.info("Get resubmission times for job: %s"%(id))

                    output=utils.run_command_continue_on_error ("glite-wms-job-logging-info --event RESUBMISSION %s"%(id))

                    shallow_counter.append(output.count("SHALLOW"))

                utils.info("Check resubmission times")

                if sum(shallow_counter)!= NodeShallowRetryCount*3 :
                     utils.error("TEST FAILS: Coumpound job %s hasn't be correctlly resubmitted"%(JOBID))
                     raise GeneralError("Check the number of resubmissions","Coumpound job %s hasn't be correctly resubmitted"%(JOBID))
                else:
                    utils.info("Test OK")

            else:
                utils.error("TEST FAILS. Problem , jobs final status is %s"%(utils.get_job_status()))
                raise GeneralError("Check if jobs final status is Aborted","Problem , jobs final status is %s"%(utils.get_job_status()))


        except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            fails=fails+1


    return fails



def test5(utils,title):

    names,ces=utils.get_target_ces()

    fails=0

    if len(names)==0:
        names.append("Default Test")
        ces.append("")

    for i in range(len(names)):

        utils.show_progress("%s - %s"%(title,names[i]))

        utils.info("%s - %s"%(title,names[i]))

        try:

            collection_resubmission_jdl(utils,utils.get_jdl_file(),"shallow")

            NodeShallowRetryCount = 1

            utils.add_jdl_general_attribute("DefaultNodeShallowRetryCount",NodeShallowRetryCount)

            if len(ces[i])>0:
                 utils.set_requirements("%s && %s"%(ces[i],utils.DEFAULTREQ))
            else:
                 utils.set_requirements("%s"%utils.DEFAULTREQ)

            utils.info("Submit coumpound job")

            JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
            
            utils.info("Wait until job finishes")
            
            utils.wait_until_job_finishes(JOBID)

            utils.job_status(JOBID)

            shallow_counter=[]
            
            if utils.get_job_status().find("Aborted") != -1 :

                ids = utils.get_from_coumpound_job_all_nodes_ids(JOBID)

                for id in ids:

                    utils.info("Get resubmission times for job: %s"%(id))

                    output=utils.run_command_continue_on_error ("glite-wms-job-logging-info --event RESUBMISSION %s"%(id))

                    shallow_counter.append(output.count("SHALLOW"))

                utils.info("Check resubmission times")

                if sum(shallow_counter)!= NodeShallowRetryCount*4 :
                     utils.error("TEST FAILS: Coumpound job %s hasn't be correctlly resubmitted"%(JOBID))
                     raise GeneralError("Check the number of resubmissions","Coumpound job %s hasn't be correctly resubmitted"%(JOBID))
                else:
                    utils.info("Test OK")
                    
            else:
                utils.error("TEST FAILS. Problem , jobs final status is %s"%(utils.get_job_status()))
                raise GeneralError("Check if jobs final status is Aborted","Problem , jobs final status is %s"%(utils.get_job_status()))
            

        except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            fails=fails+1


    return fails



def test6(utils,title):

    names,ces=utils.get_target_ces()

    fails=0

    if len(names)==0:
        names.append("Default Test")
        ces.append("")

    for i in range(len(names)):

        utils.show_progress("%s - %s"%(title,names[i]))

        utils.info("%s - %s"%(title,names[i]))

        try:

            dag_allowzipped_jdl(utils,utils.get_jdl_file())

            if len(ces[i])>0:
                 utils.set_requirements("%s && %s"%(ces[i],utils.DEFAULTREQ))
            else:
                 utils.set_requirements("%s"%utils.DEFAULTREQ)

            utils.info("Submit DAG job")

            output=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --debug %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

            messages=['File archiving and file compression allowed by user in the JDL']
            messages.append('Archiving the ISB files')
            messages.append('ISB ZIPPED file successfully created')

            utils.info("Check debug output for expected messages")

            for message in messages:

                utils.info("Check for message: %s"%(messages))

                if output.find(message)==-1:
                    utils.error("Message %s not found"%(message))
                    raise GeneralError("Check for message: %s"%(messages),"Message %s not found"%(message))
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
                raise GeneralError("Check if AllowZippedISB Attribute is added","Attribute AllowZippedISB not added to the jdl")

            utils.info("Check if ZippedISB Attribute is added:")

            if output.find("ZippedISB = { \"%s\" };"%(ZippedISB))!=-1:
                utils.info("Attribute ZippedISB successfully added to the jdl")
            else:
                utils.error("Unable to find ZippedISB={\"%s\"} to the jdl"%(ZippedISB))
                raise GeneralError("Check if ZippedISB Attribute is added","Unable to find ZippedISB={\"%s\"} to the jdl"%(ZippedISB))

            utils.info("Wait until job finishes")

            utils.wait_until_job_finishes(JOBID)

            utils.info("Try to get job output")

            utils.job_status(JOBID)

            if utils.get_job_status().find("Done") != -1 :

                utils.remove(utils.get_tmp_file())

                utils.info("Retrieve the output")

                utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

                utils.info("Check if the basic output directory exists")

                DIR=utils.run_command_continue_on_error("grep '%s' %s"%(utils.get_tmp_dir(),utils.get_tmp_file()))

                if os.path.isdir(DIR):
                    utils.info("Basic output directory exists")
                else:
                    utils.error("Basic output directory does not exist")
                    raise GeneralError("Check output directory","Basic output directory does not exist")

                utils.info("Check if node directories are correctly created")

                if os.path.isdir("%s/nodeA"%(DIR)) & os.path.isdir("%s/nodeB"%(DIR)) & os.path.isdir("%s/nodeC"%(DIR)):
                    utils.info("Node directories are correctly created")
                else:
                    utils.error("Node directories are not correctly created")
                    raise GeneralError("Check output directories of the nodes","Node directories are not correctly created")

                utils.info("Check if the output files are correctly retrieved")

                if os.path.isfile("%s/nodeA/std.out"%(DIR)) & os.path.isfile("%s/nodeA/std.err"%(DIR)) & os.path.isfile("%s/nodeB/std.out"%(DIR)) & os.path.isfile("%s/nodeB/std.err"%(DIR)) & os.path.isfile("%s/nodeC/std.out"%(DIR)) & os.path.isfile("%s/nodeC/std.err"%(DIR)) :

                     utils.info("All output files are correctly retrieved")

                     utils.info("Check std output to see if all the files are transferred to the CE")

                     output1=utils.run_command_continue_on_error("cat %s/nodeA/std.out"%(utils.get_job_output_dir()))
                     output2=utils.run_command_continue_on_error("cat %s/nodeB/std.out"%(utils.get_job_output_dir()))
                     output3=utils.run_command_continue_on_error("cat %s/nodeC/std.out"%(utils.get_job_output_dir()))

                     utils.info("Check for file 'fileA' to std.out file for node nodeA")

                     if output1.find("fileA")==-1:
                           utils.error("File is not transferred to the CE for nodeA")
                           raise GeneralError("Check for file in nodeA","File is not transferred to the CE for nodeA")
                     else:
                           utils.info("File successfully transferred to the CE for nodeA")

                     if output2.find("fileB")==-1:
                           utils.error("File is not transferred to the CE for nodeB")
                           raise GeneralError("Check for file in nodeB","File is not transferred to the CE for nodeB")
                     else:
                           utils.info("File successfully transferred to the CE for nodeB")

                     if output3.find("fileC")==-1:
                           utils.error("File is not transferred to the CE for nodeC")
                           raise GeneralError("Check for file in nodeC","File is not transferred to the CE for nodeC")
                     else:
                           utils.info("File successfully transferred to the CE for nodeC")
                     

                else:
                    utils.error("Output files are not correctly retrieved")
                    raise GeneralError("Check output files","Output files are not correctly retrieved")

            else:
                utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
                raise GeneralError("Try to get the job output","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))


        except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            fails=fails+1


    return fails



def test7(utils,title):

    names,ces=utils.get_target_ces()

    fails=0

    if len(names)==0:
        names.append("Default Test")
        ces.append("")

    for i in range(len(names)):

        utils.show_progress("%s - %s"%(title,names[i]))

        utils.info("%s - %s"%(title,names[i]))

        try:

            collection_allowzipped_jdl(utils,utils.get_jdl_file())

            if len(ces[i])>0:
                 utils.set_requirements("%s && %s"%(ces[i],utils.DEFAULTREQ))
            else:
                 utils.set_requirements("%s"%utils.DEFAULTREQ)

            utils.info("Submit coumpound job")

            output=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --debug %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

            messages=['File archiving and file compression allowed by user in the JDL']
            messages.append('Archiving the ISB files')
            messages.append('ISB ZIPPED file successfully created')

            utils.info("Check debug output for expected messages")

            for message in messages:

                utils.info("Check for message: %s"%(messages))

                if output.find(message)==-1:
                    utils.error("Message %s not found"%(message))
                    raise GeneralError("Check for message: %s"%(messages),"Message %s not found"%(message))
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
                raise GeneralError("Check if AllowZippedISB Attribute is added","Attribute AllowZippedISB not added to the jdl")

            utils.info("Check if ZippedISB Attribute is added:")

            if output.find("ZippedISB = { \"%s\" };"%(ZippedISB))!=-1:
                utils.info("Attribute ZippedISB successfully added to the jdl")
            else:
                utils.error("Unable to find ZippedISB={\"%s\"} to the jdl"%(ZippedISB))
                raise GeneralError("Check if ZippedISB Attribute is added","Unable to find ZippedISB={\"%s\"} to the jdl"%(ZippedISB))

            utils.info("Wait until job finishes")

            utils.wait_until_job_finishes(JOBID)

            utils.info("Try to get job output")

            utils.job_status(JOBID)

            if utils.get_job_status().find("Done") != -1 :

                utils.remove(utils.get_tmp_file())

                utils.info("Retrieve the output")

                utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

                utils.info("Check if the basic output directory exists")

                DIR=utils.run_command_continue_on_error("grep '%s' %s"%(utils.get_tmp_dir(),utils.get_tmp_file()))

                if os.path.isdir(DIR):
                    utils.info("Basic output directory exists")
                else:
                    utils.error("Basic output directory does not exist")
                    raise GeneralError("Check output directory","Basic output directory does not exist")

                utils.info("Check if node directories are correctly created")

                if os.path.isdir("%s/Node_1_jdl"%(DIR)) & os.path.isdir("%s/Node_2_jdl"%(DIR)) & os.path.isdir("%s/Node_3_jdl"%(DIR)) & os.path.isdir("%s/Node_4_jdl"%(DIR)):
                    utils.info("Node directories are correctly created")
                else:
                    utils.error("Node directories are not correctly created")
                    raise GeneralError("Check output directories of the nodes","Node directories are not correctly created")
            
                utils.info("Check if the output files are correctly retrieved")

                if os.path.isfile("%s/Node_1_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_1_jdl/std.err"%(DIR)) & os.path.isfile("%s/Node_2_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_2_jdl/std.err"%(DIR)) & os.path.isfile("%s/Node_3_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_3_jdl/std.err"%(DIR)) & os.path.isfile("%s/Node_4_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_4_jdl/std.err"%(DIR))  :

                     utils.info("All output files are correctly retrieved")
 
                     utils.info("Check std output to see if all the files are transferred to the CE")

                     output1=utils.run_command_continue_on_error("cat %s/Node_1_jdl/std.out"%(utils.get_job_output_dir()))
                     output2=utils.run_command_continue_on_error("cat %s/Node_2_jdl/std.out"%(utils.get_job_output_dir()))
                     output3=utils.run_command_continue_on_error("cat %s/Node_3_jdl/std.out"%(utils.get_job_output_dir()))
                     output4=utils.run_command_continue_on_error("cat %s/Node_4_jdl/std.out"%(utils.get_job_output_dir()))

                     utils.info("Check for files 'fileA' and 'fileB' to std.out file for nodes Node_1_jdl , Node_2_jdl and Node_3_jdl")

                     if output1.find("fileA")==-1 and output4.find("fileB")==-1:
                           utils.error("Files are not transferred to the CE for Node_1_jdl")
                           raise GeneralError("Check for files in Node_1_jdl","Files are not transferred to the CE for Node_1_jdl")
                     else:
                           utils.info("Files successfully transferred to the CE for Node_1_jdl")

                     if output2.find("fileA")==-1 and output4.find("fileB")==-1:
                           utils.error("Files are not transferred to the CE for Node_2_jdl")
                           raise GeneralError("Check for files in Node_2_jdl","Files are not transferred to the CE for Node_2_jdl")
                     else:
                           utils.info("Files successfully transferred to the CE for Node_2_jdl")

                     if output3.find("fileA")==-1 and output4.find("fileB")==-1:
                           utils.error("Files are not transferred to the CE for Node_3_jdl")
                           raise GeneralError("Check for files in Node_3_jdl","Files are not transferred to the CE for Node_3_jdl")
                     else:
                           utils.info("Files successfully transferred to the CE for Node_3_jdl")

                     utils.info("Check for files 'fileC' and 'fileB' to std.out file for nodes Node_4_jdl")

                     if output4.find("fileC")==-1 and output4.find("fileD")==-1:
                           utils.error("Files are not transferred to the CE for Node_4_jdl")
                           raise GeneralError("Check for files in Node_4_jdl","Files are not transferred to the CE for Node_4_jdl")
                     else:
                           utils.info("Files successfully transferred to the CE for Node_4_jdl")


                else:
                    utils.error("Output files are not correctly retrieved")
                    raise GeneralError("Check output files","Output files are not correctly retrieved")
            
            else:
                utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
                raise GeneralError("Try to get the job output","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))


        except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            fails=fails+1


    return fails



def test8(utils,title):

    names,ces=utils.get_target_ces()

    fails=0

    if len(names)==0:
        names.append("Default Test")
        ces.append("")

    for i in range(len(names)):

        utils.show_progress("%s - %s"%(title,names[i]))

        utils.info("%s - %s"%(title,names[i]))

        try:

            dag_usertags_jdl(utils,utils.get_jdl_file())

            if len(ces[i])>0:
                 utils.set_requirements("%s && %s"%(ces[i],utils.DEFAULTREQ))
            else:
                 utils.set_requirements("%s"%utils.DEFAULTREQ)

            utils.info("Submit coumpound job")

            JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

            utils.job_status(JOBID)

            while utils.get_job_status().find("Ready")!=-1 or utils.get_job_status().find("Waiting")!=-1:
                utils.info("Wait 10 secs until status changed from Waiting or Ready")
                time.sleep(10)
                utils.job_status(JOBID)

            utils.info("Check logging info for defined user tag for DAG")

            output=utils.run_command_continue_on_error("glite-wms-job-logging-info -v 2 --event UserTag %s"%(JOBID))

            if output.find("WMSTestsuiteTag")!=-1 and output.find("Hello from DAG")!=-1:
                utils.info("Find defined user tag")
            else:
                utils.error("Unable to find defined user tag")
                raise GeneralError("Check for defined user tag","Unable to find defined user tag")

            node_ids=[]

            output=utils.run_command_continue_on_error("glite-wms-job-status -v 0 %s"%(JOBID))

            for line in output.split("\n"):
                if line.find("Status info for the Job")!=-1 and line.find(JOBID)==-1:
                    node_ids.append(line.split(" : ")[1].strip(" \n\t"))

            utils.info("Find the following node: %s"%(node_ids))

            logging_events_messages=""

            for id in node_ids:

               utils.info("Check user tag for node : %s"%(id))

               utils.job_status(id)

               while utils.get_job_status().find("Ready")!=-1 or utils.get_job_status().find("Waiting")!=-1:
                   utils.info("Wait 10 secs until status changed from Waiting or Ready")
                   time.sleep(10)
                   utils.job_status(id)

               output=utils.run_command_continue_on_error("glite-wms-job-logging-info -v 2 --event UserTag %s"%(id))

               logging_events_messages=logging_events_messages+output


            if logging_events_messages.count("WMSTestsuiteTag")==3 and logging_events_messages.find("Hello from nodeA")!=-1 and logging_events_messages.find("Hello from nodeB")!=-1 and logging_events_messages.find("Hello from nodeC")!=-1 :
                  utils.info("Find all defined user tags in nodes")
            else:
                  utils.error("Unable to find all the defined user tags in nodes")
                  raise GeneralError("Check for defined user tags in nodes","Unable to find all the defined user tags in nodes")

            utils.info("Wait until job finishes")

            utils.wait_until_job_finishes(JOBID)

            utils.info("Try to get job output")

            utils.job_status(JOBID)

            if utils.get_job_status().find("Done") != -1 :

                utils.remove(utils.get_tmp_file())

                utils.info("Retrieve the output")

                utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

                utils.info("Check if the basic output directory exists")

                DIR=utils.run_command_continue_on_error("grep '%s' %s"%(utils.get_tmp_dir(),utils.get_tmp_file()))

                if os.path.isdir(DIR):
                    utils.info("Basic output directory exists")
                else:
                    utils.error("Basic output directory does not exist")
                    raise GeneralError("Check output directory","Basic output directory does not exist")

                utils.info("Check if node directories are correctly created")

                if os.path.isdir("%s/nodeA"%(DIR)) & os.path.isdir("%s/nodeB"%(DIR)) & os.path.isdir("%s/nodeC"%(DIR)) :
                    utils.info("Node directories are correctly created")
                else:
                    utils.error("Node directories are not correctly created")
                    raise GeneralError("Check output directories of the nodes","Node directories are not correctly created")

                utils.info("Check if the output files are correctly retrieved")

                if os.path.isfile("%s/nodeA/std.out"%(DIR)) & os.path.isfile("%s/nodeA/std.err"%(DIR)) & os.path.isfile("%s/nodeB/std.out"%(DIR)) & os.path.isfile("%s/nodeB/std.err"%(DIR)) & os.path.isfile("%s/nodeC/std.out"%(DIR)) & os.path.isfile("%s/nodeC/std.err"%(DIR)) :

                     utils.info("All output files are correctly retrieved")

                else:
                    utils.error("Output files are not correctly retrieved")
                    raise GeneralError("Check output files","Output files are not correctly retrieved")

            else:
                utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
                raise GeneralError("Try to get the job output","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))


        except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            fails=fails+1


    return fails



def test9(utils,title):

    names,ces=utils.get_target_ces()

    fails=0

    if len(names)==0:
        names.append("Default Test")
        ces.append("")

    for i in range(len(names)):

        utils.show_progress("%s - %s"%(title,names[i]))

        utils.info("%s - %s"%(title,names[i]))

        try:

            collection_usertags_jdl(utils,utils.get_jdl_file())

            if len(ces[i])>0:
                 utils.set_requirements("%s && %s"%(ces[i],utils.DEFAULTREQ))
            else:
                 utils.set_requirements("%s"%utils.DEFAULTREQ)

            utils.info("Submit coumpound job")
        
            JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

            utils.job_status(JOBID)

            while utils.get_job_status().find("Ready")!=-1 or utils.get_job_status().find("Waiting")!=-1:
                utils.info("Wait 10 secs until status changed from Waiting or Ready")
                time.sleep(10)
                utils.job_status(JOBID)

            utils.info("Check logging info for defined user tag for collection")

            output=utils.run_command_continue_on_error("glite-wms-job-logging-info -v 2 --event UserTag %s"%(JOBID))

            if output.find("WMSTestsuiteTag")!=-1 and output.find("Hello from collection")!=-1:
                utils.info("Find defined user tag")
            else:
                utils.error("Unable to find defined user tag")
                raise GeneralError("Check for defined user tag","Unable to find defined user tag")

            node_ids=[]

            output=utils.run_command_continue_on_error("glite-wms-job-status -v 0 %s"%(JOBID))

            for line in output.split("\n"):
                if line.find("Status info for the Job")!=-1 and line.find(JOBID)==-1:
                    node_ids.append(line.split(" : ")[1].strip(" \n\t"))

            utils.info("Find the following nodes: %s"%(node_ids))

            logging_events_messages=""

            for id in node_ids:

               utils.info("Check user tag for node : %s"%(id))

               utils.job_status(id)

               while utils.get_job_status().find("Ready")!=-1 or utils.get_job_status().find("Waiting")!=-1:
                   utils.info("Wait 10 secs until status changed from Waiting or Ready")
                   time.sleep(10)
                   utils.job_status(id)

               output=utils.run_command_continue_on_error("glite-wms-job-logging-info -v 2 --event UserTag %s"%(id))

               logging_events_messages=logging_events_messages+output


            if logging_events_messages.count("WMSTestsuiteTag")==4 and logging_events_messages.find("Hello from Node_1_jdl")!=-1 and logging_events_messages.find("Hello from Node_2_jdl")!=-1 and logging_events_messages.find("Hello from Node_3_jdl")!=-1 and logging_events_messages.find("Hello from Node_4_jdl")!=-1:
                  utils.info("Find all defined user tags in nodes")
            else:
                  utils.error("Unable to find all the defined user tags in nodes")
                  raise GeneralError("Check for defined user tags in nodes","Unable to find all the defined user tags in nodes")
             
            utils.info("Wait until job finishes")

            utils.wait_until_job_finishes(JOBID)

            utils.info("Try to get job output")

            utils.job_status(JOBID)

            if utils.get_job_status().find("Done") != -1 :

                utils.remove(utils.get_tmp_file())

                utils.info("Retrieve the output")

                utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),JOBID,utils.get_tmp_file()))

                utils.info("Check if the basic output directory exists")

                DIR=utils.run_command_continue_on_error("grep '%s' %s"%(utils.get_tmp_dir(),utils.get_tmp_file()))

                if os.path.isdir(DIR):
                    utils.info("Basic output directory exists")
                else:
                    utils.error("Basic output directory does not exist")
                    raise GeneralError("Check output directory","Basic output directory does not exist")

                utils.info("Check if node directories are correctly created")

                if os.path.isdir("%s/Node_1_jdl"%(DIR)) & os.path.isdir("%s/Node_2_jdl"%(DIR)) & os.path.isdir("%s/Node_3_jdl"%(DIR)) & os.path.isdir("%s/Node_4_jdl"%(DIR)):
                    utils.info("Node directories are correctly created")
                else:
                    utils.error("Node directories are not correctly created")
                    raise GeneralError("Check output directories of the nodes","Node directories are not correctly created")

                utils.info("Check if the output files are correctly retrieved")

                if os.path.isfile("%s/Node_1_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_1_jdl/std.err"%(DIR)) & os.path.isfile("%s/Node_2_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_2_jdl/std.err"%(DIR)) & os.path.isfile("%s/Node_3_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_3_jdl/std.err"%(DIR)) & os.path.isfile("%s/Node_4_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_4_jdl/std.err"%(DIR))  :

                     utils.info("All output files are correctly retrieved")
                     
                else:
                    utils.error("Output files are not correctly retrieved")
                    raise GeneralError("Check output files","Output files are not correctly retrieved")

            else:
                utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
                raise GeneralError("Try to get the job output","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))


        except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            fails=fails+1


    return fails


def test10(utils,title):

    names,ces=utils.get_target_ces()

    fails=0

    if len(names)==0:
        names.append("Default Test")
        ces.append("")

    for i in range(len(names)):

        utils.show_progress("%s - %s"%(title,names[i]))

        utils.info("%s - %s"%(title,names[i]))

        try:

            dag_expirytime_jdl(utils,utils.get_jdl_file())

            if len(ces[i])>0:
                 utils.set_requirements("%s && %s"%(ces[i],utils.DEFAULTREQ))
            else:
                 utils.set_requirements("%s"%utils.DEFAULTREQ)

            utils.info("Submit coumpound job")

            JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

            node_ids=[]

            output=utils.run_command_continue_on_error("glite-wms-job-status -v 0 %s"%(JOBID))

            for line in output.split("\n"):
                if line.find("Status info for the Job")!=-1 and line.find(JOBID)==-1:
                    node_ids.append(line.split(" : ")[1].strip(" \n\t"))

            utils.info("Find the following nodes: %s"%(node_ids))

            utils.info("Wait until job finishes")

            utils.wait_until_job_finishes(JOBID)

            utils.info("Check job's final status")

            utils.job_status(JOBID)

            if utils.get_job_status().find("Aborted") != -1 :

                utils.info("Job's final status is Aborted as expected")

                utils.info("Check failed reason")

                if utils.get_job_status_reason(JOBID).find("request expired")!=-1:
                    utils.info("Aborted reason is 'request expired' as expected")
                else:
                    utils.error("Error: Job's final status is aborted by failed reason is '%s' , while expected is 'request expired'"%(utils.get_job_status_reason(JOBID)))
                    raise GeneralError("Check failed reason","Error: Job's final status is aborted by failed reason is '%s' , while expected is 'request expired'"%(utils.get_job_status_reason(JOBID)))


                for id in node_ids:

                    utils.info("Check status and reason for node: %s"%(id))

                    utils.job_status(id)
                    status=utils.get_job_status()
                    reason=utils.get_job_status_reason(id)

                    if status.find("Aborted")!=-1 and reason.find("request expired")!=-1:
                        utils.info("Node %s is Aborted with reason 'request expired' as expected"%(id))
                    else:
                        utils.error("Node %s isn't Aborted with reason 'request expired' as expected"%(id))
                        raise GeneralError("Check status and reason for node: %s"%(id),"Node %s isn't Aborted with reason 'request expired' as expected"%(id))

            else:
                utils.error("Test Failed. Job's final status is not Aborted as expected , instead we get %s"%(utils.get_job_status()))
                raise GeneralError("Check job's final status","Test Failed. Job's final status is not Aborted as expected , instead we get %s"%(utils.get_job_status()))

        except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            fails=fails+1

    return fails



def test11(utils,title):

    names,ces=utils.get_target_ces()

    fails=0

    if len(names)==0:
        names.append("Default Test")
        ces.append("")

    for i in range(len(names)):

        utils.show_progress("%s - %s"%(title,names[i]))

        utils.info("%s - %s"%(title,names[i]))

        try:

            collection_expirytime_jdl(utils,utils.get_jdl_file())

            if len(ces[i])>0:
                 utils.set_requirements("%s && %s"%(ces[i],utils.DEFAULTREQ))
            else:
                 utils.set_requirements("%s"%utils.DEFAULTREQ)

            utils.info("Submit coumpound job")

            JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

            node_ids=[]

            output=utils.run_command_continue_on_error("glite-wms-job-status -v 0 %s"%(JOBID))

            for line in output.split("\n"):
                if line.find("Status info for the Job")!=-1 and line.find(JOBID)==-1:
                    node_ids.append(line.split(" : ")[1].strip(" \n\t"))

            utils.info("Find the following nodes: %s"%(node_ids))

            utils.info("Wait until job finishes")

            utils.wait_until_job_finishes(JOBID)

            utils.info("Check job's final status")

            utils.job_status(JOBID)

            if utils.get_job_status().find("Aborted") != -1 :

                utils.info("Job's final status is Aborted as expected")

                utils.info("Check failed reason")

                if utils.get_job_status_reason(JOBID).find("request expired")!=-1:
                    utils.info("Aborted reason is 'request expired' as expected")
                else:
                    utils.error("Error: Job's final status is aborted by failed reason is '%s' , while expected is 'request expired'"%(utils.get_job_status_reason(JOBID)))
                    raise GeneralError("Check failed reason","Error: Job's final status is aborted by failed reason is '%s' , while expected is 'request expired'"%(utils.get_job_status_reason(JOBID)))


                for id in node_ids:

                    utils.info("Check status and reason for node: %s"%(id))

                    utils.job_status(id)
                    status=utils.get_job_status()
                    reason=utils.get_job_status_reason(id)

                    if status.find("Aborted")!=-1 and reason.find("request expired")!=-1:
                        utils.info("Node %s is Aborted with reason 'request expired' as expected"%(id))
                    else:
                        utils.error("Node %s isn't Aborted with reason 'request expired' as expected"%(id))
                        raise GeneralError("Check status and reason for node: %s"%(id),"Node %s isn't Aborted with reason 'request expired' as expected"%(id))
        
            else:
                utils.error("Test Failed. Job's final status is not Aborted as expected , instead we get %s"%(utils.get_job_status()))
                raise GeneralError("Check job's final status","Test Failed. Job's final status is not Aborted as expected , instead we get %s"%(utils.get_job_status()))

        except (RunCommandError,GeneralError,TimeOutError) , e :
            utils.log_error("%s"%(utils.get_current_test()))
            utils.log_error("Command: %s"%(e.expression))
            utils.log_error("Message: %s"%(e.message))
            utils.log_traceback("%s"%(utils.get_current_test()))
            utils.log_traceback(traceback.format_exc())
            fails=fails+1

    return fails




def main():
    	
    utils = Test_utils.Test_utils(sys.argv[0],"Test a complete job cycle for coumpound jobs with non default jdl files")

    tests=["TEST 1: Check job cycle using DAG job with jdl that contains other DAG"]
    tests.append("TEST 2: Check job cycle using DAG job and jdl with DefaultNodeRetryCount attribute")
    tests.append("TEST 3: Check job cycle using jobs collection and jdl with DefaultNodeRetryCount attribute")
    tests.append("TEST 4: Check job cycle using DAG job and jdl with DefaultNodeShallowRetryCount attribute")
    tests.append("TEST 5: Check job cycle using jobs collection and jdl with DefaultNodeShallowRetryCount attribute")
    tests.append("TEST 6: Check job cycle using DAG job and jdl with AllowZippedISB attribute")
    tests.append("TEST 7: Check job cycle using jobs collection and jdl with AllowZippedISB attribute")
    tests.append("TEST 8: Check job cycle using DAG job and jdl with UserTags attribute")
    tests.append("TEST 9: Check job cycle using jobs collection and jdl with UserTags attribute")
    tests.append("TEST 10: Check job cycle using DAG job and jdl with ExpiryTime attribute")
    tests.append("TEST 11: Check job cycle using jobs collection and jdl with ExpiryTime attribute")

    utils.prepare(sys.argv[1:],tests)

    utils.info("Test a complete job cycle for coumpound jobs with non default jdl files : from submission to get output")

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

    if all_tests==1 or utils.check_test_enabled(8)==1 :
         if test8(utils, tests[7]):
            fails.append(tests[7])

    if all_tests==1 or utils.check_test_enabled(9)==1 :
         if test9(utils, tests[8]):
            fails.append(tests[8])

    if all_tests==1 or utils.check_test_enabled(10)==1 :
         if test10(utils, tests[9]):
            fails.append(tests[9])

    if all_tests==1 or utils.check_test_enabled(11)==1 :
         if test11(utils, tests[10]):
            fails.append(tests[10])


    if len(fails) > 0 :
      utils.exit_failure("%s test(s) fail(s): %s"%(len(fails), fails))
    else:
      utils.exit_success()


if __name__ == "__main__":
    main()
