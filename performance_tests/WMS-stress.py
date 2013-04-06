#! /usr/bin/python

"""
    Note:
    
    Mutliprocess part is based on the CREAM stress test suite [ https://twiki.cern.ch/twiki/bin/view/EMI/CREAMStressTests ]
    written by Dimosthenes Fioretos dfiore -at- noc -dot- uoa -dot- gr
        
"""

import os
import os.path
import sys
import signal
import time
import pwd

import Stress_utils
from Exceptions import *

from multiprocessing import Array, Process, Lock, Value, Queue, queues
import multiprocessing

class sync_queue(multiprocessing.queues.Queue):
        
        def __init__(self):
                self.q = Queue()
                self.lock = Lock()

        def add(self, item):
                self.lock.acquire()
                self.q.put(item)
                self.lock.release()

        def remove(self):
                return self.q.get()


def manager(var_lock,queue,stress_utils,totally_submitted_jobs):

    """
         method that executed by manager process
    """

    pids = []

    submitted = []
    done_success = []
    failed = []
    cleared = []
    exit_code_not_0 = []
    cancelled = []
    aborted = []
    unknown = []
    running = []
    submit_failed = []
    query_status_failed  = []
    
    destination_ces = []

    status_reasons = []

    exceptions = []

    start_time = time.time()

    while True:

        if len(exceptions) == int(stress_utils.USERS):

            var_lock.acquire()

            for exception in exceptions:
                stress_utils.myecho(exception,"error")

            var_lock.release()

            stress_utils.exit_failure("All submission process failed")
        
        message = queue.remove()

        if message[0] == "pid":
            pids.append(message[1])
            continue

        if message[0] == "destination-ce":
            destination_ces.append(message[1])
            continue

        if message[0] == "status-reason":
            status_reasons.append(message[1])
            continue

        if message[1] == "EXCEPTION":
            exceptions.append(message[2])
            continue
        else:
            
            if message[1] == 'submitted':
                submitted.append(message[0])
                running.append(message[0])
            elif message[1] == 'cancelled':
                cancelled.append(message[0])
            elif message[1] == 'done-success':
                done_success.append(message[0])
            elif message[1] == 'failed':
                failed.append(message[0])
            elif message[1] == 'aborted':
                aborted.append(message[0])
            elif message[1] == 'cleared':
                cleared.append(message[0])
            elif message[1] == 'exit-code-not-0':
                exit_code_not_0.append(message[0])
            elif message[1] == 'query_status_failed':
                query_status_failed.append(message[0])
            elif message[1] == 'submit_failed':
                submit_failed.append(message[0])
            elif message[1] == 'unknown':
                unknown.append(message[0])
            else:
                var_lock.acquire()
                stress_utils.myecho("Job %s has invalid state '%s'"%(message[0],message[1]),"error")
                var_lock.release()

            if message[1] in ['cancelled','done-success','failed','aborted','cleared']:
                if message[0] in running:
                   running.remove(message[0])

        finished_jobs = len(cancelled)+len(done_success)+len(failed)+len(aborted)+len(query_status_failed)+len(submit_failed)+len(cleared)+len(exit_code_not_0)+len(unknown)

        message = "\n=============================================================================="
        message += "\n\n Submitted: %s \t Running: %s \t Done Success: %s \t Cleared: %s"%(len(submitted),len(running),len(done_success),len(cleared))
        message += "\n Failed: %s \t Exit Code !=0 : %s \t Cancelled: %s \t Aborted: %s"%(len(failed),len(exit_code_not_0),len(cancelled),len(aborted))
        message += "\n Unknown: %s \t Failed Submissions: %s \t Query Status Failed: %s"%(len(unknown),len(submit_failed),len(query_status_failed))
        message += "\n\n Finished Jobs: %s / %s"%(finished_jobs,totally_submitted_jobs)
        message += "\n\n=============================================================================="

        var_lock.acquire()
        stress_utils.myecho(message)
        var_lock.release()

        if finished_jobs == totally_submitted_jobs:

            end_time = time.time()

            for pid in pids:
                while os.path.exists('/proc/'+str(pid)):
                    pass

            c_done = len(done_success)
            p_done = (float(c_done)/totally_submitted_jobs)*100

            c_cleared = len(cleared)
            p_cleared = (float(c_cleared)/totally_submitted_jobs)*100

            c_failed = len(failed)
            p_failed = (float(c_failed)/totally_submitted_jobs)*100

            c_aborted = len(aborted)
            p_aborted = (float(c_aborted)/totally_submitted_jobs)*100

            c_cancelled = len(cancelled)
            p_cancelled = (float(c_cancelled)/totally_submitted_jobs)*100

            c_exit_code_not_0 = len(exit_code_not_0)
            p_exit_code_not_0 = (float(c_exit_code_not_0)/totally_submitted_jobs)*100

            c_submit_failed = len(submit_failed)
            p_submit_failed = (float(c_submit_failed)/totally_submitted_jobs)*100

            c_query_status_failed = len(query_status_failed)
            p_query_status_failed = (float(c_query_status_failed)/totally_submitted_jobs)*100

            c_unknown = len(unknown)
            p_unknown = (float(c_unknown)/totally_submitted_jobs)*100

            lcg_ce = 0
            cream = 0
            arc_ce = 0
            
            for ce in destination_ces:
              
              if ce.find("2119/jobmanager")!=-1:
                  lcg_ce += 1
              elif ce.find("/cream-")!=-1:
                  cream += 1
              elif ce.find("/nordugrid")!=-1:
                  acr_ce += 1

            p_lcg_ce = (float(lcg_ce)/totally_submitted_jobs)*100
            p_cream = (float(cream)/totally_submitted_jobs)*100
            p_arc_ce = (float(arc_ce)/totally_submitted_jobs)*100

            stress_utils.print_stats("")
            stress_utils.print_stats("=========================== STATISTICS ===========================")
            stress_utils.print_stats("")
            stress_utils.print_stats(" Total Jobs: %s"%(totally_submitted_jobs))
            stress_utils.print_stats("")
            stress_utils.print_stats(" Total Execution Time: %s secs"%(int(end_time-start_time)))
            stress_utils.print_stats("")
            stress_utils.print_stats(" Done Success:         %s - %s %% "%(c_done,p_done))
            stress_utils.print_stats(" Cleared:              %s - %s %% "%(c_cleared,p_cleared))
            stress_utils.print_stats(" Failed:               %s - %s %% "%(c_failed,p_failed))
            stress_utils.print_stats(" Aborted:              %s - %s %% "%(c_aborted,p_aborted))
            stress_utils.print_stats(" Cancelled:            %s - %s %% "%(c_cancelled,p_cancelled))
            stress_utils.print_stats(" Exit Code !=0 :       %s - %s %% "%(c_exit_code_not_0,p_exit_code_not_0))
            stress_utils.print_stats(" Failed Submissions:   %s - %s %% "%(c_submit_failed,p_submit_failed))
            stress_utils.print_stats(" Failed Query Status:  %s - %s %% "%(c_query_status_failed,p_query_status_failed))
            stress_utils.print_stats(" Unknown Final Status: %s - %s %% "%(c_unknown,p_unknown))
            stress_utils.print_stats("")
            stress_utils.print_stats("==================================================================")
            stress_utils.print_stats("")
            stress_utils.print_stats("==================== JOBS DISTRIBUTION TO CES ====================")
            stress_utils.print_stats("")
            stress_utils.print_stats(" LCG-CE:  %s - %s %%"%(lcg_ce,p_lcg_ce))
            stress_utils.print_stats(" CREAM:   %s - %s %%"%(cream,p_cream))
            stress_utils.print_stats(" ARC:     %s - %s %%"%(arc_ce,p_arc_ce))
            stress_utils.print_stats("")
            stress_utils.print_stats("==================================================================")
            stress_utils.print_stats("")
            stress_utils.print_stats("============ STATUS REASON FOR ABORTED AND FAILED JOBS ===========")
            stress_utils.print_stats("")

            for i in range(len(status_reasons)):
                stress_utils.print_stats(" Job: %s - Reason: %s"%(status_reasons[i]["jobid"],status_reasons[i]["reason"]))

            stress_utils.print_stats("")
            stress_utils.print_stats("==================================================================")
            
            stress_utils.exit_success()
        
        
