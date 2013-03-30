#
# Bug:34420
# Title: WMS Client: glite-wms-job-submit option --valid does not accept any time value
# Link: https://savannah.cern.ch/bugs/?34420
#
#

import time
import math

from lib.Exceptions import *


def run(utils):

    bug='34420'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())
  
    utils.log_info("Submit job")
    
    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg --valid 01:00 %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    now=math.ceil(time.time())

    utils.log_info("Get job's info")

    job_info=utils.run_command("glite-wms-job-info --jdl %s"%(JOBID))

    utils.log_info("Cancel the submitted job")

    utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))

    utils.log_info("Look at job requirements for attribute ExpiryTime")

    job_info_lines=job_info.split("\n")

    target=''

    for line in job_info_lines :
        if line.find("ExpiryTime")!=-1:
           target=line.strip()
           break

    #Get the value from the expression ExpiryTime=value; and

    target=target.split("=")
    jdl_time=target[1].split(";")[0]

    diff=int(jdl_time)-int(now)

    if diff <= 3500 or diff >= 3610 :
       utils.log_info("ERROR: Test failed, we did not find the attribute %s at job requirements {%s}"%(attribute,target))
       raise GeneralError("","Error !!! Test failed, we did not find the attribute %s at job requirements {%s}"%(attribute,target))
   
      
    utils.log_info("End of regression test for bug %s"%(bug))
