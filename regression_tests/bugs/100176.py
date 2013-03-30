#
# Bug:100176
# Title: classad plugin functions are broken
# Link: https://savannah.cern.ch/bugs/?100176
#
#

import logging

from libutils.Exceptions import *
from libutils import Job_utils

def run(utils):

    bug='100176'

    logging.info("Start regression test for bug %s"%(bug))
        
    utils.use_external_jdl("%s.jdl"%(bug))
    
    logging.info("Execute list match")

    output=utils.run_command_continue_on_error("glite-wms-job-list-match %s -c %s  %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Check list match output")

    if output.find("No Computing Element matching your job requirements has been found")!=-1:
            logging.error("Output is not as expected. No Computing Element found matching our requirements")
            raise GeneralError("Check list match output","Output is not as expected. No Computing Element found matching our requirements")
    else:
          logging.info("List match returned %s computing elements"%(output.count(" - ")))

    logging.info("End of regression test for bug %s"%(bug))
