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
        utils.add_jdl_attribute(utils.get_jdl_file(),"Prologue","\"/bin/false\"")

        JOBID=Job_utils.submit_wait_finish(utils,dest)

        logging.info("Check if failed reason is 'Prologue failed with error 1'")
    
        result=utils.run_command_continue_on_error("glite-wms-job-logging-info -v 2 --event Done %s"%(JOBID))
 
        blocks=result.split('Event: Done')

        logmonitor_reasons=[]

        for block in blocks:
          if block.find('LogMonitor')!=-1:
             lines=block.split('\n')
             for line in lines:
                if line.find('Reason')!=-1:
                  logmonitor_reasons.append(line.split(' = ')[1].strip(' \t\n'))
                  break

        
        for reason in logmonitor_reasons:
            if reason!='Prologue failed with error 1' and reason!='prologue failed with error 1':
                logging.error("Wrong faild reason for LogMonitor. Found '%s' , while expected is 'Prologue failed with error 1'",reason)
                raise GeneralError("Check failend reasons for LogMonitor","Wrong failed reason. Found %s , while expected is 'Prologue failed with error 1'"%(reason))
                break
        
    logging.info("End of regression test for bug %s"%(bug))
