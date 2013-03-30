#
# Bug:74259
# Title: Previous matches information is not taken into account if direct submission is used
# Link: https://savannah.cern.ch/bugs/?74259
#
#

from lib.Exceptions import *


def run(utils):

    bug='74259'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.use_utils_jdl()
    utils.set_shallow_jdl(utils.get_jdl_file())
    
    # select a matching CE
    output=utils.run_command("glite-wms-job-list-match %s --config %s --noint %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
    for lines in output.splitlines():
        if lines.find(" - ") == 0:
            CEID=lines[3:]
            break
    
    target=CEID.split(":")[0] # CE host name
    
    utils.log_info("Submit directly to %s a job which trigger a resubmission"%(CEID))    

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg -r %s %s"%(utils.get_delegation_options(),utils.get_config_file(),CEID,utils.get_jdl_file()))
    
    utils.wait_until_job_finishes (JOBID)
    utils.job_status(JOBID)
    
    utils.log_info("Check the CEInfoHostName at UserTag events (destination CE is %s)"%(target))

    OUTPUT=utils.run_command("glite-wms-job-logging-info -v 2 --user-tag CEInfoHostName=%s %s "%(target, JOBID))

    if OUTPUT.count("Event: UserTag") == 3:
        utils.log_info("Test PASS")
    else:
        utils.log_info("ERROR: CEInfoHostName has not the value of the chosen CE for all the events")
        raise GeneralError("Check CEInfoHostName","CEInfoHostName has not the value of the chosen CE for all the events ")    
    
    
    utils.log_info("End of regression test for bug %s"%(bug))

