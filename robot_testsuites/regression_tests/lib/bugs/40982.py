#
# Bug:40982
# Title: When a collection is aborted the "Abort" event should be logged for the sub-nodes as well 
# Link: https://savannah.cern.ch/bugs/?40982
#
#


from lib.Exceptions import *

def run(utils):

    bug='40982'

    utils.log_info("Start regression test for bug %s"%(bug))
    
    utils.log_info("Submit the job and wait to finish")

    utils.use_external_jdl("%s.jdl"%(bug))

    utils.log_info("Register the collection")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg --register-only %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Start job execution")

    utils.run_command("glite-wms-job-submit --start %s"%(JOBID))

    utils.log_info("Wait the job to finish")

    utils.wait_until_job_finishes(JOBID)

    utils.log_info("Check job final status")

    output=utils.run_command("glite-wms-job-status  %s "%(JOBID))

    if int(output.count("Aborted")) == 11 :
        utils.log_info("We have 11 Abort events as expected")
    else:
      utils.log_info("ERROR: Wrong number of abort events. Get %s expected 11"%(counter))
      raise GeneralError("","Error !!! Error retry count. Get %s expected 11"%(counter))


    utils.log_info("End of regression test for bug %s",bug)