def submit(var_lock,queue,stress_utils,user_index,username,jobs_left):

    """
         method that executed by submitter process 
    """

    try:

          #Ids for jobs submitted by the process
          ids = []

          #get new process id and send it to the manager
          my_pid = str(os.getpid())
          queue.add(['pid',my_pid])

          #Get user details from his username
          pw_record = pwd.getpwnam(username)

          #Set group and user id for new process
          os.setgid(pw_record.pw_gid)
          os.setuid(pw_record.pw_uid)

          #Set user environment variable for new process
          os.environ['USER'] = username

          #Proxy file
          proxy = "%s/proxy.file"%(pw_record.pw_dir)

          #Create voms certificate
          stress_utils.run_command_continue_on_error("echo %s | voms-proxy-init -voms %s -cert %s/.globus/usercert.pem -key %s/.globus/userkey.pem -verify -valid 24:00 -bits 1024 -pwstdin -out %s"%(stress_utils.PASSWORDS[user_index],stress_utils.VOS[user_index],pw_record.pw_dir,pw_record.pw_dir,proxy))

          #Update X509_USER_PROXY environment variable
          os.environ['X509_USER_PROXY'] = proxy
          
          var_lock.acquire()

          stress_utils.info("Setup submitter process %s"%(my_pid))

          jdl_file = stress_utils.get_jdl_file()

          #Create configuration file
          config_file = stress_utils.set_conf(user_index)

          #Create delegation
          delegation = stress_utils.set_delegation(config_file)

          #Create job output directory
          output_dir = stress_utils.get_job_output_dir(user_index)

          sleep_time = int(stress_utils.SLEEP_TIME)

          stress_utils.info("Process %s starts submitting jobs"%(my_pid))

          var_lock.release()

          while True:
              
            var_lock.acquire()

            if jobs_left.value == 0 and len(ids) == 0:
                
                    stress_utils.info("Process %s terminating, no jobs left to submit or collect"%(my_pid))
                    var_lock.release()
                    sys.exit(0)

            else:    

                    var_lock.release()

                    while True:
                    
                        var_lock.acquire()
                        
                        if jobs_left.value == 0: 
                                var_lock.release()
                                break
                        else:

                                jobs_left.value = jobs_left.value-1
                                
                                var_lock.release()
                              
                        JOBID =  submit_job(stress_utils,jdl_file,config_file,delegation,var_lock,queue)

                        if JOBID == None:
                              continue
                        else:

                              if stress_utils.JOB_TYPE.lower().find("normal") !=- 1:
                                   ids.append(JOBID)
                              else:

                                   node_ids = query_node_ids(stress_utils,JOBID,var_lock)
                                   if node_ids ==None:
                                       continue
                                   else:
                                       for node_id in node_ids:
                                        ids.append(node_id)


                    time.sleep(sleep_time)
                    
                    for jobid in ids:

                        (status_code,status) = query_job_status(stress_utils,jobid,output_dir,var_lock,queue)

                        if status_code != None and status_code !=0:

                                destination_ce = query_destination_ce(stress_utils,jobid,var_lock)

                                queue.add(["destination-ce",destination_ce])
                            
                                if status_code == 1:
                                        queue.add([jobid,'done-success'])
                                elif status_code == 2:
                                        queue.add([jobid,'aborted'])
                                        status_reason = query_status_reason(stress_utils,jobid,var_lock)
                                        queue.add(["status-reason",{"jobid":jobid,"reason":status_reason}])
                                elif status_code == 3:
                                        queue.add([jobid,'cancelled'])
                                elif status_code == 4:
                                        queue.add([jobid,'exit-code-not-0'])
                                elif status_code == 5:
                                        queue.add([jobid,'cleared'])
                                elif status_code == 6:
                                        queue.add([jobid,'failed'])
                                        status_reason = query_status_reason(stress_utils,jobid,var_lock)
                                        queue.add(["status-reason",{"jobid":jobid,"reason":status_reason}])
                                else:
                                        queue.add([jobid,'unknown'])

                                ids.remove(jobid)

                                    
    except (RunCommandError,GeneralError,TimeOutError), e:
            queue.add(["MESSAGE","EXCEPTION","%s - %s"%(e.expression,e.message)])
            var_lock.acquire()
            stress_utils.myecho("ERROR: %s - %s"%(e.expression,e.message),"error")
            var_lock.release()
            sys.exit(1)



