#
# Bug: 85071
# Title: Wmproxy authorization breaks with longer proxy chain
# Link: https://savannah.cern.ch/bugs/?85071
#
#

from lib.Exceptions import *

def run(utils):

    bug='85071'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.console_log("Interactive test")

    if utils.MYPROXYSERVER =='' :
        utils.log_info("ERROR: Please set the required variable MYPROXYSERVER at configuration file.")
        raise GeneralError("Check Configuration","Please set the required variable MYPROXYSERVER at configuration file.")

    utils.log_info("Prepare jdl file for submission")
    utils.use_utils_jdl()
  
    utils.log_info("Store a credential for later retrieval")

    utils.run_command("myproxy-init -d -s %s "%(utils.MYPROXYSERVER))

    utils.log_info("Retrieve a new proxy from the myproxy server")

    utils.run_command("myproxy-logon -d -s %s --voms %s "%(utils.MYPROXYSERVER,utils.VO))

    utils.log_info("Check that we have a proxy with a longer chain")

    result=utils.run_command("voms-proxy-info -all")

    result=result.split("\n")

    for line in result:
        if line.find("subject")!=-1:
            subject=line
            break
  
    if subject.count("CN=proxy")!=4:
       utils.log_info("ERROR: Test failed. Problem with proxy chain . Subject is (%s)"%(subject))
       raise GeneralError("Test failed","Problem with proxy chain. Subject is (%s)"%(subject))

    utils.log_info("Submit a job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Wait until job finishes")

    utils.wait_until_job_finishes(JOBID)

    utils.log_info("Check job stauts")

    utils.job_status(JOBID)

    if utils.get_job_status().find("Done (Success)")!=-1:
        utils.log_info("Test OK , job terminated successfully")
    else:
      utils.log_info("ERROR: Job status is not 'Done (Success)', job failed to terminated successfully. Status reason %s"%(utils.get_StatusReason(JOBID)))
      raise GeneralError("Check job status","Job status is not 'Done (Success)' but %s. Status reason %s"%(utils.get_job_status(),utils.get_StatusReason(JOBID)))

 
    utils.log_info("End of regression test for bug %s"%(bug))
