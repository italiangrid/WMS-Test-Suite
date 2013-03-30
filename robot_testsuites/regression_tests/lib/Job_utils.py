import time
import commands
import os
import os.path
import logging
import traceback

from lib.Exceptions import *


def prepare_normal_job(utils,filename,dest_ce=""):
    utils.set_isb_jdl(filename)

    if dest_ce !="":
       utils.set_destination_ce(filename,dest_ce)


def prepare_collection_job(utils,filename,dest_ce=""):

     utils.set_isb_jdl(filename)

     if dest_ce !="":
       utils.set_destination_ce(filename,dest_ce)

     # create 3 jdl files based on basic jdl file
     logging.info("Create 3 jdl files based on basic jdl file %s",filename)

     if os.path.isdir("%s/collection_jdls"%(utils.get_tmp_dir())):
         os.system("rm -rf %s/collection_jdls"%(utils.get_tmp_dir()))
     
     os.mkdir("%s/collection_jdls"%(utils.get_tmp_dir()))
     os.system("cp %s %s/collection_jdls/1.jdl"%(filename,utils.get_tmp_dir()))
     os.system("cp %s %s/collection_jdls/2.jdl"%(filename,utils.get_tmp_dir()))
     os.system("cp %s %s/collection_jdls/3.jdl"%(filename,utils.get_tmp_dir()))


def prepare_parametric_job(utils,filename,dest_ce):
    utils.set_parametric_jdl(filename)

    if dest_ce !="":
       utils.set_destination_ce(filename, dest_ce)

def prepare_dag_job(utils,filename,dest_ce):
    utils.set_dag_jdl(filename)

    if dest_ce !="":
       utils.set_destination_ce(filename, dest_ce)

def prepare_mpi_job(utils,filename,dest_ce):

    utils.set_mpi_jdl(filename)

    if dest_ce !="":
       utils.set_mpi_destination_ce(filename,dest_ce)

