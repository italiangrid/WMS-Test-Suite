#
# Bug: 54728
# Title: WMP finds FQAN inconsistency only if GROUPS are different , not ROLES
# Link: https://savannah.cern.ch/bugs/?54728
#
#


from lib.Exceptions import *


def run(utils):

    bug='54728'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("To verify this bug you have to set attributes PROXY_PASSWORD and ROLE in configuration file")

    if utils.PROXY_PASSWORD=='' or utils.ROLE=='':
         utils.log_info("ERROR: Please set the required variables PROXY_PASSWORD and ROLE in test's configuration file")
         raise GeneralError("Missing required configuration attribute","Please set the required variables PROXY_PASSWORD and ROLE in test's configuration file")

    utils.log_info("Prepare jdl file for submission")
    utils.use_utils_jdl()
  
    utils.log_info("Create a new proxy")

    utils.run_command("echo %s | voms-proxy-init --voms %s -pwstdin"%(utils.PROXY_PASSWORD,utils.VO))

    utils.log_info("Delegate a user proxy")

    delegationId="test_54728"

    utils.run_command("glite-wms-job-delegate-proxy -c %s -d %s"%(utils.get_config_file(),delegationId))

    utils.log_info("Create a new proxy with role")

    utils.run_command("echo %s | voms-proxy-init --voms %s:/%s/Role=%s -pwstdin"%(utils.PROXY_PASSWORD,utils.VO,utils.VO,utils.ROLE))

    utils.log_info("Try to submit a job using the delegated proxy")

    output=utils.run_command_fail("glite-wms-job-submit -d %s --config %s %s"%(delegationId,utils.get_config_file(),utils.get_jdl_file()))

    if output.find("Client proxy FQAN")==-1 or output.find("does not match delegated proxy FQAN")==-1:
        utils.log_info("ERROR: Submission failed, but for some other reason not because client proxy FQAN does not match delegated proxy FQAN")
        raise GeneralError("","Submission failed, but for some other reason not because client proxy FQAN does not match delegated proxy FQAN")
    else:
        utils.log_info("Submission failed with the expected reason , client proxy FQAN does not match delegated proxy FQAN")

    utils.log_info("TEST OK")
 
    utils.log_info("End of regression test for bug %s"%(bug))