def submit_job(stress_utils,jdl_file,config_file,delegation,var_lock,queue):

    """
         submit job, method which implement fault tolerance and reporting
    """

    limit_retries = 3
    
    successful = False

    for i in range(limit_retries):

       try:

             jobid = stress_utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(delegation,config_file,jdl_file))
             successful = True
             break

       except (RunCommandError,GeneralError,TimeOutError), e:
             time.sleep(5)

    if successful == False:

          var_lock.acquire()
          stress_utils.myecho("Submit operation failed: %s - %s "%(e.expression,e.message),"error")
          var_lock.release()

          queue.add(['not-available','submit-failed'])

          return None

    else:

          var_lock.acquire()
          stress_utils.myecho("%s job submitted. Jod Id: %s"%(stress_utils.JOB_TYPE,jobid),"info")
          var_lock.release()

          if stress_utils.JOB_TYPE.lower().find("normal") !=- 1:
                queue.add([jobid,'submitted'])                       
          else:
                node_ids = query_node_ids(stress_utils,jobid,var_lock)

                for node_id in node_ids:
                    queue.add([node_id,'submitted'])
        
          return jobid


def query_job_status(stress_utils,jobid,output_dir,var_lock,queue):

    """
         Return job status, method which implement fault tolerance and reporting
    """

    limit_retries = 3

    successful = False

    for i in range(limit_retries):

       try:

             status_code = stress_utils.job_is_finished(jobid)

             status = stress_utils.get_job_status(jobid)

             successful = True

             break

       except (RunCommandError,GeneralError,TimeOutError), e:
             time.sleep(5)

    if successful == False:

          var_lock.acquire()
          stress_utils.myecho("Unable to get status for job: %s "%(jobid),"error")
          stress_utils.myecho("Details: %s - %s "%(e.expression,e.message),"error")
          var_lock.release()

          queue.add([jobid,'query-status-failed'])

          return (None,None)

    else:
        
          return (int(status_code),status)


