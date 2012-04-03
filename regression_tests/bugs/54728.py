#
# Bug: 54728
# Title: WMP finds FQAN inconsistency only if GROUPS are different , not ROLES
# Link: https://savannah.cern.ch/bugs/?54728
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='54728'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you have to set attributes PROXY_PASSWORD and ROLE in configuration file")

    if utils.PROXY_PASSWORD=='' or utils.ROLE=='':
         logging.warn("Please set the required variables PROXY_PASSWORD and ROLE in test's configuration file")
         raise GeneralError("Missing required configuration attribute","Please set the required variables PROXY_PASSWORD and ROLE in test's configuration file")

    logging.info("Prepare jdl file for submission")
    utils.use_utils_jdl()
  
    logging.info("Create a new proxy")

    utils.run_command_continue_on_error("echo %s | voms-proxy-init --voms %s -pwstdin"%(utils.PROXY_PASSWORD,utils.VO))

    logging.info("Delegate a user proxy")

    delegationId="test_54728"

    utils.run_command_continue_on_error("glite-wms-job-delegate-proxy -c %s -d %s"%(utils.get_config_file(),delegationId))

    logging.info("Create a new proxy with role")

    utils.run_command_continue_on_error("echo %s | voms-proxy-init --voms %s:/%s/Role=%s -pwstdin"%(utils.PROXY_PASSWORD,utils.VO,utils.VO,utils.ROLE))

    logging.info("Try to submit a job using the delegated proxy")

    output=utils.run_command_fail_continue_on_error("glite-wms-job-submit -d %s --config %s %s"%(delegationId,utils.get_config_file(),utils.get_jdl_file()))

    if output.find("Client proxy FQAN")==-1 or output.find("does not match delegated proxy FQAN")==-1:
        logging.error("Submission failed, but for some other reason not because client proxy FQAN does not match delegated proxy FQAN")
        raise GeneralError("","Submission failed, but for some other reason not because client proxy FQAN does not match delegated proxy FQAN")
    else:
        logging.info("Submission failed with the expected reason , client proxy FQAN does not match delegated proxy FQAN")

    logging.info("TEST OK")
 
    logging.info("End of regression test for bug %s"%(bug))
