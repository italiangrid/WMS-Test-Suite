#
# Bug:75223
# Title: wrong reason logged
# Link: https://savannah.cern.ch/bugs/?75223
#
#

import logging

from libutils.Exceptions import *
from libutils import Job_utils

def run(utils):

    bug='75223'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Prepare jdl file for submission")

    for dest in ("/cream-", "2119/jobmanager") :
    
        # Necessary to avoid overwrite of the external jdls
        utils.use_utils_jdl()
        utils.set_jdl(utils.get_jdl_file())
        utils.set_destination_ce(utils.get_jdl_name(), dest)


        JOBID=Job_utils.submit_wait_finish(utils,dest)

        logging.info("Check failing reasons")
        
        reason=utils.getLoggedReason(JOBID)
        
        for msg in reason:
            if msg.find("LM_log_done_begin") != -1:
                logging.error("Wrong message found in %s",msg)
                raise GeneralError("Check failig reasons","Wrong message found in %s"%(msg))
                break
     
    logging.info("End of regression test for bug %s"%(bug))
