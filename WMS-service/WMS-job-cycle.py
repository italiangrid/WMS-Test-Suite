#! /usr/bin/python

import sys
import signal
import os
import glob
import time
import traceback

import Test_utils
import Job_utils

from Exceptions import *

def normal_submit(utils, title):

    fails=0

    utils.show_progress(title)
    utils.info(title)

    utils.show_progress("Test 1A: Submit to an LCG-CE")
    utils.info("\tTest 1A: Submit to an LCG-CE")

    Job_utils.prepare_normal_job(utils,utils.get_jdl_file(),"2119/jobmanager")

    result=Job_utils.submit_only_normal_job(utils,"2119/jobmanager")

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))

    utils.show_progress("Test 1B: Submit to a CREAM CE")
    utils.info("\tTest 1B: Submit to a CREAM CE")

    Job_utils.prepare_normal_job(utils,utils.get_jdl_file(),"/cream-")

    result=Job_utils.submit_normal_job(utils,"/cream-")

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))

    utils.show_progress("Test 1C: Submit without restrictions")
    utils.info("\tTest 1C: Submit without restrictions")

    Job_utils.prepare_normal_job(utils,utils.get_jdl_file())

    result=Job_utils.submit_normal_job(utils)

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))

    return fails

def bulk_submit(utils, title):

    fails=0
    
    utils.show_progress(title)
    utils.info(title)

    utils.show_progress("Test 2A: Submit to an LCG-CE")
    utils.info("\tTest 2A: Submit to an LCG-CE")    

    Job_utils.prepare_collection_job(utils,utils.get_jdl_file(),"2119/jobmanager")

    result=Job_utils.submit_collection_job(utils,"2119/jobmanager")

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))
        utils.dbg("Clean collection's jdl files")
        os.system("rm -rf %s/collection_jdls/"%(utils.get_tmp_dir()))

    utils.show_progress("Test 2B: Submit to a CREAM CE")
    utils.info("\tTest 2B: Submit to a CREAM CE")

    Job_utils.prepare_collection_job(utils,utils.get_jdl_file(),"/cream-")

    result=Job_utils.submit_collection_job(utils,"/cream-")

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))
        utils.dbg("Clean collection's jdl files")
        os.system("rm -rf %s/collection_jdls/"%(utils.get_tmp_dir()))

    utils.show_progress("Test 2C: Submit without restrictions")
    utils.info("\tTest 2C: Submit without restrictions")

    Job_utils.prepare_collection_job(utils,utils.get_jdl_file())

    result=Job_utils.submit_collection_job(utils)

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))
        utils.dbg("Clean collection's jdl files")
        os.system("rm -rf %s/collection_jdls/"%(utils.get_tmp_dir()))    
    
    return fails


def bulk_submit_with_single_jdl(utils, title):

    fails=0

    utils.show_progress(title)
    utils.info(title)

    utils.show_progress("Test 7A: Submit to an LCG-CE")
    utils.info("\tTest 7A: Submit to an LCG-CE")


    Job_utils.prepare_single_jdl_for_collection_job(utils,utils.get_jdl_file(),"2119/jobmanager")

    result=Job_utils.submit_collection_job(utils,"2119/jobmanager",True)

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))
        
    utils.show_progress("Test 7B: Submit to a CREAM CE")
    utils.info("\tTest 7B: Submit to a CREAM CE")

    Job_utils.prepare_single_jdl_for_collection_job(utils,utils.get_jdl_file(),"/cream-")

    result=Job_utils.submit_collection_job(utils,"/cream-",True)

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))
     

    utils.show_progress("Test 7C: Submit without restrictions")
    utils.info("\tTest 7C: Submit without restrictions")

    Job_utils.prepare_single_jdl_for_collection_job(utils,utils.get_jdl_file())

    result=Job_utils.submit_collection_job(utils,"",True)

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))
        
    return fails
    
    
def parametric_submit(utils, title):

    fails=0
    
    utils.show_progress(title)
    utils.info(title)

    utils.show_progress("Test 3A: Submit to an LCG-CE")
    utils.info("\tTest 3A: Submit to an LCG-CE")     

    Job_utils.prepare_parametric_job(utils,utils.get_jdl_file(),"2119/jobmanager")

    result=Job_utils.submit_parametric_job(utils,"2119/jobmanager")

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))

    utils.show_progress("Test 3B: Submit to a CREAM CE")
    utils.info("\tTest 3B: Submit to a CREAM CE")

    Job_utils.prepare_parametric_job(utils,utils.get_jdl_file(),"/cream-")

    result=Job_utils.submit_parametric_job(utils,"/cream-")

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))

    utils.show_progress("Test 3C: Submit without restrictions")
    utils.info("\tTest 3C: Submit without restrictions")

    Job_utils.prepare_parametric_job(utils,utils.get_jdl_file())

    result=Job_utils.submit_parametric_job(utils)

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))   

    return fails
    
