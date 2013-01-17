import time
import commands
import os
import os.path

from Exceptions import *


def prepare_normal_job(utils,filename,dest_ce=""):
    utils.set_isb_jdl(filename)

    if dest_ce !="":
       utils.set_destination_ce(filename,dest_ce)

def prepare_collection_job(utils,filename,dest_ce=""):

     if dest_ce !="":
       utils.set_destination_ce(filename,dest_ce)

     # create 3 jdl files based on basic jdl file
     utils.log_info("Create 3 jdl files based on basic jdl file %s"%(filename))

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

    
    utils.log_info("Submit normal job")
    
    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
        
    utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

    utils.log_info("Wait 60 secs before check job",'DEBUG')
    time.sleep(60)

    CENAME=utils.get_CE(JOBID)

    if dest_ce !="":

       utils.log_info ("Check if it match a correct CE")

       OUTPUT=commands.getstatusoutput("grep %s <<< \"%s\" > /dev/null"%(dest_ce,CENAME))

       if OUTPUT[0] != 0 :
              utils.log_info("EROR: Matching CE is %s"%(CENAME))
              utils.log_info("Cancel job %s"%(JOBID))
              utils.run_command("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))                
              raise GeneralError("Check destination CE","Error!!! Matching CE is %s"%(CENAME))
       else:
              utils.log_info("Matchmaking is ok , now wait job to finish ")

    utils.wait_until_job_finishes (JOBID)
    get_normal_job_output(utils,JOBID)
    


def submit_only_normal_job(utils,dest_ce=""):

    utils.log_info("Submit normal job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(), utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

    CENAME=utils.get_CE(JOBID)

    if dest_ce !="":

        utils.log_info("Wait 60 secs before check job",'DEBUG')
        time.sleep(60)

        utils.log_info ("Check if it match a correct CE")

        OUTPUT=commands.getstatusoutput("grep %s <<< \"%s\" > /dev/null"%(dest_ce,CENAME))

        if OUTPUT[0] != 0 :
              utils.log_info("ERROR: Matching CE is %s"%(CENAME))
              utils.log_info("Cancel job %s"%(JOBID))
              utils.run_command("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
              raise GeneralError("Check destination CE","Error!!! Matching CE is %s"%(CENAME))
        else:
              utils.log_info("Matchmaking is ok , now wait job to finish ")

    return JOBID      

def submit_collection_job(utils,dest_ce="",single_file=''):

    utils.log_info("Submit collection job")

    if len(single_file)>0:
        JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
    else:
        JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg --collection %s/collection_jdls"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_tmp_dir()))

    utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

    utils.log_info("Wait 60 secs before check job",'DEBUG')
    time.sleep(60)

    if dest_ce != "":

       utils.log_info("Check if it match correct CEs")

       OUTPUT=commands.getstatusoutput("glite-wms-job-status %s | grep 'Destination' | grep %s "%(JOBID,dest_ce))
    
       if OUTPUT[0] !=0 :
            utils.log_info("Matching CE is not %s"%(dest_ce))
            utils.log_info("Cancel job %s",JOBID)
            utils.run_command("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
            raise GeneralError("Check destination CE","Error !!! Matching CE is not %s"%(dest_ce))   
       else:
            utils.log_info("Matchmaking is ok , now wait job to finish")

    utils.wait_until_job_finishes(JOBID)
    get_collection_job_output(utils,JOBID)
        


def submit_parametric_job(utils,dest_ce=""):

    utils.log_info("Submit parametric job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(), utils.get_config_file(), utils.get_jdl_file()))

    utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

    utils.log_info("Wait 60 secs before check job",'DEBUG')
    time.sleep(60)

    if dest_ce != "" :

         utils.log_info("Check if it match correct CEs")

         OUTPUT=commands.getstatusoutput("glite-wms-job-status %s | grep 'Destination' | grep %s "%(JOBID,dest_ce))

         if OUTPUT[0] !=0 :
              utils.log_info("ERROR: Matching CE is not %s"%(dest_ce))
              utils.log_info("Cancel job %s"%(JOBID))
              utils.run_command("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
              raise GeneralError("Check destination CE","Error !!! Matching CE is not %s"%(dest_ce))
         else:
              utils.log_info("Matchmaking is ok , now wait job to finish")

    utils.wait_until_job_finishes (JOBID)
    get_parametric_job_output(utils,JOBID)
    

def submit_dag_job(utils,dest_ce=""):

    utils.log_info("Submit DAG job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(), utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

    utils.log_info("Wait 60 secs before check job",'DEBUG')
    time.sleep(60)

    if dest_ce !="" :

         utils.log_info ("Check if it match correct CEs")

         OUTPUT=commands.getstatusoutput("glite-wms-job-status %s | grep 'Destination' | grep %s "%(JOBID,dest_ce))
 
         if OUTPUT[0] !=0 :
              utils.log_info("ERROR: Matching CE is not %s"%(dest_ce))
              utils.log_info("Used destination %s"%(OUTPUT[1]))
              utils.log_info("Cancel job %s"%(JOBID))
              utils.run_command("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
              raise GeneralError("Check destination CE","Error !!! Matching CE is not %s"%(dest_ce))
         else:
              utils.ingo("Matchmaking is ok , now wait job to finish")

    utils.wait_until_job_finishes (JOBID)
    get_dag_job_output(utils,JOBID)
    


def submit_mpi_job(utils,dest_ce=""):

    utils.log_info("Submit MPI job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(), utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

    utils.log_info("Wait 60 secs before check job",'DEBUG')
    time.sleep(60)

    if dest_ce !="" :

        utils.log_info("Check if it match correct CEs")

        OUTPUT=commands.getstatusoutput("glite-wms-job-status %s | grep 'Destination' | grep %s "%(JOBID,dest_ce))

        if OUTPUT[0] !=0 :
             utils.log_info("ERROR: Matching CE is not %s"%(dest_ce))
             utils.log_info("Used destination %s"%(OUTPUT[1]))
             utils.log_info("Cancel job %s"%(JOBID))
             utils.run_command("glite-wms-job-cancel --noint %s >> %s"%(JOBID,utils.get_tmp_file()))
             raise GeneralError("Check destination CE","Error !!! Matching CE is not %s"%(dest_ce))
        else:
             utils.log_info("Matchmaking is ok , now wait job to finish")

    utils.wait_until_job_finishes (JOBID)
    get_mpi_job_output(utils,JOBID)
   


def get_normal_job_output(utils,jobid):

    utils.log_info("Try to get the output of the normal job")

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
                


def get_collection_job_output(utils,jobid):

   utils.log_info("Try to get the output of the collection job")

   status=utils.get_job_status(jobid)

   if status.find("Done") != -1 :

        utils.remove(utils.get_tmp_file())

        utils.log_info("Retrieve the collection output")

        utils.run_command("glite-wms-job-output --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid, utils.get_tmp_file()))

        utils.log_info("Check if the basic output directory exists")

        DIR=utils.run_command("grep '%s' %s"%(utils.get_tmp_dir(),utils.get_tmp_file()))

        if os.path.isdir(DIR):
              utils.log_info("Basic output directory exists")
        else:
              utils.log_info("ERROR: Basic output directory does not exist")
              raise GeneralError("Check output directory","Basic output directory does not exist")
   
        utils.log_info("Check if node directories are correctly created")

        if os.path.isdir("%s/Node_1_jdl"%(DIR)) & os.path.isdir("%s/Node_2_jdl"%(DIR)) & os.path.isdir("%s/Node_3_jdl"%(DIR)) :
              utils.log_info("Node directories are correctly created")
        else:
              utils.log_info("Node directories are not correctly created")
              raise GeneralError("Check output directories of the nodes","Node directories are not correctly created")

        utils.log_info("Check if the output files are correctly retrieved")

        if os.path.isfile("%s/Node_1_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_1_jdl/std.err"%(DIR)) & os.path.isfile("%s/Node_2_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_2_jdl/std.err"%(DIR)) & os.path.isfile("%s/Node_3_jdl/std.out"%(DIR)) & os.path.isfile("%s/Node_3_jdl/std.err"%(DIR))  :
              utils.log_info("All output files are correctly retrieved")
              
        else:
              utils.log_info("ERROR: Output files are not correctly retrieved")
              raise GeneralError("Check output files","Output files are not correctly retrieved")
  
   else:
        utils.log_info("ERROR: Job finishes with status: %s cannot retrieve output"%(status))
        raise GeneralError("Check final job status","Job finishes with status: %s cannot retrieve output"%(status))
   


def get_parametric_job_output(utils,jobid):

   utils.log_info("Try to get the output of the parametric job")

   status=utils.get_job_status(jobid)

   if status.find("Done") != -1 :

        utils.remove(utils.get_tmp_file())

        utils.log_info("Retrieve the parametric job output")

        utils.run_command("glite-wms-job-output --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid, utils.get_tmp_file()))

        utils.log_info("Check if the basic output directory exists")

        DIR=utils.run_command("grep '%s' %s"%(utils.get_tmp_dir(),utils.get_tmp_file()))

        if os.path.isdir(DIR):
             utils.log_info("Basic output directory exists")
        else:
             utils.log_info("ERROR: Basic output directory does not exist")
             raise GeneralError("Check output directory","Basic output directory does not exist")
         
        utils.log_info("Check if node directories are correctly created")

        if os.path.isdir("%s/Node_1"%(DIR)) & os.path.isdir("%s/Node_3"%(DIR)) & os.path.isdir("%s/Node_5"%(DIR)) & os.path.isdir("%s/Node_7"%(DIR)) & os.path.isdir("%s/Node_9"%(DIR)) :
             utils.log_info("Node directories are correctly created")
        else:
             utils.log_info("ERROR: Node directories are not correctly created")
             raise GeneralError("Check output directories of the nodes","Node directories are not correctly created")
            
        utils.log_info("Check if the output files are correctly retrieved")

        if os.path.isfile("%s/Node_1/output1.txt"%(DIR)) & os.path.isfile("%s/Node_1/error1.txt"%(DIR)) & os.path.isfile("%s/Node_3/output3.txt"%(DIR)) & os.path.isfile("%s/Node_3/error3.txt"%(DIR)) & os.path.isfile("%s/Node_5/output5.txt"%(DIR)) & os.path.isfile("%s/Node_5/error5.txt"%(DIR)) & os.path.isfile("%s/Node_7/output7.txt"%(DIR)) & os.path.isfile("%s/Node_7/error7.txt"%(DIR)) &  os.path.isfile("%s/Node_9/output9.txt"%(DIR)) & os.path.isfile("%s/Node_9/error9.txt"%(DIR))  :
              utils.log_info("Output files are correctly retrieved")
        else:
              utils.log_info("ERROR: Output files are not correctly retrieved")
              raise GeneralError("Check output files","Output files are not correctly retrieved")
              
   else:
        utils.log_info("ERROR: Job finishes with status: %s cannot retrieve output"%(status))
        raise GeneralError("Check job final status","Job finishes with status: %s cannot retrieve output"%(status))
           


def get_dag_job_output(utils,jobid):

  
   utils.log_info("Try to get the output of the DAG job")

   status=utils.get_job_status(jobid)

   if status.find("Done") != -1 :

        utils.remove(utils.get_tmp_file())

        utils.log_info("Retrieve the DAG job output")

        utils.run_command("glite-wms-job-output --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid, utils.get_tmp_file()))

        utils.log_info("Check if the basic output directory exists")

        DIR=utils.run_command("grep '%s' %s"%(utils.get_tmp_dir(),utils.get_tmp_file()))

        if os.path.isdir(DIR):
             utils.log_info("Basic output directory exists")
        else:
             utils.log_info("ERROR: Basic output directory does not exist")
             raise GeneralError("Check output directory","Basic output directory does not exist")
        
        utils.log_info("Check if node directories are correctly created")

        if os.path.isdir("%s/nodeA"%(DIR)) & os.path.isdir("%s/nodeB"%(DIR)) & os.path.isdir("%s/nodeC"%(DIR)) :
             utils.log_info("Node directories are correctly created")
        else:
             utils.log_info("ERROR: Node directories are not correctly created")
             raise GeneralError("Check output directories of the nodes","Node directories are not correctly created")
              
        utils.log_info("Check if the output files are correctly retrieved")

        if os.path.isfile("%s/nodeA/std.out"%(DIR)) & os.path.isfile("%s/nodeA/std.err"%(DIR)) & os.path.isfile("%s/nodeB/std.out"%(DIR)) & os.path.isfile("%s/nodeB/std.err"%(DIR)) & os.path.isfile("%s/nodeC/std.out"%(DIR)) & os.path.isfile("%s/nodeC/std.err"%(DIR)) :
              utils.log_info("Output files are correctly retrieved")
        else:
              utils.log_info("ERROR: Output files are not correctly retrieved")
              raise GeneralError("Check output files","Output files are not correctly retrieved")

   else:
        utils.log_info("ERROR: Job finishes with status: %s cannot retrieve output"%(status))
        raise GeneralError("Check job final status","Job finishes with status: %s cannot retrieve the output"%(status))
           


def get_mpi_job_output(utils,jobid):

   utils.log_info("Try to get the output of the MPI job")

   status=utils.get_job_status(jobid)

   if status.find("Done") != -1 :

        utils.remove(utils.get_tmp_file())

        utils.log_info("Retrieve the output")

        utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s >> %s"%(utils.get_job_output_dir(),jobid, utils.get_tmp_file()))

        utils.log_info("Check if the output files are correctly retrieved")

        if os.path.isfile("%s/hello.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/hello.err"%(utils.get_job_output_dir())) :
              utils.log_info("Output files are correctly retrieved")
        else:
              utils.log_info("ERROR: Output files are not correctly retrieved")
              raise GeneralError("Check output files","Output files are not correctly retrieved")
 
   else:
         utils.error("Job finishes with status: %s cannot retrieve output"%(status))
         raise GeneralError("Check job final status","Job finishes with status: %s cannot retrieve output"%(status))
     


   
