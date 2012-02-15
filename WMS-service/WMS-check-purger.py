#! /usr/bin/python

import sys
import signal
import traceback
import datetime
import time

from Exceptions import *

import Test_utils
import Job_utils
import SSH_utils


def test1(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        Job_utils.prepare_normal_job(utils,utils.get_jdl_file(),"2119/jobmanager")

        utils.info("Submit a job to a LCG CE")

        JOBID=Job_utils.submit_only_normal_job(utils,"2119/jobmanager")[1]

        utils.info("Check the SBD and the others file used by the services")

        prefix=JOBID.split("https://%s:9000/"%(utils.get_WMS()))[1][0:2]

        dir2="/var/jobcontrol/condorio/%s"%(prefix)

        utils.info("Check files at %s"%(dir2))

        condorio=SSH_utils.execute_remote_cmd(ssh,"ls -l %s"%(dir2))

        for line in condorio.split("\n"):
            if line.find("https")!=-1:
               target=line.lstrip().split(" ")[8]
              
        dir1="/var/SandboxDir/%s/%s"%(prefix,target)

        utils.info("Check files at %s"%(dir1))

        SSH_utils.execute_remote_cmd(ssh,"ls -l %s"%(dir1))
            
        dir3="/var/jobcontrol/submit/%s/"%(prefix)

        utils.info("Check files at %s"%(dir3))
        
        SSH_utils.execute_remote_cmd(ssh,"ls -l %s"%(dir3))

        utils.info("Wait until job finishes")

        utils.wait_until_job_finishes(JOBID)

        utils.job_status(JOBID)

        if utils.get_job_status().find("Done") != -1 :

            utils.info("Check on WMS auxiliary files should be removed")

            utils.info("Check directory %s"%(dir3))
            output=SSH_utils.execute_remote_cmd(ssh,"ls -l %s"%(dir3)).split("\n")

            if output.count("total 0")!=1:
                utils.error("Auxiliary files are not removed from directory %s"%(dir3))
                raise GeneralError("Check for auxiliary files at %s"%(dir3),"Auxiliary files are not removed from directory %s"%(dir3))
            else:
                utils.info("Auxiliary files are removed as expected from directory %s"%(dir3))

            utils.info("Check directory %s"%(dir2))
            output=SSH_utils.execute_remote_cmd(ssh,"ls -l %s"%(dir2)).split("\n")

            if output.count("total 0")!=1:
                utils.error("Auxiliary files are not removed from directory %s"%(dir2))
                raise GeneralError("Check for auxiliary files at %s"%(dir2),"Auxiliary files are not removed from directory %s"%(dir2))
            else:
                utils.info("Auxiliary files are removed as expected from directory %s"%(dir2))

            utils.info("Retrieve job output")

            utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s"%(utils.get_job_output_dir(),JOBID))

            utils.info("Check that also the SBD has been removed on WMS")

            utils.info("Check directory /var/SandboxDir/%s/"%(prefix))
            output=SSH_utils.execute_remote_cmd(ssh,"ls -l /var/SandboxDir/%s/"%(prefix)).split("\n")

            if output.count("total 0")!=1:
                utils.error("SBD not removed from directory /var/SandboxDir/%s/"%(prefix))
                raise GeneralError("Check for SBD at /var/SandboxDir/%s/"%(prefix),"Auxiliary files are not removed from directory %s"%(dir2))
            else:
                utils.info("SBD has been removed as expected from directory /var/SandboxDir/%s/"%(prefix))


        else:
            utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            raise GeneralError("Check job final status","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            
        utils.info("TEST OK")
        
    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0


def test2(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        Job_utils.prepare_normal_job(utils,utils.get_jdl_file(),"/cream-")

        utils.info("Submit a job to a CREAM CE without setting myproxyserver")

        JOBID=Job_utils.submit_only_normal_job(utils,"/cream-")[1]

        utils.info("Check the SBD and the others file used by the services")

        prefix=JOBID.split("https://%s:9000/"%(utils.get_WMS()))[1][0:2]
        
        dir="/var/SandboxDir/%s"%(prefix)

        utils.info("Check files at %s"%(dir))

        SSH_utils.execute_remote_cmd(ssh,"ls -l %s"%(dir))
 
        utils.info("Wait until job finishes")

        utils.wait_until_job_finishes(JOBID)

        utils.job_status(JOBID)

        if utils.get_job_status().find("Done") != -1 :

            utils.info("Retrieve job output")

            utils.run_command_continue_on_error ("glite-wms-job-output --nosubdir --noint --dir %s %s"%(utils.get_job_output_dir(),JOBID))

            utils.info("Check that the SBD has been removed on WMS")

            utils.info("Check directory /var/SandboxDir/%s/"%(prefix))
            output=SSH_utils.execute_remote_cmd(ssh,"ls -l /var/SandboxDir/%s/"%(prefix))
         
            output=output.split("\n")

            if output.count("total 0")!=1:
                utils.error("SBD not removed from directory /var/SandboxDir/%s/"%(prefix))
                raise GeneralError("Check for SBD at /var/SandboxDir/%s/"%(prefix),"Auxiliary files are not removed from directory %s"%(dir2))
            else:
                utils.info("SBD has been removed as expected from directory /var/SandboxDir/%s/"%(prefix))


        else:
            utils.error("Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))
            raise GeneralError("Check job final status","Job finishes with status: %s cannot retrieve output"%(utils.get_job_status()))

        utils.info("TEST OK")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0


def test3(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

          wms_location_var=SSH_utils.execute_remote_cmd(ssh,"echo $WMS_LOCATION_VAR")[:-1]

          utils.info("Check inside $WMS_LOCATION_VAR/proxycache for expired proxies for more than 6 hours")

          proxies=SSH_utils.execute_remote_cmd(ssh,"find %s/proxycache/ -name *.pem"%(wms_location_var)).split("\n")

          for proxy in proxies:
            
             if proxy.strip()!='':

                 expiry_date=SSH_utils.execute_remote_cmd(ssh,"openssl x509 -in %s -noout -enddate"%(proxy.strip())).split("=")[1].strip("\n")

                 ddate_str=time.strptime(expiry_date,"%b %d %H:%M:%S %Y %Z")[0:8]

                 dt = datetime.datetime(ddate_str[0],ddate_str[1],ddate_str[2],ddate_str[3],ddate_str[4],ddate_str[5],ddate_str[6])

                 now_dt = datetime.datetime.utcnow()

                 diff=now_dt-dt

                 minutes, seconds = divmod(diff.seconds, 60)
                 hours, minutes = divmod(minutes, 60)

                 if diff.days>=0:

                    #Maybe it is necessary to check and minutes
                    if hours>=6:
                        utils.error("Find expired proxy for more than 6 hours. Proxy is %s"%(proxy))
                        raise GeneralError("Check for expired proxies for more than 6 hours","Find expired proxy for more than 6 hours. Proxy is %s"%(proxy))

          utils.info("Check if there are empty directories")

          dirs = SSH_utils.execute_remote_cmd(ssh,"ls /%s/proxycache"%(wms_location_var)).split(" ")

          for dir in dirs:
              
              dir=dir.strip(" \n\t")

              if dir.find("cache")==-1:
                utils.info("Check directory: %s"%(dir))
                subdirs=SSH_utils.execute_remote_cmd(ssh,"find /var/proxycache/%s -name userproxy.pem | wc -l"%(dir))
                total_subdirs=SSH_utils.execute_remote_cmd(ssh,"ls -l /var/proxycache/%s | grep glite | wc -l"%(dir))

                if total_subdirs == subdirs :
                    utils.info("Check OK, there are no empty directories in %s"%(dir))
                else:
                    utils.error("Test Failed. There are empty directories in %s"%(dir))
                    raise GeneralError("Check for emptry directories","Test Failed. There are empty directories in %s"%(dir))
     
          utils.info("TEST OK")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0



def test4(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        utils.set_long_jdl(utils.get_jdl_file())

        utils.info("Submit a job")

        JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        prefix=JOBID.split("https://%s:9000/"%(utils.get_WMS()))[1][0:2]

        utils.job_status(JOBID)

        while(utils.get_job_status().find("Waiting")!=-1):
           utils.info("Wait 60 secs. Job's status is Waiting")
           time.sleep(60)
           utils.job_status(JOBID)

        utils.info("Purge the job")

        #WARNING EXECUTE COMMAND AS root INSTEAD OF glite USER
        utils.info("Execute '/usr/sbin/glite-wms-purgeStorage.sh -p /var/SandboxDir/%s -s' on remote host"%(prefix))

        output=SSH_utils.execute_remote_cmd(ssh,"/usr/sbin/glite-wms-purgeStorage.sh -p /var/SandboxDir/%s -s"%(prefix))

        utils.info("Check glite-wms-purgeStorage.sh output")

        if output.find("%s: removed"%(JOBID))!=-1:
             utils.info("glite-wms-purgeStorage.sh successfully remove the job %s"%(JOBID))
        else:
             utils.error("glite-wms-purgeStorage.sh didn't remove successfully the job %s"%(JOBID))
             raise GeneralError("Check glite-wms-purgeStorage.sh","glite-wms-purgeStorage.sh didn't remove successfully the job %s"%(JOBID))


        utils.info("Wait 60 secs")
        time.sleep(60)

        utils.info("Check again job's status")

        utils.job_status(JOBID)

        if utils.get_job_status().find("Cleared")!=-1:

              utils.info("Job's final status after purge is Cleared")

              utils.info("Check job's status reason")

              status=utils.get_job_status_reason(JOBID)

              if status.find("timed out, resource purge forced")!=-1:
                    utils.info("Status reason is 'timed out, resource purge forced' as expected")
              else:
                    utils.error("Status reason is %s while the expected is 'timed out, resource purge forced'"%(status))
                    raise GeneralError("Check job's status reason","Status reason is %s while the expected is 'timed out, resource purge forced'"%(status))

        else:
              utils.error("Job's final status after purge is not Cleared , instead we get %s"%(utils.get_job_status()))
              raise GeneralError("Check job final status after purge","Job's final status after purge is not Cleared , instead we get %s"%(utils.get_job_status()))

       
        utils.info("TEST OK")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0




def test5(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        Job_utils.prepare_normal_job(utils,utils.get_jdl_file())

        utils.info("Submit a job to a CREAM CE")

        JOBID=Job_utils.submit_only_normal_job(utils)[1]

        prefix=JOBID.split("https://%s:9000/"%(utils.get_WMS()))[1][0:2]

        utils.info("Wait until job finishes")

        utils.wait_until_job_finishes(JOBID)

        utils.job_status(JOBID)

        if utils.get_job_status().find("Done") != -1 :

             utils.info("Purge a done job")

             #WARNING EXECUTE COMMAND AS root INSTEAD OF glite USER
             utils.info("Execute '/usr/sbin/glite-wms-purgeStorage.sh -p /var/SandboxDir/%s -s' on remote host"%(prefix))
             
             output=SSH_utils.execute_remote_cmd(ssh,"/usr/sbin/glite-wms-purgeStorage.sh -p /var/SandboxDir/%s -s"%(prefix))

             utils.info("Check glite-wms-purgeStorage.sh output")

             if output.find("%s: removed DONE job"%(JOBID))!=-1:
                   utils.info("glite-wms-purgeStorage.sh successfully remove the DONE job %s"%(JOBID))
             else:
                   utils.error("glite-wms-purgeStorage.sh didn't remove successfully the DONE job %s"%(JOBID))
                   raise GeneralError("Check glite-wms-purgeStorage.sh","glite-wms-purgeStorage.sh didn't remove successfully the DONE job %s"%(JOBID))
             
             utils.info("Check again job's status")
         
             utils.job_status(JOBID)

             if utils.get_job_status().find("Cleared")!=-1:

                   utils.info("Job's final status after purge is Cleared")

                   utils.info("Check job's status reason")

                   status=utils.get_job_status_reason(JOBID)

                   if status.find("timed out, resource purge forced")!=-1:
                       utils.info("Status reason is 'timed out, resource purge forced' as expected")
                   else:
                       utils.error("Status reason is %s while the expected is 'timed out, resource purge forced'"%(status))
                       raise GeneralError("Check job's status reason","Status reason is %s while the expected is 'timed out, resource purge forced'"%(status))

             else:
                   utils.error("Job's final status after purge is not Cleared , instead we get %s"%(utils.get_job_status()))
                   raise GeneralError("Check job final status after purge","Job's final status after purge is not Cleared , instead we get %s"%(utils.get_job_status()))
            
        else:
            utils.error("Job finishes with status: %s while expected 'Done'"%(utils.get_job_status()))
            raise GeneralError("Check job final status","Job finishes with status: %s while expected 'Done'"%(utils.get_job_status()))

        utils.info("TEST OK")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0


def convert_to_job(str):

    jobid=str.split("/var/SandboxDir/")[1][3:]

    jobid=jobid.replace("_3a_2f_2f","://")
    jobid=jobid.replace("_3a",":")
    jobid=jobid.replace("_2f","/")
    jobid=jobid.replace("_5f","_")

    return jobid


def test6(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        wms_location_var=SSH_utils.execute_remote_cmd(ssh,"echo $WMS_LOCATION_VAR")[:-1]

        utils.info("Check inside $WMS_LOCATION_VAR/SandboxDir for uncleared jobs")

        available_jobs=SSH_utils.execute_remote_cmd(ssh,"find %s/SandboxDir/ -name https*"%(wms_location_var)).split("\n")
        
        last_update=[]

        threshold_overcome=0

        threshold=432

        for job_dir in available_jobs:

             if job_dir.strip()!='':

                 utils.info("Parse job id from directory %s"%(job_dir))

                 JOBID=convert_to_job(job_dir)

                 utils.info("Get the timestamp of the latest event for the job %s"%(JOBID))

                 timestamps=[]

                 output=utils.run_command_continue_on_error("glite-wms-job-logging-info  -v 2 %s"%(JOBID)).split("\n")

                 for line in output:
                     if line.find("- Timestamp")!=-1:
                         timestamps.append(line.split("=")[1].strip(" \t\n"))

                 last_update.append(timestamps[len(timestamps)-1])


        utils.info("Find jobs which are older than 12 hours")

        for update in last_update:
                            
             ddate_str=time.strptime(update,"%a %b %d %H:%M:%S %Y %Z")[0:8]

             dt = int(datetime.datetime(ddate_str[0],ddate_str[1],ddate_str[2],ddate_str[3],ddate_str[4],ddate_str[5],ddate_str[6]).strftime("%s"))

             now_dt = int(datetime.datetime.now().strftime("%s"))

             if now_dt-dt>threshold:
                threshold_overcome=threshold_overcome+1
             

        if threshold_overcome==0:
             utils.error("Test is skipped. There are no jobs older than 12 hours")
             raise GeneralError("Purge jobs older than 12 hours","Test is skipped. There are no jobs older than 12 hours")


        utils.info("Purge jobs older than 12 hours")

        #WARNING EXECUTE COMMAND AS root INSTEAD OF glite USER
        utils.info("Execute '/usr/sbin/glite-wms-purgeStorage.sh -p %s/SandboxDir -t %s' on remote host"%(wms_location_var,threshold))

        output=SSH_utils.execute_remote_cmd(ssh,"/usr/sbin/glite-wms-purgeStorage.sh -p %s/SandboxDir -t %s"%(wms_location_var,threshold)).split("\n")

        utils.info("Check the number of purged jobs")
    
        removed=0

        for line in output:
            if line.find(": removed")!=-1:
                removed=removed+1

        if removed!=threshold_overcome:
              utils.error("Removed %s jobs while expected %s"%(removed,threshold_overcome))
              raise GeneralError("Check the number of purged jobs","Removed %s jobs while expected %s"%(removed,threshold_overcome))


        utils.info("Check again the %s/SandboxDir directory after job purging")

        remaining_jobs=SSH_utils.execute_remote_cmd(ssh,"find %s/SandboxDir/ -name https*"%(wms_location_var)).split("\n")

        if len(available_jobs)-removed!=len(remaining_jobs):
             utils.error("It seems not to be removed all the jobs which are older than 12 hours")
             raise GeneralError("Check again the %s/SandboxDir directory after job purging","It seems not to be removed all the jobs which are older than 12 hours")



        utils.info("TEST OK")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0



def test7(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        wms_location_var=SSH_utils.execute_remote_cmd(ssh,"echo $WMS_LOCATION_VAR")[:-1]

        utils.info("Check inside $WMS_LOCATION_VAR/SandboxDir for jobs with expired proxy")

        proxies=SSH_utils.execute_remote_cmd(ssh,"find %s/SandboxDir/ -name user.proxy"%(wms_location_var)).split("\n")

        has_expired=0
        
        for proxy in proxies:

             if proxy.strip()!='':

                 expiry_date=SSH_utils.execute_remote_cmd(ssh,"openssl x509 -in %s -noout -enddate"%(proxy.strip())).split("=")[1].strip("\n")

                 ddate_str=time.strptime(expiry_date,"%b %d %H:%M:%S %Y %Z")[0:8]

                 dt = datetime.datetime(ddate_str[0],ddate_str[1],ddate_str[2],ddate_str[3],ddate_str[4],ddate_str[5],ddate_str[6])

                 now_dt = datetime.datetime.utcnow()

                 diff=now_dt-dt
            
                 minutes, seconds = divmod(diff.seconds, 60)
                 hours, minutes = divmod(minutes, 60)

                 if diff.days>=0:
                     
                     if minutes>0 or hours>0:
                        target_proxy=proxy
                        has_expired=1
                        break
                

        if has_expired==0:
              utils.error("Skip test: Unable to find any expired proxy in %s/SandboxDir"%(wms_location_var))
              raise GeneralError(title,"Skip test: Unable to find any expired proxy in %s/SandboxDir"%(wms_location_var))


        target_dir=target_proxy.split("/https")[0]

        utils.info("Purge a job with expired proxy")

        #WARNING EXECUTE COMMAND AS root INSTEAD OF glite USER
        utils.info("Execute '/usr/sbin/glite-wms-purgeStorage.sh -p %s -s' on remote host"%(target_dir))

        output=SSH_utils.execute_remote_cmd(ssh,"/usr/sbin/glite-wms-purgeStorage.sh -p %s -s"%(target_dir))

        utils.info("Get job id ")

        JOBID=output.split(": ")[2]

        utils.info("Check job's status")

        utils.job_status(JOBID)

        if utils.get_job_status().find("Cleared")!=-1:

              utils.info("Job's final status after purge is Cleared")

              utils.info("Check job's status reason")

              status=utils.get_job_status_reason(JOBID)

              if status.find("timed out, resource purge forced")!=-1:
                    utils.info("Status reason is 'timed out, resource purge forced' as expected")
              else:
                    utils.error("Status reason is %s while the expected is 'timed out, resource purge forced'"%(status))
                    raise GeneralError("Check job's status reason","Status reason is %s while the expected is 'timed out, resource purge forced'"%(status))

        else:
              utils.error("Job's final status after purge is not Cleared , instead we get %s"%(utils.get_job_status()))
              raise GeneralError("Check job final status after purge","Job's final status after purge is not Cleared , instead we get %s"%(utils.get_job_status()))

                
        utils.info("Check the user Clear event")

        output=utils.run_command_continue_on_error("glite-wms-job-logging-info --event Clear -v 2 %s"%(JOBID)).split("\n")

        host=""
        user=""

        for line in output:

            if line.find("- Host")!=-1:
                 host=line.split(" = ")[1].strip(" \t\n")


            if line.find("- User")!=-1:
                 user=line.split(" = ")[1].strip(" \t\t")


        if user.find(host)==-1:
             utils.error("Unable to find the host proxy as user of the Clear event")
             raise GeneralError("Check the user of the Clear event","Unable to find the host proxy as user of the Clear event")




        utils.info("TEST OK")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0



def test8(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        utils.set_dag_jdl(utils.get_jdl_file())

        utils.info("Submit a DAG job")

        JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

        utils.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        output=utils.run_command_continue_on_error("glite-wms-job-status -c %s %s"%(utils.get_config_file(),JOBID)).split("\n")

        nodes_prefix=[]
        nodes_dir=[]
        
        for line in output :

           if line.find("https://")!=-1 and line.find(JOBID)==-1:

               id=line.split("Status info for the Job : ")[1]
               ndprefix=id.split("https://%s:9000/"%(utils.get_WMS()))[1][0:2]
               
               nodes_prefix.append(ndprefix)
               nodes_dir.append(SSH_utils.execute_remote_cmd(ssh,"ls /var/SandboxDir/%s"%(ndprefix)))

        
        prefix=JOBID.split("https://%s:9000/"%(utils.get_WMS()))[1][0:2]

    
        utils.info("Purge a DAG job")

        
        #WARNING EXECUTE COMMAND AS root INSTEAD OF glite USER
        utils.info("Execute '/usr/sbin/glite-wms-purgeStorage.sh -p /var/SandboxDir/%s -s' on remote host"%(prefix))

        output=SSH_utils.execute_remote_cmd(ssh,"/usr/sbin/glite-wms-purgeStorage.sh -p /var/SandboxDir/%s -s"%(prefix))
        
        utils.info("Check glite-wms-purgeStorage.sh output")

        if output.find("%s: 3/3 nodes removed"%(JOBID))!=-1:
             utils.info("glite-wms-purgeStorage.sh successfully remove all the nodes of job %s"%(JOBID))
        else:
             utils.error("glite-wms-purgeStorage.sh didn't remove successfully all the nodes of job %s"%(JOBID))
             raise GeneralError("Check glite-wms-purgeStorage.sh","glite-wms-purgeStorage.sh didn't remove successfully all the nodes of job %s"%(JOBID))

        if output.find("%s: removed"%(JOBID))!=-1:
             utils.info("glite-wms-purgeStorage.sh successfully remove the job %s"%(JOBID))
        else:
             utils.error("glite-wms-purgeStorage.sh didn't remove successfully the job %s"%(JOBID))
             raise GeneralError("Check glite-wms-purgeStorage.sh","glite-wms-purgeStorage.sh didn't remove successfully the job %s"%(JOBID))

        
        utils.info("Check the SandBoxDir of nodes")

        x=0

        for ndprefix in nodes_prefix:

           output=SSH_utils.execute_remote_cmd_failed(ssh,"ls -l /var/SandboxDir/%s/%s1"%(ndprefix,nodes_dir[x]))

           if output.find("No such file or directory")==-1:
               utils.error("Command failed for some other reason. Expected reasaon 'No such file or directory'")
               raise GeneralError("Execute command ls -l /var/SandboxDir/%s/%s"%(ndprefix,nodes_dir[x]),"Command failed for some other reason. Expected reasaon 'No such file or directory'")

           x=x+1

        utils.info("Check job's final status")

        utils.job_status(JOBID)

        if utils.get_job_status().find("Cleared")!=-1:
              utils.info("Job's final status after purge is Cleared")
        else:
              utils.error("Job's final status after purge is not Cleared , instead we get %s"%(utils.get_job_status()))
              raise GeneralError("Check job final status after purge","Job's final status after purge is not Cleared , instead we get %s"%(utils.get_job_status()))

        
        utils.info("TEST OK")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0




    
def main():

    fails=[]

    tests=["Test 1: Test purge , normal job cycle ( Submit to LCG CE )"]
    tests.append("Test 2: Test purge, normal job cycle ( Submit to CREAM CE )")
    tests.append("Test 3: Test proxy cache purging")
    tests.append("Test 4: SandBoxDir cron purger ( Submit a job and force its purge before it finishes )")
    tests.append("Test 5: SandBoxDir cron purger ( Purge a DONE job )")
    tests.append("Test 6: SandBoxDir cron purger ( Purge only jobs older than 12 hours )")
    tests.append("Test 7: SandBoxDir cron purger ( Purge a job which proxy is already expired )")
    tests.append("Test 8: SandBoxDir cron purger ( Purge a DAG job )")

    utils = Test_utils.Test_utils(sys.argv[0],"WMS Purge Mechanism")

    utils.prepare(sys.argv[1:],tests)

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    if utils.WMS_USERNAME=='' or utils.WMS_PASSWORD=='':
       utils.warn("Please set the required variables WMS_USERNAME , WMS_PASSWORD in test's configuration file")
       utils.show_progress("Please set the required variables WMS_USERNAME , WMS_PASSWORD in test's configuration file")
       sys.exit(0)

    utils.info("WMS Purge Mechanism Testing")

    all_tests=utils.is_all_enabled()

    try:

        ssh=SSH_utils.open_ssh(utils.get_WMS(),utils.WMS_USERNAME,utils.WMS_PASSWORD)

    except (GeneralError) , e:
        utils.log_error("Unable to connect to remote host: %s"%(utils.get_WMS()))
        utils.log_error(e)
        utils.exit_failure("Unable to connect to remote host %s"%(utils.get_WMS()))


    if all_tests==1 or utils.check_test_enabled(1)==1 :
            if test1(utils,ssh,tests[0]):
                fails.append(tests[0])

    if all_tests==1 or utils.check_test_enabled(2)==1 :
            if test2(utils,ssh,tests[1]):
                fails.append(tests[1])

    if all_tests==1 or utils.check_test_enabled(3)==1 :
            if test3(utils,ssh,tests[2]):
                fails.append(tests[2])

    if all_tests==1 or utils.check_test_enabled(4)==1 :
            if test4(utils,ssh,tests[3]):
                fails.append(tests[3])
    
    if all_tests==1 or utils.check_test_enabled(5)==1 :
            if test5(utils,ssh,tests[4]):
                fails.append(tests[4])

    if all_tests==1 or utils.check_test_enabled(6)==1 :
            if test6(utils,ssh,tests[5]):
                fails.append(tests[5])

    if all_tests==1 or utils.check_test_enabled(7)==1 :
            if test7(utils,ssh,tests[6]):
                fails.append(tests[6])

    if all_tests==1 or utils.check_test_enabled(8)==1 :
            if test8(utils,ssh,tests[7]):
                fails.append(tests[7])


    
    SSH_utils.close_ssh(ssh)

    if len(fails) > 0 :
      utils.exit_failure("%s test(s) fail(s): %s"%(len(fails), fails))
    else:
      utils.exit_success()
    
    
if __name__ == "__main__":
    main()
