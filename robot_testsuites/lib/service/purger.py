
import time
import datetime
import SSH_utils

from Exceptions import *

def get_job_prefix(jobid):

    prefix=''

    prefix=jobid.split(":9000/")[1][0:2]

    return prefix


def get_target(data):

   target=''

   for line in data.split("\n"):
       if line.find("https")!=-1:
          target=line.lstrip().split(" ")[8]
          
   return target


def test2_target(utils,ssh,sbd_files,jobid):

   target=""

   for line in sbd_files.split("\n"):
   
      if line.find(jobid.split("https://%s:9000/"%(utils.get_WMS()))[1])!=-1:
          target="https_%s"%(line.lstrip().split("https_")[1])
                
   return target 



def get_location_var(utils,ssh):

  return SSH_utils.execute_remote_cmd(utils,ssh,"echo $WMS_LOCATION_VAR")[:-1]


def wait_the_job(utils,jobid):

  status=utils.get_job_status(jobid)

  while(status.find("Waiting")!=-1 or status.find("Ready")!=-1 ):
      utils.log_info("Wait 60 secs. Job's status is Waiting")
      time.sleep(60)
      status=utils.get_job_status(jobid)


def convert_to_job(str):

    jobid=str.split("/var/SandboxDir/")[1][3:]

    jobid=jobid.replace("_3a_2f_2f","://")
    jobid=jobid.replace("_3a",":")
    jobid=jobid.replace("_2f","/")
    jobid=jobid.replace("_5f","_")

    return jobid  


def get_nodes_prefix(utils,ssh,jobid):

    output=utils.run_command("glite-wms-job-status -c %s %s"%(utils.get_config_file(),jobid)).split("\n")

    nodes_prefix=[]
        
    for line in output :

       if line.find("https://")!=-1 and line.find(jobid)==-1:

           id=line.split("Status info for the Job : ")[1]
           ndprefix=id.split(":9000/")[1][0:2]
               
           nodes_prefix.append(ndprefix)
          

    return nodes_prefix


def get_nodes_dir(utils,ssh,jobid):

    output=utils.run_command("glite-wms-job-status -c %s %s"%(utils.get_config_file(),jobid)).split("\n")

    nodes_dir=[]
        
    for line in output :

       if line.find("https://")!=-1 and line.find(jobid)==-1:

           id=line.split("Status info for the Job : ")[1]
           ndprefix=id.split(":9000/")[1][0:2]
 
           nodes_dir.append(SSH_utils.execute_remote_cmd(utils,ssh,"ls /var/SandboxDir/%s"%(ndprefix)))

    return nodes_dir


def check_for_expired_proxies(utils,ssh,wms_location_var):

   proxies=SSH_utils.execute_remote_cmd(utils,ssh,"find %s/proxycache/ -name \*.pem"%(wms_location_var)).split("\n")

   for proxy in proxies:
            
       if proxy.strip()!='':

           expiry_date=SSH_utils.execute_remote_cmd(utils,ssh,"openssl x509 -in %s -noout -enddate"%(proxy.strip())).split("=")[1].strip("\n")

           ddate_str=time.strptime(expiry_date,"%b %d %H:%M:%S %Y %Z")[0:8]

           dt = datetime.datetime(ddate_str[0],ddate_str[1],ddate_str[2],ddate_str[3],ddate_str[4],ddate_str[5],ddate_str[6])

           now_dt = datetime.datetime.utcnow()

           diff=now_dt-dt

           minutes, seconds = divmod(diff.seconds, 60)
           hours, minutes = divmod(minutes, 60)

           if diff.days>=0:

              #Maybe it is necessary to check and minutes
              if hours>=6:
                 utils.log_info("ERROR: Find expired proxy for more than 6 hours. Proxy is %s"%(proxy))
                 raise GeneralError("Check for expired proxies for more than 6 hours","Find expired proxy for more than 6 hours. Proxy is %s"%(proxy))



def check_for_empty_directories(utils,ssh,wms_location_var):

   dirs = SSH_utils.execute_remote_cmd(utils,ssh,"ls /%s/proxycache"%(wms_location_var)).split(" ")

   for dir in dirs:
              
       dir=dir.strip(" \n\t")

       if dir.find("cache")==-1:
          utils.log_info("Check directory: %s"%(dir))
          subdirs=SSH_utils.execute_remote_cmd(utils,ssh,"find /%s/proxycache/%s -name userproxy.pem | wc -l"%(wms_location_var,dir))
          total_subdirs=SSH_utils.execute_remote_cmd(utils,ssh,"ls -l /%s/proxycache/%s | grep glite | wc -l"%(wms_location_var,dir))

          if total_subdirs == subdirs :
                utils.log_info("Check OK, there are no empty directories in %s"%(dir))
          else:
                utils.log_info("ERROR: Test Failed. There are empty directories in %s"%(dir))
                raise GeneralError("Check for emptry directories","Test Failed. There are empty directories in %s"%(dir))
     
     

