import time
import commands
import os
import os.path
import traceback

from Exceptions import *


def prepare_normal_job(utils,filename,dest_ce=""):
    utils.set_isb_jdl(filename)

    if dest_ce !="":
       utils.set_destination_ce(filename,dest_ce)

def prepare_collection_job(utils,filename,dest_ce=""):

     if dest_ce !="":
       utils.set_destination_ce(filename,dest_ce)

     # create 3 jdl files based on basic jdl file
     utils.info("Create 3 jdl files based on basic jdl file %s"%(filename))

     if os.path.isdir("%s/collection_jdls"%(utils.get_tmp_dir())):
         os.system("rm -rf %s/collection_jdls"%(utils.get_tmp_dir()))
     
     os.mkdir("%s/collection_jdls"%(utils.get_tmp_dir()))
     os.system("cp %s %s/collection_jdls/1.jdl"%(filename,utils.get_tmp_dir()))
     os.system("cp %s %s/collection_jdls/2.jdl"%(filename,utils.get_tmp_dir()))
     os.system("cp %s %s/collection_jdls/3.jdl"%(filename,utils.get_tmp_dir()))


def prepare_single_jdl_for_collection_job(utils,filename,dest_ce=""):

    #utils.set_collection_jdl(filename)
    utils.set_collection_external_jdls(filename)

    if dest_ce !="":
        utils.set_destination_ce(filename,dest_ce)


def prepare_parametric_job(utils,filename,dest_ce=""):
    utils.set_parametric_jdl(filename)

    if dest_ce !="":
       utils.set_destination_ce(filename, dest_ce)

def prepare_dag_job(utils,filename,dest_ce=""):
    utils.set_dag_jdl(filename)

    if dest_ce !="":
       utils.set_destination_ce(filename, dest_ce)

def prepare_mpi_job(utils,filename,dest_ce=""):

    utils.set_mpi_jdl(filename)

    if dest_ce !="":
       utils.set_mpi_destination_ce(filename,dest_ce)


def submit_normal_job(utils,dest_ce=""):

    ret=[0,""]

    try:

        utils.info("Submit normal job")
    
        JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
        
        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        utils.dbg("Wait 60 secs before check job")
        time.sleep(60)

        CENAME=utils.get_CE(JOBID)

        if dest_ce !="":

            utils.info ("Check if it match a correct CE")

            OUTPUT=commands.getstatusoutput("grep %s <<< \"%s\" > /dev/null"%(dest_ce,CENAME))

            if OUTPUT[0] != 0 :
                utils.error("Matching CE is %s"%(CENAME))
                utils.info("Cancel job %s"%(JOBID))
                utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
                ret[0]=1
                ret[1]="Matchmaking fails"
                raise GeneralError("Check destination CE","Error!!! Matching CE is %s"%(CENAME))
                return ret
            else:
                utils.info("Matchmaking is ok , now wait job to finish ")


        utils.wait_until_job_finishes (JOBID)
        ret=get_normal_job_output(utils,JOBID)
        return ret
     
    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        ret[0]=1
        return ret


def submit_only_normal_job(utils,dest_ce=""):

    ret=[0,""]

    try:

        utils.info("Submit normal job")

        JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        ret[1]=JOBID

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        CENAME=utils.get_CE(JOBID)

        if dest_ce !="":

            utils.dbg("Wait 60 secs before check job")
            time.sleep(60)

            utils.info ("Check if it match a correct CE")

            OUTPUT=commands.getstatusoutput("grep %s <<< \"%s\" > /dev/null"%(dest_ce,CENAME))

            if OUTPUT[0] != 0 :
                utils.error("Matching CE is %s"%(CENAME))
                utils.info("Cancel job %s"%(JOBID))
                utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
                ret[0]=1
                ret[1]="Matchmaking fails"
                raise GeneralError("Check destination CE","Error!!! Matching CE is %s"%(CENAME))
                return ret
            else:
                utils.info("Matchmaking is ok , now wait job to finish ")
                ret[1]=JOBID

        return ret

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        ret[0]=1
        return ret


