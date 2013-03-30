#
# Bug:28637
# Title: Delegation IDs not found when CREAM persistence storage is cleared
# Link: https://savannah.cern.ch/bugs/?28637
#
#


from lib.Exceptions import *


def run(utils):

    bug='28637'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("To verify this bug you need access to some CREAM CE. You have to set OTHER_HOST,OTHER_USERNAME and OTHER_PASSWORD attributes at configuration file")

    if utils.OTHER_HOST=='' or utils.OTHER_USERNAME=='' or utils.OTHER_PASSWORD=='' :
        utils.log_info("ERROR: Missing required variables (OTHER_HOST, OTHER_USERNAME,OTHER_PASSWORD) from configuration file")
        raise GeneralError("Missing required variables","To verify this bug it is necessary to set OTHER_HOST,OTHER_USERNAME and OTHER_PASSWORD in the configuration file")


    ssh=utils.open_ssh(utils.OTHER_HOST,utils.OTHER_USERNAME,utils.OTHER_PASSWORD)

    utils.log_info("Create a delegated proxy")

    utils.run_command("glite-wms-job-delegate-proxy --config %s -d bug_%s"%(utils.get_config_file(),bug))

    utils.log_info("Submit a job to a CREAM CE")

    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())
    utils.set_destination_ce(utils.get_jdl_file(),utils.OTHER_HOST)
       
    JOBID=utils.run_command("glite-wms-job-submit --config %s -d bug_%s --nomsg %s"%(utils.get_config_file(),bug,utils.get_jdl_file()))

    utils.log_info("Get the user DN with which we are submitting")

    OUTPUT=utils.run_command("voms-proxy-info")

    OUTPUT=OUTPUT.split("\n")

    for line in OUTPUT:
        if line.find("identity")!=-1:
            user_dn=line.split(":")[1].strip()
            
    utils.log_info("Create SQL script file")

    utils.execute_remote_cmd(ssh,"echo \"DELETE FROM t_credential WHERE dn like '%%%s%%';\" > /root/test.sql"%(user_dn))
    utils.execute_remote_cmd(ssh,"echo \"DELETE FROM t_credential_cache WHERE dn like '%%%s%%';\" >> /root/test.sql"%(user_dn))

    utils.log_info("Delete records for the user DN %s from the delegationdb on the CREAM CE"%(user_dn))

    mysql_cmd="mysql -u %s --password=%s delegationdb < /root/test.sql"%(utils.OTHER_USERNAME,utils.OTHER_PASSWORD)

    utils.execute_remote_cmd(ssh,mysql_cmd)

    utils.log_info("Submit a new normal job using the same delegated proxy as above")

    JOBID=utils.run_command("glite-wms-job-submit --config %s -d bug_%s --nomsg %s"%(utils.get_config_file(),bug,utils.get_jdl_file()))

    utils.log_info("Wait until job finishes")

    utils.wait_until_job_finishes(JOBID)

    utils.log_info("Check job status")

    utils.job_status(JOBID)

    if utils.get_job_status().find("Done (Success)")!=-1:
          utils.log_info("Job finished successfully. Test OK.")
    else:
          utils.log_info("ERROR: Test failed. Job final status is '%s' while expecting 'Done (Success)'"%(utils.get_job_status()))
          raise GeneralError("Check job status","Error !!!. Job final status is '%s' while expecting 'Done (Success)'")

   
    utils.log_info("End of regression test for bug %s"%(bug))