def dag_submit(utils, title):

    # Dag jobs can be submitted only to LCG-CE

    utils.show_progress(title)
    utils.info(title)

    Job_utils.prepare_dag_job(utils,utils.get_jdl_file())

    result=Job_utils.submit_dag_job(utils)

    if result[0] == 1 :
        utils.info(result[1])
        return 1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))
    
    return 0
        
def parallel_submit(utils, title):

    fails=0

    utils.show_progress(title)
    utils.info(title)

    utils.show_progress("Test 5A: Submit to an LCG-CE")
    utils.info("\tTest 5A: Submit to an LCG-CE")   

    Job_utils.prepare_mpi_job(utils,utils.get_jdl_file(),"2119/jobmanager")

    result=Job_utils.submit_mpi_job(utils,"2119/jobmanager")

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))
        
    utils.show_progress("Test 5B: Submit to a CREAM CE")
    utils.info("\tTest 5B: Submit to a CREAM CE")

    Job_utils.prepare_mpi_job(utils,utils.get_jdl_file(),"/cream-")

    result=Job_utils.submit_mpi_job(utils,"/cream-")

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))

    utils.show_progress("Test 5C: Submit without restrictions")
    utils.info("\tTest 5C: Submit without restrictions")

    Job_utils.prepare_mpi_job(utils,utils.get_jdl_file())

    result=Job_utils.submit_mpi_job(utils)

    if result[0] == 1 :
        utils.info(result[1])
        fails=fails+1
    else:
        utils.dbg("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))

    return fails


def perusal_submit_test(utils,target):

    ret=[0,""]

    try:

        utils.set_perusal_jdl(utils.get_jdl_file())

        utils.set_destination_ce(utils.get_jdl_file(),target)

        JOBID=utils.run_command ("glite-wms-job-submit %s --nomsg -c %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.dbg("Job %s has been submitted"%(JOBID))

        utils.run_command_continue_on_error ("glite-wms-job-perusal --set --filename out.txt -f std.out %s"%(JOBID))

        utils.info("Wait until job's state is Running")

        utils.job_status(JOBID)

        while utils.get_job_status().find("Running")==-1 and utils.job_is_finished(JOBID)==0:
           time.sleep(30)
           utils.job_status(JOBID)

        utils.info("Wait for 1010 secs")

        time.sleep(1010)

        utils.run_command_continue_on_error ("glite-wms-job-perusal --get -f out.txt --dir %s %s"%(utils.get_job_output_dir(),JOBID))

        utils.info("Check if some chunkes have been retrieved")

        filespec="out.txt-*"

        first_try_chunk=glob.glob(os.path.join(utils.get_job_output_dir(),filespec))

        if len(first_try_chunk):
            utils.info("These chunks have been retrieved: %s"%(first_try_chunk))
        else:
            utils.error("TEST FAILS. No chunks have been retrieved")
            raise GeneralError("glite-wms-job-perusal --get","No chunks have been retrieved.")

        #first_try_size=os.stat(first_try_chunk[0]).st_size

        utils.info("Wait for another 1010 secs")

        time.sleep(1010)

        utils.run_command_continue_on_error ("glite-wms-job-perusal --get -f out.txt --dir %s %s"%(utils.get_job_output_dir(),JOBID))

        utils.info("Check if some chunks have been retrieved")

        second_try_chunk=glob.glob(os.path.join(utils.get_job_output_dir(),filespec))

        if len(second_try_chunk)>len(first_try_chunk):
            utils.info("These chunks have been retrieved: %s"%(second_try_chunk))
        else:
            utils.error("TEST FAILS. No chunks have been retrieved")
            raise GeneralError("glite-wms-job-perusal --get","No chunks have been retrieved.")

        second_try_chunk.remove(first_try_chunk[0])

        #second_try_size=os.stat(second_try_chunk[0]).st_size


    except (GeneralError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        ret[0]=1
        ret[1]=e.message
        return ret

    return ret



def perusal_submit(utils, title):

    utils.show_progress(title)
    utils.info(title)

    fails=0

    try:

        utils.info("CASE A: Use LCG CE")
        utils.show_progress("CASE A: Use LCG CE")
 
        result=perusal_submit_test(utils,"2119/jobmanager")

        if result[0] == 1 :
           fails=fails+1
           utils.error(result[1])
        else:
           utils.info("TEST CASE OK")
           utils.dbg("Clean job output directory")
           os.system("rm -rf %s"%(utils.get_job_output_dir()))

        utils.info("CASE B: Use CREAM CE")
        utils.show_progress("CASE B: Use CREAM CE")

        result=perusal_submit_test(utils,"/cream-")

        if result[0] == 1 :
           fails=fails+1
           utils.error(result[1])
        else:
           utils.info("TEST CASE OK")
           utils.dbg("Clean job output directory")
           os.system("rm -rf %s"%(utils.get_job_output_dir()))


    except (GeneralError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return fails
        
    return fails


def forward_parameters_parallel_jobs(utils, title):

    fails=0

    utils.show_progress(title)
    utils.info(title)

    try:

        utils.show_progress("Test 8: Case 1")
        utils.info("\tTest 8: Case 1")

        Job_utils.prepare_mpi_job(utils,utils.get_jdl_file(),"/cream-")

        utils.change_jdl_attribute("CpuNumber","2")
        utils.add_jdl_general_attribute("WholeNodes","true")
        utils.add_jdl_general_attribute("SMPGranularity","2")
        utils.add_jdl_general_attribute("Hostnumber","1")

        check=['CpuNumber = 2','WholeNodes = true','SMPGranularity = 2','Hostnumber = 1']

        errors=[]

        utils.info("Submit MPI job")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))
    
        utils.info("Wait until job transefered to CREAM CE")

        utils.wait_until_job_transfered(JOBID)
    
        cream_jobid=utils.get_cream_jobid(JOBID)

        utils.info("Get the resulting cream jdl")

        cream_jdl=utils.get_cream_jdl(cream_jobid)

        utils.info("Check the cream jdl for the forwarding parameters")

        for attribute in check:
            if cream_jdl.find(attribute)==-1:
                errors.append(attribute)


        if len(errors)>0:
            msg=' , '.join(errors)
            utils.error("Problem with the following parameters: %s"%(msg))
            fails=fails+1


        utils.show_progress("Test 8: Case 2")
        utils.info("\tTest 8: Case 2")

        Job_utils.prepare_mpi_job(utils,utils.get_jdl_file(),"/cream-")

        utils.change_jdl_attribute("CpuNumber","1")
        utils.add_jdl_general_attribute("WholeNodes","true")
        utils.add_jdl_general_attribute("SMPGranularity","2")

        check=['CpuNumber = 1','WholeNodes = true','SMPGranularity = 2']

        errors=[]

        utils.info("Submit MPI job")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        utils.info("Wait until job transefered to CREAM CE")

        utils.wait_until_job_transfered(JOBID)

        cream_jobid=utils.get_cream_jobid(JOBID)

        utils.info("Get the resulting cream jdl")

        cream_jdl=utils.get_cream_jdl(cream_jobid)

        utils.info("Check the cream jdl for the forwarding parameters")

        for attribute in check:
            if cream_jdl.find(attribute)==-1:
                errors.append(attribute)


        if len(errors)>0:
            msg=' , '.join(errors)
            utils.error("Problem with the following parameters: %s"%(msg))
            fails=fails+1
        

        utils.show_progress("Test 8: Case 3")
        utils.info("\tTest 8: Case 3")

        Job_utils.prepare_mpi_job(utils,utils.get_jdl_file(),"/cream-")

        utils.change_jdl_attribute("CpuNumber","3")
        utils.add_jdl_general_attribute("WholeNodes","false")
        utils.add_jdl_general_attribute("SMPGranularity","3")
        utils.add_jdl_general_attribute("Hostnumber","1")

        utils.info("Submit MPI job")

        message=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()),1)

        utils.info("Check the error message")

        if message.find("SMPGranularity and HostNumber are mutually exclusive when WholeNodes allocation is not requested: wrong combination of values")==-1:
           utils.error("Job failed reason: %s. Expected reason: SMPGranularity and HostNumber are mutually exclusive when WholeNodes allocation is not requested: wrong combination of values"%(message))
           fails=fails+1


        utils.show_progress("Test 8: Case 4")
        utils.info("\tTest 8: Case 4")

        Job_utils.prepare_mpi_job(utils,utils.get_jdl_file(),"/cream-")

        utils.change_jdl_attribute("CpuNumber","3")
        utils.add_jdl_general_attribute("WholeNodes","false")
        utils.add_jdl_general_attribute("SMPGranularity","3")

        check=['CpuNumber = 3','WholeNodes = false','SMPGranularity = 3']

        errors=[]

        utils.info("Submit MPI job")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        utils.info("Wait until job transefered to CREAM CE")

        utils.wait_until_job_transfered(JOBID)

        cream_jobid=utils.get_cream_jobid(JOBID)

        utils.info("Get the resulting cream jdl")

        cream_jdl=utils.get_cream_jdl(cream_jobid)

        utils.info("Check the cream jdl for the forwarding parameters")

        for attribute in check:
            if cream_jdl.find(attribute)==-1:
                errors.append(attribute)


        if len(errors)>0:
            msg=' , '.join(errors)
            utils.error("Problem with the following parameters: %s"%(msg))
            fails=fails+1


        utils.show_progress("Test 8: Case 5")
        utils.info("\tTest 8: Case 5")

        Job_utils.prepare_mpi_job(utils,utils.get_jdl_file(),"/cream-")
        utils.change_jdl_attribute("CpuNumber","8")
        utils.add_jdl_general_attribute("WholeNodes","true")
        utils.add_jdl_general_attribute("SMPGranularity","8")
        utils.add_jdl_general_attribute("Hostnumber","2")
        
        check=['CpuNumber = 8','WholeNodes = true','SMPGranularity = 8','Hostnumber = 2']

        errors=[]

        utils.info("Submit MPI job")

        JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        utils.info("Wait until job transefered to CREAM CE")

        utils.wait_until_job_transfered(JOBID)

        cream_jobid=utils.get_cream_jobid(JOBID)

        utils.info("Get the resulting cream jdl")

        cream_jdl=utils.get_cream_jdl(cream_jobid)

        utils.info("Check the cream jdl for the forwarding parameters")

        for attribute in check:
            if cream_jdl.find(attribute)==-1:
                errors.append(attribute)


        if len(errors)>0:
            msg=' , '.join(errors)
            utils.error("Problem with the following parameters: %s"%(msg))
            fails=fails+1

    except (GeneralError,RunCommandError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return fails

    return fails


def check_jdls_normal_job(utils, title):

    fails=0

     



def main():
    	
    utils = Test_utils.Test_utils(sys.argv[0],"Test a complete job cycle: from submission to get output")

    tests=["Set 1: Submit a normal job (3 cases LCG-CE, CREAM, general)"]
    tests.append("Set 2: Submit a bulk of jobs (3 cases LCG-CE, CREAM, general)")
    tests.append("Set 3: Submit a parametric job (3 cases LCG-CE, CREAM, general)")
    tests.append("Set 4: Submit a DAG job")
    tests.append("Set 5: Submit a MPI job (3 cases LCG-CE, CREAM, general)")
    tests.append("Set 6: Submit a perusal job (2 cases LCG-CE,CREAM)")
    tests.append("Set 7: Submit a bulk of jobs (3 cases LCG-CE, CREAM, general) using a single jdl with al the jdls of nodes")
    tests.append("Set 8: Testing forwarding parameters for parallel jobs")
    tests.append("Set 9: Check different jdls cases for normal job ( submission to LCG-CE and CREAM)")

    utils.prepare(sys.argv[1:],tests)

    utils.info("Test a complete job cycle: from submission to get output")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    fails=[]

    # This test is for direct submission to a given CE
    if utils.get_user_CE() !='' :
    
        utils.info ("Submit a normal job to %s"%(utils.get_user_CE()))

        Job_utils.prepare_normal_job(utils,utils.get_jdl_file(),utils.get_user_CE())
        
        result=Job_utils.submit_normal_job(utils,utils.get_user_CE())

        if result[0] == 1 :
            utils.warn(result[1])
            utils.log_error("Submit a normal job to %s"%(utils.get_user_CE()))
            utils.log_error(result[1])
            utils.exit_failure(result[1])

        utils.message("Clean job output directory")
        os.system("rm -rf %s"%(utils.get_job_output_dir()))
	
    else:
        
        all_tests=utils.is_all_enabled()

        if all_tests==1 or utils.check_test_enabled(1)==1 :
            if normal_submit(utils, tests[0]):
                fails.append(tests[0])
                
        if all_tests==1 or utils.check_test_enabled(2)==1 :
            if bulk_submit(utils, tests[1]):
               fails.append(tests[1])
        
        if all_tests==1 or utils.check_test_enabled(3)==1 :
            if parametric_submit(utils, tests[2]):
                fails.append(tests[2])
                
        if all_tests==1 or utils.check_test_enabled(4)==1 :
            if dag_submit(utils, tests[3]):
                fails.append(tests[3])
            
        if all_tests==1 or utils.check_test_enabled(5)==1 :
            if parallel_submit(utils, tests[4]):
                fails.append(tests[4])
                
        if all_tests==1 or utils.check_test_enabled(6)==1 :
            if perusal_submit(utils, tests[5]):
                fails.append(tests[5])

        if all_tests==1 or utils.check_test_enabled(7)==1 :
            if bulk_submit_with_single_jdl(utils, tests[6]):
                fails.append(tests[6])

        if all_tests==1 or utils.check_test_enabled(8)==1 :
            if forward_parameters_parallel_jobs(utils, tests[7]):
                fails.append(tests[7])

        if all_tests==1 or utils.check_test_enabled(9)==1 :
            if check_jdls_normal_job(utils, tests[8]):
                fails.append(tests[8])




    if len(fails) > 0 :
      utils.exit_failure("%s test(s) fail(s): %s"%(len(fails), fails))
    else:
      utils.exit_success()


if __name__ == "__main__":
    main()
