#
# Bug:44599
# Title: WMS should consider MaxTotalJobs
# Link: https://savannah.cern.ch/bugs/?44599
#
#

from lib.Exceptions import *


def run(utils):

    bug='44599'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.use_external_jdl("%s.jdl"%(bug))
    
    utils.log_info("Submit the job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Check job requirements expression")

    output=utils.run_command("glite-wms-job-info --jdl %s "%(JOBID))

    #Extract requirements expression from jdl description
    output=output.split("\n")

    for line in output:

        if line.find("requirements")!=-1:
             requirements=line.split("requirements = ")[1].strip()
             
    
    #!!! Target expression differs slightly (* character at sdj expressions) from example at https://savannah.cern.ch/bugs/?44599
    target="( ( true ) && ( other.GlueCEStateStatus == \"Production\" ) ) && ( ( ( ShortDeadlineJob is true ) ? RegExp(\".*sdj$\",other.GlueCEUniqueID) :  !RegExp(\".*sdj$\",other.GlueCEUniqueID) ) && ( other.GlueCEPolicyMaxTotalJobs == 0 || other.GlueCEStateTotalJobs < other.GlueCEPolicyMaxTotalJobs ) && ( EnableWmsFeedback is true ? RegExp(\"cream\",other.GlueCEImplementationName,\"i\") : true ) );"

    if requirements == target:
        utils.log_info("Attribute requirements has the right expression")
    else:
        utils.log_info("ERROR: Error expression at attribute requirements. Get %s while expect %s"%(requirements,target))
        raise GeneralError("","Error !!! Attribute requirements has not the expected expression.Get %s while expect %s"%(requirements,target))


    if utils.job_is_finished(JOBID) == 0 :
         utils.log_info("Cancel the job")
         utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))

    utils.log_info("End of regression test for bug %s"%(bug))
