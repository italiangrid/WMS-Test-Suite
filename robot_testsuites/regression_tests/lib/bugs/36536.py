#
# Bug:36536
# Title:  The glite wms purge storage library should rely on LBProxy while logging CLEAR events
# Link: https://savannah.cern.ch/bugs/?36536
#


from lib import Job_utils
from lib.Exceptions import *


def run(utils):

    bug='36536'

    utils.log_info("Start regression test for bug %s"%(bug))

    if utils.WMS_USERNAME=='' or utils.WMS_PASSWORD=='' or utils.USERNAME=='' or utils.PASSWORD=='' :
        utils.log_info("ERROR: Missing required variables (WMS_USERNAME,WMS_PASSWORD,USERNAME,PASSWORD) from configuration file")
        raise GeneralError("Missing required variables","To verify this bug it is necessary to set WMS_USERNAME,WMS_PASSWORD,USERNAME and PASSWORD in the configuration file")


    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Prepare and submit a simple job")

    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())

    JOBID=Job_utils.submit_wait_finish(utils,"")
    
    utils.log_info("Create SQL script file")

    utils.execute_remote_cmd(ssh,"echo \"SELECT * FROM jobs WHERE dg_jobid like '%%%s%%';\" > /root/test.sql"%(JOBID))

    utils.log_info("Retrieve the job record from LBProxy database")

    mysql_cmd="mysql -u %s --password=%s lbserver20 < /root/test.sql"%(utils.USERNAME,utils.PASSWORD)

    output=utils.execute_remote_cmd(ssh,mysql_cmd)

    if output.find(JOBID)==-1:
        utils.log_info("ERROR: Unable to retrieve the job record from LBProxy datasse for job id:%s"%(JOBID))
        raise GeneralError("Retrieve job record from LBProxy database","Unable to retrieve the job record from LBProxy datasse for job id:%s"%(JOBID))

    utils.log_info("Get job output")

    Job_utils.output_normal_job(utils,JOBID)

    #Check LBProxy
    utils.log_info("Check again the job record in LBProxy database")

    output=utils.execute_remote_cmd(ssh,mysql_cmd)

    if output.find(JOBID)!=-1:
        utils.log_info("ERROR: Job's record in LBProxy database has not been removed.")
        raise GeneralError("","Job's record in LBProxy database has not been removed.")
    
    utils.log_info("End of regression test for bug %s"%(bug))
