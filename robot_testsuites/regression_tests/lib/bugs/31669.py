#
# Bug:31669
# Title: org.glite.jdl.api-cpp: defaultNode[Shallow]RetryCount attributes unexpected behavior
# Link: https://savannah.cern.ch/bugs/?31669
#
#


from lib.Exceptions import *


def run(utils):

    bug='31669'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Prepare jdl file for submission")

    utils.use_external_jdl("%s.jdl"%(bug))

    utils.log_info("Submit job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Get job's info")

    job_info=utils.run_command("glite-wms-job-info --jdl %s"%(JOBID))

    utils.log_info("Cancel the submitted job")

    utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))

    utils.log_info("Look at job requirements for required attributes")
    
    job_info_lines=job_info.split("\n")

    count_attributes=[]

    #find 3 times
    target_1='RetryCount = 17;'
    target_2='ShallowRetryCount = 13;'

    #find one time
    target_3='DefaultNodeShallowRetryCount = 13;'
    target_4='DefaultNodeRetryCount = 17;'

    for line in job_info_lines :
        if line.find("Count")!=-1:
           count_attributes.append(line.strip())


    set_r=count_attributes.count(target_1)

    if int(set_r ) !=3 :
       utils.log_info("ERROR: Test failed, we did not find the attribute %s 3 times as required, instead get %s"%(target_1,int(set_r)))
       raise GeneralError("","Error !!! Test failed, we did not find the attribute %s 3 times as required, instead get %s"%(target_1,int(set_r)))

    set_r=count_attributes.count(target_2)

    if int(set_r ) !=3 :
       utils.log_info("ERROR: Test failed, we did not find the attribute %s 3 times as required, instead get %s"%(target_2,int(set_r)))
       raise GeneralError("","Error !!! Test failed, we did not find the attribute %s 3 times as required, instead get %s"%(target_2,int(set_r)))


    set_r=count_attributes.count(target_3)

    if int(set_r ) !=1 :
       utils.log_info("ERROR: Test failed, we did not find the attribute %s one time as required, instead get %s"%(target_3,int(set_r)))
       raise GeneralError("","Error !!! Test failed, we did not find the attribute %s one time as required, instead get %s"%(target_3,int(set_r)))


    set_r=count_attributes.count(target_4)

    if int(set_r ) !=1 :
       utils.log_info("ERROR: Test failed, we did not find the attribute %s one time as required, instead get %s"%(target_4,int(set_r)))
       raise GeneralError("","Error !!! Test failed, we did not find the attribute %s one time as required, instead get %s"%(target_4,int(set_r)))

          
    utils.log_info("End of regression test for bug %s"%(bug))