def query_destination_ce(stress_utils,jobid,var_lock):

    """
         Return destination CE, method which implement fault tolerance and reporting
    """

    limit_retries = 3

    successful = False

    for i in range(limit_retries):

       try:

             ce = stress_utils.get_destination_ce(jobid)
             
             successful = True

             break

       except (RunCommandError,GeneralError,TimeOutError), e:
             time.sleep(5)

    if successful == False:

          var_lock.acquire()
          stress_utils.myecho("Unable to get destination ce for job: %s "%(jobid),"error")
          stress_utils.myecho("Details: %s - %s "%(e.expression,e.message),"error")
          var_lock.release()
          
          return None

    else:
          return ce


def query_status_reason(stress_utils,jobid,var_lock):

    """
         Return job status reason, method which implement fault tolerance and reporting
    """

    limit_retries = 3

    successful = False

    for i in range(limit_retries):

       try:

             status_reason = stress_utils.get_job_status_reason(jobid)

             successful = True

             break

       except (RunCommandError,GeneralError,TimeOutError), e:
             time.sleep(5)

    if successful == False:

          var_lock.acquire()
          stress_utils.myecho("Unable to get status reason for job: %s "%(jobid),"error")
          stress_utils.myecho("Details: %s - %s "%(e.expression,e.message),"error")
          var_lock.release()

          return None

    else:
          return status_reason


def query_node_ids(stress_utils,jobid,var_lock):

    """
         Return node ids for a compound job, method which implement fault tolerance and reporting
    """

    limit_retries = 3

    successful = False

    for i in range(limit_retries):

       try:

             node_ids  = stress_utils.get_from_coumpound_job_all_nodes_ids(jobid)

             successful = True

             break

       except (RunCommandError,GeneralError,TimeOutError), e:
             time.sleep(5)

    if successful == False:

          var_lock.acquire()
          stress_utils.myecho("Unable to get node ids for job: %s "%(jobid),"error")
          stress_utils.myecho("Details: %s - %s "%(e.expression,e.message),"error")
          var_lock.release()

          return None

    else:
          return node_ids



def main():

    """
        the main function , creates basic object (Stress_utils) , setups multiprocess environment and
        starts test execution
        
    """    
    utils = Stress_utils.Stress_utils(sys.argv[0],"Stress testing for WMS service")

    utils.prepare(sys.argv[1:])

    utils.info("Stress testing for WMS service")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    ### Setup multiprocess enviroment 

    # Create process locks
    var_lock = Lock()

    # Shared Variable
    number_of_jobs = Value('i', int(utils.TOTAL_JOBS))

    #Initialize queue object
    queue = sync_queue()

    # Start test
    
    job_submitters=[]

    if utils.JOB_TYPE.lower().find("normal")!=-1:
        totally_submitted_jobs = int(utils.TOTAL_JOBS)
    else:
        totally_submitted_jobs = int(utils.TOTAL_JOBS)*int(utils.NODES_PER_JOB)
        
    #Create manager process - orchestrate test , collect statistical data
    p=Process(target=manager, args=(var_lock,queue,utils,totally_submitted_jobs))
    job_submitters.append(p)
    p.start()

    #Create submission process
    for i in range(int(utils.USERS)):
        p=Process(target=submit,args=(var_lock,queue,utils,i,utils.USERNAMES[i],number_of_jobs))
        job_submitters.append(p)
        p.start()

    #Wait until all procs have been terminated
    active_procs = multiprocessing.active_children()

    while ( len(active_procs) > 0 ):
            active_procs = multiprocessing.active_children()
            time.sleep(10)
    
            
        
if __name__ == "__main__":
    main()

