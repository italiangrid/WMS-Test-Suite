#
# Bug:36145
# Title: Jobdir support to be enabled in the glite-wms-planner
# Link: https://savannah.cern.ch/bugs/?36145
#
#


from lib.Exceptions import *
from lib import Job_utils


def run(utils):

    bug='36145'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Set DispatcherType=\"jobdir\";  and  Input=\"${WMS_LOCATION_VAR}/workload_manager/jobdir\"; to glite_wms.conf at WMS")

    attributes=['DispatcherType','Input']
    new=['\"jobdir\"','\"${WMS_LOCATION_VAR}/workload_manager/jobdir\"']
  
    utils.change_attribute_at_remote_file_section(ssh,"/etc/glite-wms/glite_wms.conf",attributes[0],'WorkloadManager',new[0])
    utils.change_attribute_at_remote_file_section(ssh,"/etc/glite-wms/glite_wms.conf",attributes[1],'WorkloadManager',new[1])

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    utils.log_info("Submit the job and wait to finish")

    utils.use_external_jdl("%s.jdl"%(bug))

    utils.log_info("Submit the job and wait to finish")

    utils.set_destination_ce(utils.get_jdl_file(),"2119/jobmanager")

    JOBID=Job_utils.submit_wait_finish(utils)

    utils.log_info("Check job's final status")

    utils.job_status(JOBID)

    if utils.JOBSTATUS.find('Done (Success)') == -1 :
        utils.log_info("ERROR: Job not finished successfully. Job final status is '%s' instead of 'Done (Success)'"%(utils.get_job_status()))
        utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
        raise GeneralError("Check job final status","Job not finished successfully. Job final status is '%s' instead of 'Done (Success)'"%(utils.get_job_status()))
    else:
         utils.log_info("Job finished successfully.")


    utils.log_info("Restore the initial glite_wms.conf file")

    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
    
    ssh.close()

    utils.log_info("End of regression test for bug %s"%(bug))
