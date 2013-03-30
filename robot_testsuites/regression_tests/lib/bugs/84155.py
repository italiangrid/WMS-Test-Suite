#
# Bug: 84155
# Title: Internal proxy structure convertion error in ICE 
# Link: https://savannah.cern.ch/bugs/?84155
#
#

from lib.Exceptions import *

def run(utils):

    bug='84155'

    utils.log_info("Start regression test for bug %s"%(bug))

    if utils.PROXY_PASSWORD=='':
       utils.log_info("ERROR: Please set the required variable PROXY_PASSWORD in test's configuration file")
       raise GeneralError("Missing required configuration attribute","Please set the required variable PROXY_PASSWORD in test's configuration file")

    utils.log_info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_external_jdl("%s.jdl"%(bug))
    utils.add_jdl_attribute(utils.get_jdl_file(),'MyProxyServer',"%s"%utils.get_MYPROXY_SERVER())

    utils.log_info("Create a short proxy, valid for 14 minutes")

    utils.run_command("echo %s | voms-proxy-init --voms %s --valid 00:14 -pwstdin"%(utils.PROXY_PASSWORD,utils.VO))

    utils.log_info("Submit the job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Check that job's proxy is valid for no more than 14 minutes")

    output=utils.run_command("glite-wms-job-info -p %s"%(JOBID))

    for line in output.splitlines():
            if line.split(":")[0].strip() == "Timeleft":
                token=line.split(":")[1].strip()
                if ( (token.split(" ")[1] == "hours") or
                   (int(token.split(" ")[0]) > 14 ) ):
                    utils.log_info("ERROR: The proxy of the submitted job has not the expected duration")
                    raise GeneralError("Check proxy of the submitted job","Wrong duration")


    utils.log_info("Create a long proxy")

    utils.run_command("echo %s | voms-proxy-init --voms %s -pwstdin "%(utils.PROXY_PASSWORD,utils.VO))

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
