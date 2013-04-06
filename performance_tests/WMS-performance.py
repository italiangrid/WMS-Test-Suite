#! /usr/bin/python

import sys
import signal
import traceback
import time

import Performance_utils

from Exceptions import *

def execute_performance_test(utils):

    """
        Implements performance test logic:
            (a): Submit a compound job
            (b): Wait until compound job finished
            (c): Calculate statistics based on the final status of all nodes

        Argument: Performance_utils Object

        Return: 0 on success , 1 on failure 

    """

    utils.info("Start performance test")

    try:

        utils.info("Submit compound job")

        JOBID = utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Job submitted. JOBID: %s"%(JOBID))

        node_ids = utils.get_from_coumpound_job_all_nodes_ids(JOBID)

        utils.info("Wait until sumbitted job finished")

        utils.wait_until_job_finishes(JOBID)

        calculate_statistics(utils,JOBID,node_ids)
        
    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("WMS Performance Test")
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("WMS Performance Test")
        utils.log_traceback(traceback.format_exc())
        utils.exit_failure(e.message)
        return 1

    return 0


def calculate_statistics(utils,jobid,node_ids):

    """
       Calculate various statistics for the performance test
    
       Arguments:
            - Performance_utils Object
            - Compound job id
            - List with ids for all nodes in the compound job

    """

    utils.info("Compute statistics for compound job %s"%(jobid))

    Aborted=[]
    Aborted_reason=[]
    Cancelled=[]
    Cancelled_reason=[]
    Done=[]
    Failed=[]
    Failed_reason=[]
    Other=[]
    Other_reason=[]

    start_time=time.mktime(time.strptime(utils.START_TIME,"%d/%m/%Y %H:%M:%S"))

    end_time=time.time()

    for id in node_ids:

        status=utils.get_job_status(id)

        if status.find('Done (Success)') != -1 or status.find('Done(Success)') != -1 :
            Done.append(id)
        elif status.find('Done (Failed)') != -1 or status.find('Done(Failed)') != -1 :
            Failed.append(id)
        elif status.find("Aborted")!=-1:
            Aborted.append(id)
        elif status.find("Cancelled")!=-1:
            Cancelled.append(id)
        else:
            Other.append(id)

    total=len(node_ids)

    c_done=len(Done)
    p_done=(float(c_done)/total)*100

    c_failed=len(Failed)
    p_failed=(float(c_failed)/total)*100

    c_aborted=len(Aborted)
    p_aborted=(float(c_aborted)/total)*100

    c_cancelled=len(Cancelled)
    p_cancelled=(float(c_cancelled)/total)*100

    c_other=len(Other)
    p_other=(float(c_other)/total)*100

    for i in range(c_aborted):
        Aborted_reason.append(utils.get_job_status_reason(Aborted[i]))
        
    for i in range(c_failed):
        Failed_reason.append(utils.get_job_status_reason(Failed[i]))

    for i in range(c_cancelled):
        Cancelled_reason.append(utils.get_job_status_reason(Cancelled[i]))

    for i in range(c_other):
        Other_reason.append(utils.get_job_status_reason(Other[i]))

    utils.print_statistics("")
    utils.print_statistics("======================================= Statistics =======================================")
    utils.print_statistics("")
    utils.print_statistics("Compound Job id: %s"%(jobid))
    utils.print_statistics("")
    utils.print_statistics("Total Execution Time: %s secs"%(int(end_time-start_time)))
    utils.print_statistics("")
    utils.print_statistics("Cancelled:  %s\t - %s %% "%(c_cancelled,p_cancelled))
    utils.print_statistics("Aborted:    %s\t - %s %% "%(c_aborted,p_aborted))
    utils.print_statistics("Done:       %s\t - %s %% "%(c_done,p_done))
    utils.print_statistics("Failed:     %s\t - %s %% "%(c_failed,p_failed))
    utils.print_statistics("Other:      %s\t - %s %% "%(c_other,p_other))
    utils.print_statistics("")
    utils.print_statistics("==========================================================================================")
    utils.print_statistics("")
    utils.print_statistics("")
    utils.print_statistics("=================== Details for nodes with status Failed,Aborted,Other ===================")

    for i in range(c_failed):
        utils.print_statistics("Node id: %s , status: Failed , reason: %s"%(Failed[i],Failed_reason[i]))

    for i in range(c_aborted):
        utils.print_statistics("Node id: %s , status: Aborted , reason: %s"%(Aborted[i],Aborted_reason[i]))

    for i in range(c_other):
        utils.print_statistics("Node id: %s , status: Other , reason: %s"%(Other[i],Other_reason[i]))

    utils.print_statistics("==========================================================================================")
    utils.print_statistics("")
    utils.print_statistics("")
    
    utils.exit_success()

    

def main():

    """
        The main function , creates basic object (Performance_utils) and starts test execution
    """

    utils = Performance_utils.Performance_utils(sys.argv[0],"Performance testing for WMS service")

    utils.prepare(sys.argv[1:])

    utils.info("Performance testing for WMS service")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    execute_performance_test(utils)
        
if __name__ == "__main__":
    main()