def submit_collection_job(utils,dest_ce="",single_file=False):

    ret=[0,""]

    try:

        utils.info("Submit collection job")

        if single_file ==True:
          JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
        else:
          JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg --collection %s/collection_jdls"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_tmp_dir()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        utils.dbg("Wait 60 secs before check job")
        time.sleep(60)

        if dest_ce != "":

            utils.info("Check if it match correct CEs")

            OUTPUT=commands.getstatusoutput("glite-wms-job-status %s | grep 'Destination' | grep %s "%(JOBID,dest_ce))
    
            if OUTPUT[0] !=0 :
                utils.error("Matching CE is not %s"%(dest_ce))
                utils.info("Cancel job %s",JOBID)
                utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
                ret[0]=1
                ret[1]="Matchmaking fails"
                raise GeneralError("Check destination CE","Error !!! Matching CE is not %s"%(dest_ce))
                return ret
            else:
                utils.info("Matchmaking is ok , now wait job to finish")

        utils.wait_until_job_finishes (JOBID)
        ret=get_collection_job_output(utils,JOBID)
        return ret

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        ret[0]=1
        return ret


def submit_parametric_job(utils,dest_ce=""):

    ret=[0,""]

    try:

        utils.info("Submit parametric job")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        utils.dbg("Wait 60 secs before check job")
        time.sleep(60)

        if dest_ce != "" :

            utils.info("Check if it match correct CEs")

            OUTPUT=commands.getstatusoutput("glite-wms-job-status %s | grep 'Destination' | grep %s "%(JOBID,dest_ce))

            if OUTPUT[0] !=0 :
                utils.error("Matching CE is not %s"%(dest_ce))
                utils.info("Cancel job %s"%(JOBID))
                utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
                ret[0]=1
                ret[1]="Matchmaking fails"
                raise GeneralError("Check destination CE","Error !!! Matching CE is not %s"%(dest_ce))
                return ret
            else:
                utils.info("Matchmaking is ok , now wait job to finish")

        utils.wait_until_job_finishes (JOBID)
        ret=get_parametric_job_output(utils,JOBID)
        return ret

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        ret[0]=1
        return ret


def submit_dag_job(utils,dest_ce=""):

    ret=[0,""]

    try:

        utils.info("Submit DAG job")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        utils.dbg("Wait 60 secs before check job")
        time.sleep(60)

        if dest_ce !="" :

            utils.info ("Check if it match correct CEs")

            OUTPUT=commands.getstatusoutput("glite-wms-job-status %s | grep 'Destination' | grep %s "%(JOBID,dest_ce))
 
            if OUTPUT[0] !=0 :
                utils.error("Matching CE is not %s"%(dest_ce))
                utils.info("Used destination %s"%(OUTPUT[1]))
                utils.info("Cancel job %s"%(JOBID))
                utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
                ret[0]=1
                ret[1]="Matchmaking fails"
                raise GeneralError("Check destination CE","Error !!! Matching CE is not %s"%(dest_ce))
                return ret
            else:
                utils.ingo("Matchmaking is ok , now wait job to finish")

        utils.wait_until_job_finishes (JOBID)
        ret=get_dag_job_output(utils,JOBID)
        return ret

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        ret[0]=1
        return ret


def submit_mpi_job(utils,dest_ce=""):

    ret=[0,""]

    try:

        utils.info("Submit MPI job")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        utils.dbg("Wait 60 secs before check job")
        time.sleep(60)

        if dest_ce !="" :

            utils.info ("Check if it match correct CEs")

            OUTPUT=commands.getstatusoutput("glite-wms-job-status %s | grep 'Destination' | grep %s "%(JOBID,dest_ce))

            if OUTPUT[0] !=0 :
                utils.error("Matching CE is not %s"%(dest_ce))
                utils.info("Used destination %s"%(OUTPUT[1]))
                utils.info("Cancel job %s"%(JOBID))
                utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
                ret[0]=1
                ret[1]="Matchmaking fails"
                raise GeneralError("Check destination CE","Error !!! Matching CE is not %s"%(dest_ce))
                return ret
            else:
                utils.info("Matchmaking is ok , now wait job to finish")

        utils.wait_until_job_finishes (JOBID)
        ret=get_mpi_job_output(utils,JOBID)
        return ret

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        ret[0]=1
        return ret