def submit_normal_job(utils,dest_ce):

    ret=[0,""]

    try:

        logging.info("Submit normal job")
    
        JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
        
        logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

        logging.info("Wait 60 secs before check job")
        time.sleep(60)

        CENAME=utils.get_CE(JOBID)

        if dest_ce !="":

            logging.info("Check if it match a correct CE")

            OUTPUT=commands.getstatusoutput("grep %s <<< \"%s\" > /dev/null"%(dest_ce,CENAME))

            if OUTPUT[0] != 0 :
                logging.error("Error !!! Matching CE is %s",CENAME)
                logging.info("Cancel job %s",JOBID)
                utils.run_command("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
                ret[0]=1
                ret[1]="Matchmaking fails"
                raise GeneralError("","Error!!! Matching CE is %s"%(CENAME))
                return ret
            else:
                logging.info("Matchmaking is ok, now wait the job to finish")


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
   

def submit_collection_job(utils,dest_ce):

    ret=[0,""]

    try:

        logging.info("Submit collection job")

        JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg --collection %s/collection_jdls"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_tmp_dir()))

        logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

        logging.debug("Wait 60 secs before check job")
        time.sleep(60)

        if dest_ce != "":

            logging.info("Check if it match correct CEs")

            OUTPUT=commands.getstatusoutput("glite-wms-job-status %s | grep 'Destination' | grep %s "%(JOBID,dest_ce))
    
            if OUTPUT[0] !=0 :
                logging.error("Error !!! Matching CE is not %s",dest_ce)
                logging.info("Cancel job %s",JOBID)
                utils.run_command("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
                ret[0]=1
                ret[1]="Matchmaking fails"
                raise GeneralError("","Error !!! Matching CE is not %s"%(dest_ce))
                return ret
            else:
                logging.info("Matchmaking is ok , now wait job to finish")

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


def submit_parametric_job(utils,dest_ce):

    ret=[0,""]

    try:

        logging.info("Submit parametric job")

        JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

        logging.debug("Wait 60 secs before check job")
        time.sleep(60)

        if dest_ce != "" :

            logging.info("Check if it match correct CEs")

            OUTPUT=commands.getstatusoutput("glite-wms-job-status %s | grep 'Destination' | grep %s "%(JOBID,dest_ce))

            if OUTPUT[0] !=0 :
                logging.error("Error !!! Matching CE is not %s",dest_ce)
                logging.info("Cancel job %s",JOBID)
                utils.run_command("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
                ret[0]=1
                ret[1]="Matchmaking fails"
                raise GeneralError("","Error !!! Matching CE is not %s"%(dest_ce))
                return ret
            else:
                logging.info("Matchmaking is ok , now wait job to finish")

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


def submit_dag_job(utils,dest_ce):

    ret=[0,""]

    try:

        logging.info("Submit DAG job")

        JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

        logging.debug("Wait 60 secs before check job")
        time.sleep(60)

        if dest_ce !="" :

            logging.info("Check if it match correct CEs")

            OUTPUT=commands.getstatusoutput("glite-wms-job-status %s | grep 'Destination' | grep %s "%(JOBID,dest_ce))
 
            if OUTPUT[0] !=0 :
                logging.error("Error !!! Matching CE is not %s",dest_ce)
                logging.info("Used destination %s",OUTPUT[1])
                logging.info("Cancel job %s",JOBID)
                utils.run_command("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
                ret[0]=1
                ret[1]="Matchmaking fails"
                raise GeneralError("","Error !!! Matching CE is not %s"%(dest_ce))
                return ret
            else:
                logging.info("Matchmaking is ok, now wait job to finish")

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


def submit_mpi_job(utils,dest_ce):

    ret=[0,""]

    try:

        logging.info("Submit MPI job")

        JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

        logging.debug("Wait 60 secs before check job")
        time.sleep(60)

        if dest_ce !="" :

            logging.info("Check if it match correct CEs")

            OUTPUT=commands.getstatusoutput("glite-wms-job-status %s | grep 'Destination' | grep %s "%(JOBID,dest_ce))

            if OUTPUT[0] !=0 :
                logging.error("Error !!! Matching CE is not %s",dest_ce)
                logging.info("Used destination %s",OUTPUT[1])
                logging.info("Cancel job %s",JOBID)
                utils.run_command("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
                ret[0]=1
                ret[1]="Matchmaking fails"
                raise GeneralError("","Error !!! Matching CE is not %s"%(dest_ce))
                return ret
            else:
                logging.info("Matchmaking is ok, now wait job to finish")

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

        logging.info("Try to get the output of the normal job")

        utils.job_status(jobid)
    
        if utils.get_job_status().find("Done (Success)") != -1 :

            utils.remove(utils.get_tmp_file())

            logging.info("Retrieve the output")

            utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))
            logging.info("Check if the output files are correctly retrieved")

            if os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.err"%(utils.get_job_output_dir())) :
                logging.info("Output files are collectly retrieved")
                return ret
            else:
                ret[0]=1
                ret[1]="Output files are not correctly retrieved"
                logging.error("Output files are not correctly retrieved")
                raise GeneralError("","Output files are not correctly retrieved")
                return ret

        else:
            logging.error("Job finishes with status %s cannont retrieve output",utils.get_job_status())
            ret[0]=1
            ret[1]="Job finishes with status: %s cannot retrieve output"%(utils.get_job_status())
            raise GeneralError("","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
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

        logging.info("Try to get the output of the collection job")

        utils.job_status(jobid)

        if utils.get_job_status().find("Done (Success)") != -1 :

            utils.remove(utils.get_tmp_file())

            logging.info("Retrieve the collection output")

            utils.run_command("glite-wms-job-output --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))

            logging.info("Check if the basic output directory exists")

            DIR=utils.run_command("grep '%s' %s"%(utils.get_tmp_dir(),utils.get_tmp_file()))

            if os.path.isdir(DIR):
                logging.info("Basic output directory exists")
            else:
                logging.error("Basic output directory does not exist")
                ret[0]=1
                ret[1]="Basic output directory does not exist"
                raise GeneralError("","Basic output directory does not exist")
                return ret

            logging.info("Check if node directories are correctly created")

            if os.path.isdir("%s/Node_1_jdl"%(DIR)) & os.path.isdir("%s/Node_2_jdl"%(DIR)) & os.path.isdir("%s/Node_3_jdl"%(DIR)) :
                logging.info("Node directories are collectly created")
                return ret
            else:
                logging.error("Node directories are not correctly created")
                ret[0]=1
                ret[1]="Node directories are not correctly created"
                raise GeneralError("","Node directories are not correctly created")
                return ret

            logging.info("Check if the output files are correctly retrieved")

            if os.path.isfile("%s/Node_1_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_1_jdl/std.err"%(DIR)) & os.path.isfile("%s/Node_2_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_2_jdl/std.err"%(DIR)) & os.path.isfile("%s/Node_3_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_3_jdl/std.err"%(DIR))  :
                logging.info("All output files are collectly retrieved")
                return ret
            else:
                logging.error("Output files are not correctly retrieved")
                ret[0]=1
                ret[1]="Output files are not correctly retrieved"
                raise GeneralError("","Output files are not correctly retrieved")
                return ret

        else:
            logging.error("Job finishes with status %s cannot retrieve output",utils.get_job_status())
            ret[0]=1
            ret[1]="Job finishes with status: %s cannot retrieve output"%(utils.get_job_status())
            raise GeneralError("","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
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

        logging.info("Try to get the output of the parametric job")

        utils.job_status(jobid)

        if utils.get_job_status().find("Done (Success)") != -1 :

            utils.remove(utils.get_tmp_file())

            logging.info("Retrieve the parametric job output")

            utils.run_command("glite-wms-job-output --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))

            logging.info("Check if the basic output directory exists")

            DIR=utils.run_command("grep '%s' %s"%(utils.get_tmp_dir(),utils.get_tmp_file()))

            if os.path.isdir(DIR):
                logging.info("Basic output directory exists")
            else:
                logging.error("Basic output directory does not exist")
                ret[0]=1
                ret[1]="Basic output directory does not exist"
                raise GeneralError("","Basic output directory does not exist")
                return ret

            logging.info("Check if node directories are correctly created")

            if os.path.isdir("%s/Node_1"%(DIR)) & os.path.isdir("%s/Node_3"%(DIR)) & os.path.isdir("%s/Node_5"%(DIR)) & os.path.isdir("%s/Node_7"%(DIR)) & os.path.isdir("%s/Node_9"%(DIR)) :
                logging.info("Node directories are collectly created")
                return ret
            else:
                logging.error("Node directories are not collectly created")
                ret[0]=1
                ret[1]="Node directories are not correctly created"
                raise GeneralError("","Node directories are not correctly created")
                return ret

            logging.info("Check if the output files are correctly retrieved")

            if os.path.isfile("%s/Node_1/ouput1.txt"%(DIR)) & os.path.isfile("%s/Node_1/error1.txt"%(DIR)) & os.path.isfile("%s/Node_3/ouput3.txt"%(DIR)) & os.path.isfile("%s/Node_3/error3.txt"%(DIR)) & os.path.isfile("%s/Node_5/ouput5.txt"%(DIR)) & os.path.isfile("%s/Node_5/error5.txt"%(DIR)) & os.path.isfile("%s/Node_7/ouput7.txt"%(DIR)) & os.path.isfile("%s/Node_7/error7.txt"%(DIR)) &  os.path.isfile("%s/Node_9/ouput9.txt"%(DIR)) & os.path.isfile("%s/Node_9/error9.txt"%(DIR))  :
                logging.info("Output files are collectly retrieved")
                return ret
            else:
                logging.error("Output files are not collectly retrieved")
                ret[0]=1
                ret[1]="Output files are not correctly retrieved"
                raise GeneralError("","Output files are not collectly retrieved")
                return ret

        else:
            logging.error("Job finishes with status %s cannot retrieve output",utils.get_job_status())
            ret[0]=1
            ret[1]="Job finishes with status: %s cannot retrieve output"%(utils.get_job_status())
            raise GeneralError("","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
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

        logging.info("Try to get the output of the DAG job")

        utils.job_status(jobid)

        if utils.get_job_status().find("Done (Success)") != -1 :

            utils.remove(utils.get_tmp_file())

            logging.info("Retrieve the DAG job output")

            utils.run_command("glite-wms-job-output --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))

            logging.info("Check if the basic output directory exists")

            DIR=utils.run_command("grep '%s' %s"%(utils.get_tmp_dir(),utils.get_tmp_file()))

            if os.path.isdir(DIR):
                logging.info("Basic output directory exists")
            else:
                logging.error("Basic output directory does not exist")
                ret[0]=1
                ret[1]="Basic output directory does not exist"
                raise GeneralError("","Basic output directory does not exist")
                return ret

            logging.info("Check if node directories are correctly created")

            if os.path.isdir("%s/nodeA"%(DIR)) & os.path.isdir("%s/nodeB"%(DIR)) & os.path.isdir("%s/nodeC"%(DIR)) :
                logging.info("Node directories are collectly created")
                return ret
            else:
                logging.error("Node directories are not collectly created")
                ret[0]=1
                ret[1]="Node directories are not correctly created"
                raise GeneralError("","Node directories are not correctly created")
                return ret

            logging.info("Check if the output files are correctly retrieved")

            if os.path.isfile("%s/nodeA/std.out"%(DIR)) & os.path.isfile("%s/nodeA/std.err"%(DIR)) & os.path.isfile("%s/nodeB/std.out"%(DIR)) & os.path.isfile("%s/nodeB/std.err"%(DIR)) & os.path.isfile("%s/nodeC/std.out"%(DIR)) & os.path.isfile("%s/nodeC/std.err"%(DIR)) :
                logging.info("Output files are collectly retrieved")
                return ret
            else:
                logging.error("Output files are not collectly retrieved")
                ret[0]=1
                ret[1]="Output files are not correctly retrieved"
                raise GeneralError("","Output files are not correctly retrieved")
                return ret

        else:
            logging.error("Job finishes with status %s cannot retrieve output",utils.get_job_status())
            ret[0]=1
            ret[1]="Job finishes with status: %s cannot retrieve output"%(utils.get_job_status())
            raise GeneralError("","Job finishes with status: %s cannot retrieve the output"%(utils.get_job_status()))
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

        logging.info("Try to get the output of the MPI job")

        utils.job_status(jobid)

        if utils.get_job_status().find("Done (Success)") != -1 :

            utils.remove(utils.get_tmp_file())

            logging.info("Retrieve the output")

            utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))

            logging.info("Check if the output files are correctly retrieved")

            if os.path.isfile("%s/hello.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/hello.err"%(utils.get_job_output_dir())) :
                logging.info("Output files are collectly retrieved")
                return ret
            else:
                ret[0]=1
                ret[1]="Output files are not correctly retrieved"
                logging.error("Output files are not correctly retrieved")
                raise GeneralError("","Output files are not correctly retrieved")
                return ret

        else:
            logging.error("Job finishes with status %s cannont retrieve output",utils.get_job_status())
            ret[0]=1
            ret[1]="Job finishes with status: %s cannot retrieve output"%(utils.get_job_status())
            raise GeneralError("","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
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
  

#####

def submit_output_normal_job(utils,dest_ce=""):

  
    logging.info("Submit normal job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

    time.sleep(60)

    if dest_ce !="":

            CENAME=utils.get_CE(JOBID)

            logging.info("Check if it match a correct CE")

            OUTPUT=commands.getstatusoutput("grep %s <<< \"%s\" > /dev/null"%(dest_ce,CENAME))

            if OUTPUT[0] != 0 :
                logging.error("Error !!! Matching CE is %s",CENAME)
                logging.info("Cancel job %s",JOBID)
                utils.run_command("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
                raise GeneralError("","Error!!! Matching CE is %s"%(CENAME))
            else:
                logging.info("Matchmaking is ok, now wait the job to finish")


    utils.wait_until_job_finishes (JOBID)
    output_normal_job(utils,JOBID)




def output_normal_job(utils,jobid):

   
    logging.info("Try to get the output of job %s"%(jobid))

    utils.job_status(jobid)

    if utils.get_job_status().find("Done (Success)") != -1 :

            utils.remove(utils.get_tmp_file())

            logging.info("Retrieve the output")

            utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))

    else:
            logging.error("Job finishes with status %s cannont retrieve output",utils.get_job_status())
            raise GeneralError("","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))



def output_parametric_job(utils,jobid):

  
    logging.info("Try to get the output of the parametric job")

    utils.job_status(jobid)

    if utils.get_job_status().find("Done (Success)") != -1 :

            utils.remove(utils.get_tmp_file())

            logging.info("Retrieve the parametric job output")

            utils.run_command("glite-wms-job-output --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid,utils.get_tmp_file()))

            logging.info("Check if the basic output directory exists")

            DIR=utils.run_command("grep '%s' %s"%(utils.get_tmp_dir(),utils.get_tmp_file()))

            return DIR

    else:
            logging.error("Job finishes with status %s cannot retrieve output",utils.get_job_status())
            raise GeneralError("","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
        


def submit_wait_finish(utils,dest_ce=""):

    logging.info("Submit a job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

    time.sleep(60)

    if dest_ce !="":

            CENAME=utils.get_CE(JOBID)

            logging.info("Check if it match a correct CE")

            OUTPUT=commands.getstatusoutput("grep %s <<< \"%s\" > /dev/null"%(dest_ce,CENAME))

            if OUTPUT[0] != 0 :
                logging.error("Error !!! Matching CE is %s",CENAME)
                logging.info("Cancel job %s",JOBID)
                utils.run_command("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
                raise GeneralError("","Error!!! Matching CE is %s"%(CENAME))
            else:
                logging.info("Matchmaking is ok, now wait the job to finish")


    utils.wait_until_job_finishes (JOBID)

    return JOBID


def submit_collection_wait_finish(utils,dest_ce):

    logging.info("Submit collection job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg --collection %s/collection_jdls"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_tmp_dir()))

    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)

    time.sleep(60)

    if dest_ce != "":

            logging.info("Check if it match correct CEs")

            OUTPUT=commands.getstatusoutput("glite-wms-job-status %s | grep 'Destination' | grep %s "%(JOBID,dest_ce))

            if OUTPUT[0] !=0 :
                logging.error("Error !!! Matching CE is not %s",dest_ce)
                logging.info("Cancel job %s",JOBID)
                utils.run_command("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
                raise GeneralError("","Error !!! Matching CE is not %s"%(dest_ce))

            else:
                logging.info("Matchmaking is ok , now wait job to finish")

    utils.wait_until_job_finishes (JOBID)

    return JOBID
