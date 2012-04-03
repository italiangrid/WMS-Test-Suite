#
# Bug:36536
# Title:  The glite wms purge storage library should rely on LBProxy while logging CLEAR events
# Link: https://savannah.cern.ch/bugs/?36536
#


import logging

from libutils import Job_utils

from libutils.Exceptions import *


def run(utils):

    bug='36536'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to LBProxy DATABASE. You have to set USERNAME and PASSWORD attributes at configuration file")

    if utils.WMS_USERNAME=='' or utils.WMS_PASSWORD=='' or utils.USERNAME=='' or utils.PASSWORD=='' :
        logging.error("Missing required variables (WMS_USERNAME,WMS_PASSWORD,USERNAME,PASSWORD) from configuration file")
        raise GeneralError("Missing required variables","To verify this bug it is necessary to set WMS_USERNAME,WMS_PASSWORD,USERNAME and PASSWORD in the configuration file")


    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Prepare and submit a simple job")

    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())

    JOBID=Job_utils.submit_wait_finish(utils,"")
    
    logging.info("Create SQL script file")

    utils.execute_remote_cmd(ssh,"echo \"SELECT * FROM jobs WHERE dg_jobid like '%%%s%%';\" > /root/test.sql"%(JOBID))

    logging.info("Retrieve the job record from LBProxy database")

    mysql_cmd="mysql -u %s --password=%s lbserver20 < /root/test.sql"%(utils.USERNAME,utils.PASSWORD)

    output=utils.execute_remote_cmd(ssh,mysql_cmd)

    if output.find(JOBID)==-1:
        logging.error("Unable to retrieve the job record from LBProxy datasse for job id:%s"%(JOBID))
        raise GeneralError("Retrieve job record from LBProxy database","Unable to retrieve the job record from LBProxy datasse for job id:%s"%(JOBID))

    logging.info("Get job output")

    Job_utils.output_normal_job(utils,JOBID)

    #Check LBProxy
    logging.info("Check again the job record in LBProxy database")

    output=utils.execute_remote_cmd(ssh,mysql_cmd)

    if output.find(JOBID)!=-1:
        logging.error("Job's record in LBProxy database has not been removed.")
        raise GeneralError("","Job's record in LBProxy database has not been removed.")
    
    logging.info("End of regression test for bug %s"%(bug))