def purge_jobs_older_than_12_hours(utils,ssh):

        wms_location_var=SSH_utils.execute_remote_cmd(utils,ssh,"echo $WMS_LOCATION_VAR")[:-1]

        utils.log_info("Check inside $WMS_LOCATION_VAR/SandboxDir for uncleared jobs")

        available_jobs=SSH_utils.execute_remote_cmd(utils,ssh,"find %s/SandboxDir/ -name https*"%(wms_location_var)).split("\n")
        
        last_update=[]

        threshold_overcome=0

        threshold=432

        for job_dir in available_jobs:

             if job_dir.strip()!='':

                 utils.log_info("Parse job id from directory %s"%(job_dir))

                 JOBID=convert_to_job(job_dir)

                 utils.log_info("Get the timestamp of the latest event for the job %s"%(JOBID))

                 timestamps=[]

                 output=utils.run_command("glite-wms-job-logging-info -v 2 %s"%(JOBID)).split("\n")

                 for line in output:
                     if line.find("- Timestamp")!=-1:
                         timestamps.append(line.split("=")[1].strip(" \t\n"))

                 last_update.append(timestamps[len(timestamps)-1])


        utils.log_info("Find jobs which are older than 12 hours")

        for update in last_update:
                            
             ddate_str=time.strptime(update,"%a %b %d %H:%M:%S %Y %Z")[0:8]

             dt = int(datetime.datetime(ddate_str[0],ddate_str[1],ddate_str[2],ddate_str[3],ddate_str[4],ddate_str[5],ddate_str[6]).strftime("%s"))

             now_dt = int(datetime.datetime.now().strftime("%s"))

             if now_dt-dt>threshold:
                threshold_overcome=threshold_overcome+1
             

        if threshold_overcome==0:
             utils.log_info("ERROR: Test is skipped. There are no jobs older than 12 hours")
             raise GeneralError("Purge jobs older than 12 hours","Test is skipped. There are no jobs older than 12 hours")


        utils.log_info("Purge jobs older than 12 hours")

        #WARNING EXECUTE COMMAND AS root INSTEAD OF glite USER
        utils.log_info("Execute '/usr/sbin/glite-wms-purgeStorage.sh -p %s/SandboxDir -t %s' on remote host"%(wms_location_var,threshold))

        output=SSH_utils.execute_remote_cmd(utils,ssh,"/usr/sbin/glite-wms-purgeStorage.sh -p %s/SandboxDir -t %s"%(wms_location_var,threshold)).split("\n")

        utils.log_info("Check the number of purged jobs")
    
        removed=0

        for line in output:
            if line.find(": removed")!=-1:
                removed=removed+1

        if removed!=threshold_overcome:
              utils.log_info("ERROR: Removed %s jobs while expected %s"%(removed,threshold_overcome))
              raise GeneralError("Check the number of purged jobs","Removed %s jobs while expected %s"%(removed,threshold_overcome))


        utils.log_info("Check again the %s/SandboxDir directory after job purging")

        remaining_jobs=SSH_utils.execute_remote_cmd(utils,ssh,"find %s/SandboxDir/ -name https*"%(wms_location_var)).split("\n")

        if len(available_jobs)-removed!=len(remaining_jobs):
             utils.log_info("ERROR: It seems not to be removed all the jobs which are older than 12 hours")
             raise GeneralError("Check again the %s/SandboxDir directory after job purging","It seems not to be removed all the jobs which are older than 12 hours")


def check_nodes_info(utils,ssh,nodes_prefix,nodes_dir):

    x=0

    for ndprefix in nodes_prefix:

       output=SSH_utils.execute_remote_cmd_failed(utils,ssh,"ls -l /var/SandboxDir/%s/%s"%(ndprefix,nodes_dir[x]))

       if output.find("No such file or directory")==-1:
               utils.log_info("Command failed for some other reason. Expected reason 'No such file or directory'")
               raise GeneralError("Execute command ls -l /var/SandboxDir/%s/%s"%(ndprefix,nodes_dir[x]),"Command failed for some other reason. Expected reasaon 'No such file or directory'")

       x=x+1



def test7_target(utils,ssh,wms_location_var):

     
        proxies=SSH_utils.execute_remote_cmd(utils,ssh,"find %s/SandboxDir/ -name user.proxy"%(wms_location_var)).split("\n")

        has_expired=0
        
        for proxy in proxies:

             if proxy.strip()!='':

                 expiry_date=SSH_utils.execute_remote_cmd(utils,ssh,"openssl x509 -in %s -noout -enddate"%(proxy.strip())).split("=")[1].strip("\n")

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
              utils.log_info("Skip test: Unable to find any expired proxy in %s/SandboxDir"%(wms_location_var))
              raise GeneralError("","Skip test: Unable to find any expired proxy in %s/SandboxDir"%(wms_location_var))


        target_dir=target_proxy.split("/https")[0]   

        return target_dir   

def test7_jobid(data):

    return data.split(": ")[2]


def get_clear_event_details(utils,jobid):


   output=utils.run_command("glite-wms-job-logging-info --event Clear -v 2 %s"%(jobid)).split("\n")

   host=""
   user=""

   for line in output:

       if line.find("- Host")!=-1:
             host=line.split(" = ")[1].strip(" \t\n")

       if line.find("- User")!=-1:
             user=line.split(" = ")[1].strip(" \t\t")

   return (host,user)


   
         
