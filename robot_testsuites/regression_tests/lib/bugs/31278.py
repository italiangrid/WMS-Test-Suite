#
# Bug:31278
# Title: WMS should prevent non-SDJ jobs from being scheduled on SDJ CEs
# Link: https://savannah.cern.ch/bugs/?31278
#
#

from lib.Exceptions import *


def run(utils):

    bug='31278'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())
    utils.add_jdl_attribute(utils.get_jdl_file(),'ShortDeadlineJob','true')

    utils.log_info("Submit job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    attribute="RegExp(\".*sdj$\",other.GlueCEUniqueID)"

    utils.log_info("Get job's info")

    job_info=utils.run_command("glite-wms-job-info --jdl %s"%(JOBID))

    utils.log_info("Cancel the submitted job")

    utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))

    utils.log_info("Look at job requirements for attribute: %s"%(attribute))
    
    job_info_lines=job_info.split("\n")

    target=''

    for line in job_info_lines :
        if line.find("requirements")!=-1:
           target=line
           break

    if target.find(attribute) == -1:
       utils.log_info("ERROR: Test failed, we did not find the attribute %s at job requirements {%s}"%(attribute,target))
       raise GeneralError("","Error !!! Test failed, we did not find the attribute %s at job requirements {%s}"%(attribute,target))


    utils.remove(utils.get_jdl_file())
    utils.set_jdl(utils.get_jdl_file())
    utils.add_jdl_attribute(utils.get_jdl_file(),'ShortDeadlineJob','false')

    utils.log_info("Submit job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    attribute="!RegExp(\".*sdj$\",other.GlueCEUniqueID)"

    utils.log_info("Get job's info")

    job_info=utils.run_command("glite-wms-job-info --jdl %s"%(JOBID))

    utils.log_info("Cancel the submitted job")

    utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))

    utils.log_info("Look at job requirements for attribute: %s"%(attribute))

    job_info_lines=job_info.split("\n")

    target=''

    for line in job_info_lines :
        if line.find("requirements")!=-1:
           target=line
           break

    if target.find(attribute) == -1:
       utils.log_info("ERROR: Test failed, we did not find the attribute %s at job requirements"%(attribute))
       raise GeneralError("","Error !!! Test failed, we did not find the attribute %s at job requirements {%s}"%(attribute,target))


    utils.log_info("End of regression test for bug %s"%(bug))