def get_normal_job_output(utils,jobid):

    ret=[0,""]

    try:

        utils.info("Try to get the output of the normal job")

        utils.job_status(jobid)
    
        if utils.get_job_status().find("Done") != -1 :

            utils.remove(utils.get_tmp_file())

            utils.info("Retrieve the output")

            utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))

            utils.info("Check if the output files are correctly retrieved")

            if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
                utils.info("Output files are correctly retrieved")
                return ret
            else:
                ret[0]=1
                ret[1]="Output files are not correctly retrieved"
                utils.error("Output files are not correctly retrieved")
                raise GeneralError("Check output files","Output files are not correctly retrieved")
                return ret

        else:
            utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            ret[0]=1
            ret[1]="Job finishes with status: %s cannot retrieve output"%(utils.get_job_status())
            raise GeneralError("Check final job status","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            return ret

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        ret[0]=1
        return ret


    return ret


def get_collection_job_output(utils,jobid):

    ret=[0,""]

    try:

        utils.info("Try to get the output of the collection job")

        utils.job_status(jobid)

        if utils.get_job_status().find("Done") != -1 :

            utils.remove(utils.get_tmp_file())

            utils.info("Retrieve the collection output")

            utils.run_command_continue_on_error ("glite-wms-job-output --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))

            utils.info("Check if the basic output directory exists")

            DIR=utils.run_command_continue_on_error("grep '%s' %s"%(utils.get_tmp_dir(),utils.get_tmp_file()))

            if os.path.isdir(DIR):
                utils.info("Basic output directory exists")
            else:
                utils.error("Basic output directory does not exist")
                ret[0]=1
                ret[1]="Basic output directory does not exist"
                raise GeneralError("Check output directory","Basic output directory does not exist")
                return ret

            utils.info("Check if node directories are correctly created")

            if os.path.isdir("%s/Node_1_jdl"%(DIR)) & os.path.isdir("%s/Node_2_jdl"%(DIR)) & os.path.isdir("%s/Node_3_jdl"%(DIR)) :
                utils.info("Node directories are correctly created")
                return ret
            else:
                utils.error("Node directories are not correctly created")
                ret[0]=1
                ret[1]="Node directories are not correctly created"
                raise GeneralError("Check output directories of the nodes","Node directories are not correctly created")
                return ret

            utils.info("Check if the output files are correctly retrieved")

            if os.path.isfile("%s/Node_1_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_1_jdl/std.err"%(DIR)) & os.path.isfile("%s/Node_2_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_2_jdl/std.err"%(DIR)) & os.path.isfile("%s/Node_3_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_3_jdl/std.err"%(DIR))  :
                utils.info("All output files are correctly retrieved")
                return ret
            else:
                utils.error("Output files are not correctly retrieved")
                ret[0]=1
                ret[1]="Output files are not correctly retrieved"
                raise GeneralError("Check output files","Output files are not correctly retrieved")
                return ret

        else:
            utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            ret[0]=1
            ret[1]="Job finishes with status: %s cannot retrieve output"%(utils.get_job_status())
            raise GeneralError("Check final job status","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            return ret

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        ret[0]=1
        return ret

    return ret

def get_parametric_job_output(utils,jobid):

    ret=[0,""]

    try:

        utils.info("Try to get the output of the parametric job")

        utils.job_status(jobid)

        if utils.get_job_status().find("Done") != -1 :

            utils.remove(utils.get_tmp_file())

            utils.info("Retrieve the parametric job output")

            utils.run_command_continue_on_error ("glite-wms-job-output --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))

            utils.info("Check if the basic output directory exists")

            DIR=utils.run_command_continue_on_error("grep '%s' %s"%(utils.get_tmp_dir(),utils.get_tmp_file()))

            if os.path.isdir(DIR):
                utils.info("Basic output directory exists")
            else:
                utils.error("Basic output directory does not exist")
                ret[0]=1
                ret[1]="Basic output directory does not exist"
                raise GeneralError("Check output directory","Basic output directory does not exist")
                return ret

            utils.info("Check if node directories are correctly created")

            if os.path.isdir("%s/Node_1"%(DIR)) & os.path.isdir("%s/Node_3"%(DIR)) & os.path.isdir("%s/Node_5"%(DIR)) & os.path.isdir("%s/Node_7"%(DIR)) & os.path.isdir("%s/Node_9"%(DIR)) :
                utils.info("Node directories are correctly created")
                return ret
            else:
                utils.error("Node directories are not correctly created")
                ret[0]=1
                ret[1]="Node directories are not correctly created"
                raise GeneralError("Check output directories of the nodes","Node directories are not correctly created")
                return ret

            utils.info("Check if the output files are correctly retrieved")

            if os.path.isfile("%s/Node_1/output1.txt"%(DIR)) & os.path.isfile("%s/Node_1/error1.txt"%(DIR)) & os.path.isfile("%s/Node_3/output3.txt"%(DIR)) & os.path.isfile("%s/Node_3/error3.txt"%(DIR)) & os.path.isfile("%s/Node_5/output5.txt"%(DIR)) & os.path.isfile("%s/Node_5/error5.txt"%(DIR)) & os.path.isfile("%s/Node_7/output7.txt"%(DIR)) & os.path.isfile("%s/Node_7/error7.txt"%(DIR)) &  os.path.isfile("%s/Node_9/output9.txt"%(DIR)) & os.path.isfile("%s/Node_9/error9.txt"%(DIR))  :
                utils.info("Output files are correctly retrieved")
                return ret
            else:
                utils.error("Output files are not correctly retrieved")
                ret[0]=1
                ret[1]="Output files are not correctly retrieved"
                raise GeneralError("Check output files","Output files are not correctly retrieved")
                return ret

        else:
            utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            ret[0]=1
            ret[1]="Job finishes with status: %s cannot retrieve output"%(utils.get_job_status())
            raise GeneralError("Check job final status","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            return ret

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        ret[0]=1
        return ret

    return ret


def get_dag_job_output(utils,jobid):

    ret=[0,""]

    try:

        utils.info("Try to get the output of the DAG job")

        utils.job_status(jobid)

        if utils.get_job_status().find("Done") != -1 :

            utils.remove(utils.get_tmp_file())

            utils.info("Retrieve the DAG job output")

            utils.run_command_continue_on_error ("glite-wms-job-output --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))

            utils.info("Check if the basic output directory exists")

            DIR=utils.run_command_continue_on_error ("grep '%s' %s"%(utils.get_tmp_dir(),utils.get_tmp_file()))

            if os.path.isdir(DIR):
                utils.info("Basic output directory exists")
            else:
                utils.error("Basic output directory does not exist")
                ret[0]=1
                ret[1]="Basic output directory does not exist"
                raise GeneralError("Check output directory","Basic output directory does not exist")
                return ret

            utils.info("Check if node directories are correctly created")

            if os.path.isdir("%s/nodeA"%(DIR)) & os.path.isdir("%s/nodeB"%(DIR)) & os.path.isdir("%s/nodeC"%(DIR)) :
                utils.info("Node directories are correctly created")
                return ret
            else:
                utils.error("Node directories are not correctly created")
                ret[0]=1
                ret[1]="Node directories are not correctly created"
                raise GeneralError("Check output directories of the nodes","Node directories are not correctly created")
                return ret

            utils.info("Check if the output files are correctly retrieved")

            if os.path.isfile("%s/nodeA/std.out"%(DIR)) & os.path.isfile("%s/nodeA/std.err"%(DIR)) & os.path.isfile("%s/nodeB/std.out"%(DIR)) & os.path.isfile("%s/nodeB/std.err"%(DIR)) & os.path.isfile("%s/nodeC/std.out"%(DIR)) & os.path.isfile("%s/nodeC/std.err"%(DIR)) :
                utils.info("Output files are correctly retrieved")
                return ret
            else:
                utils.error("Output files are not correctly retrieved")
                ret[0]=1
                ret[1]="Output files are not correctly retrieved"
                raise GeneralError("Check output files","Output files are not correctly retrieved")
                return ret

        else:
            utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            ret[0]=1
            ret[1]="Job finishes with status: %s cannot retrieve output"%(utils.get_job_status())
            raise GeneralError("Check job final status","Job finishes with status: %s cannot retrieve the output"%(utils.get_job_status()))
            return ret

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        ret[0]=1
        return ret
    
    return ret


def get_mpi_job_output(utils,jobid):

    ret=[0,""]

    try:

        utils.info("Try to get the output of the MPI job")

        utils.job_status(jobid)

        if utils.get_job_status().find("Done") != -1 :

            utils.remove(utils.get_tmp_file())

            utils.info("Retrieve the output")

            utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))

            utils.info("Check if the output files are correctly retrieved")

            if os.path.isfile("%s/hello.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/hello.err"%(utils.get_job_output_dir())) :
                utils.info("Output files are correctly retrieved")
                return ret
            else:
                utils.error("Output files are not correctly retrieved")
                ret[0]=1
                ret[1]="Output files are not correctly retrieved"
                raise GeneralError("Check output files","Output files are not correctly retrieved")
                return ret

        else:
            utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            ret[0]=1
            ret[1]="Job finishes with status: %s cannot retrieve output"%(utils.get_job_status())
            raise GeneralError("Check job final status","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            return ret

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        ret[0]=1
        return ret

    return ret
  
