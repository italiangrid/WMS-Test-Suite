#
# Bug:58968
# Title: Request for handling SMPGranularity attribute in the JDL
# Link: https://savannah.cern.ch/bugs/?58968
#
#

from lib.Exceptions import *

def run(utils):

    bug='58968'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())
    utils.add_jdl_general_attribute(utils.get_jdl_file(),'SMPGranularity','2')
    
    utils.log_info("Submit job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    attribute="other.GlueHostArchitectureSMPSize >= SMPGranularity"

    utils.log_info("Look at job requirements for attribute: %s"%(attribute))

    output=utils.run_command("glite-wms-job-info --jdl %s "%(JOBID))

    #Extract requirements expression from jdl description
    output=output.split("\n")

    for line in output:

        if line.find("requirements")!=-1:
             requirements=line.split("requirements = ")[1].strip()


    if requirements.find(attribute) !=-1 :
        utils.log_info("Test OK")
        utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))
    else:
        utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))
        utils.log_info("ERROR: Test failed. Unable to find attribute '%s' at requirements expression"%(attribute))
        raise GeneralError("Check requirements expression at jdl","Error !!!. Test faild, unable to find attribute '%s' at requirements expression"%(attribute))
           
    utils.log_info("End of regression test for bug %s"%(bug))
