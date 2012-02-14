#
# Bug:44599
# Title: WMS should consider MaxTotalJobs
# Link: https://savannah.cern.ch/bugs/?44599
#
#

import logging

from libutils.Exceptions import *



def run(utils):

    bug='44599'

    logging.info("Start regression test for bug %s"%(bug))

    utils.use_external_jdl("%s.jdl"%(bug))
    
    logging.info("Submit the job")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Check job requirements expression")

    output=utils.run_command_continue_on_error("glite-wms-job-info --jdl %s "%(JOBID))

    #Extract requirements expression from jdl description
    output=output.split("\n")

    for line in output:

        if line.find("requirements")!=-1:
             requirements=line.split("requirements = ")[1].strip()
             
    
    #!!! Target expression differs slightly (* character at sdj expressions) from example at https://savannah.cern.ch/bugs/?44599
    target="( ( true ) && ( other.GlueCEStateStatus == \"Production\" ) ) && ( ( ( ShortDeadlineJob is true ) ? RegExp(\".*sdj$\",other.GlueCEUniqueID) :  !RegExp(\".*sdj$\",other.GlueCEUniqueID) ) && ( other.GlueCEPolicyMaxTotalJobs == 0 || other.GlueCEStateTotalJobs < other.GlueCEPolicyMaxTotalJobs ) && ( EnableWmsFeedback is true ? RegExp(\"cream\",other.GlueCEImplementationName,\"i\") : true ) );"

    if requirements == target:
        logging.info("Attribute requirements has the right expression")
    else:
        logging.error("Error expression at attribute requirements. Get %s while expect %s"%(requirements,target))
        raise GeneralError("","Error !!! Attribute requirements has not the expected expression.Get %s while expect %s"%(requirements,target))


    if utils.job_is_finished(JOBID) == 0 :
         logging.info("Cancel the job")
         utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))


    logging.info("End of regression test for bug %s"%(bug))
