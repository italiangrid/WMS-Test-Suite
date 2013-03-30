#
# Bug:100176
# Title: classad plugin functions are broken
# Link: https://savannah.cern.ch/bugs/?100176
#
#


from lib.Exceptions import *
from lib import Job_utils


def run(utils):

    bug='100176'

    utils.log_info("Start regression test for bug %s"%(bug))
        
    utils.use_external_jdl("%s.jdl"%(bug))
    
    utils.log_info("Execute list match")

    output=utils.run_command("glite-wms-job-list-match %s -c %s  %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Check list match output")

    if output.find("No Computing Element matching your job requirements has been found")!=-1:
            utils.log_info("ERROR: Output is not as expected. No Computing Element found matching our requirements")
            raise GeneralError("Check list match output","Output is not as expected. No Computing Element found matching our requirements")
    else:
          utils.log_info("List match returned %s computing elements"%(output.count(" - ")))

    utils.log_info("End of regression test for bug %s"%(bug))
