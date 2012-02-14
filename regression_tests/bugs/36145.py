#
# Bug:36145
# Title: Jobdir support to be enabled in the glite-wms-planner
# Link: https://savannah.cern.ch/bugs/?36145
#
#

import logging

from libutils.Exceptions import *

from libutils import Job_utils


def run(utils):

    bug='36145'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Set DispatcherType=\"jobdir\";  and  Input=\"${WMS_LOCATION_VAR}/workload_manager/jobdir\"; to glite_wms.conf at WMS")

    attributes=['DispatcherType','Input']
    old=['filelist','${WMS_LOCATION_VAR}/workload_manager/input.fl']
    new=['jobdir','${WMS_LOCATION_VAR}/workload_manager/jobdir']
  
    utils.change_remote_file(ssh, "/etc/glite-wms/glite_wms.conf", attributes,old,new)

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    logging.info("Submit the job and wait to finish")

    #We use the same jdl with bug 35250
    utils.use_external_jdl("35250.jdl")

    logging.info("Submit the job and wait to finish")

    utils.set_destination_ce(utils.get_jdl_file(),"2119/jobmanager")

    JOBID=Job_utils.submit_wait_finish(utils)

    logging.info("Check job's final status")

    utils.job_status(JOBID)

    if utils.JOBSTATUS.find('Done (Success)') == -1 :
        logging.error("Job not finished successfully. Job final status is '%s' instead of 'Done (Success)'"%(utils.get_job_status()))
        utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
        raise GeneralError("Check job final status","Job not finished successfully. Job final status is '%s' instead of 'Done (Success)'"%(utils.get_job_status()))
    else:
         logging.info("Job finished successfully.")


    logging.info("Restore the initial glite_wms.conf file")

    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
    

    ssh.close()

    logging.info("End of regression test for bug %s"%(bug))
