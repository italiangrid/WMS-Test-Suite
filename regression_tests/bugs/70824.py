#
# Bug:70824
# Title: Environment values in JDL cannot have spaces
# Link: https://savannah.cern.ch/bugs/?70824
#
#

import logging

from libutils.Exceptions import *
from libutils import Job_utils

def run(utils):


    logging.info("Start regression test for bug 70824")
    
    OUTPUT="ATHENA_RUN_EVENTS=[(152345L, 216721L)]" # expected output
    
    # we need to test both lcg CE and CREAM CE
    
    for dest in ("/cream-", "2119/jobmanager") :
        
        utils.use_external_jdl("70824.jdl")
    
        utils.set_destination_ce(utils.get_jdl_name(), dest)

        Job_utils.submit_output_normal_job(utils, dest)

        ### Now check the job out output

        logging.info("Check if job output is as expected")

        FILE = open("%s/env.out"%(utils.get_job_output_dir()),"r")

        lines = FILE.readlines()

        R_OUTPUT=""

        for line in lines :
            if line.find("ATHENA_RUN_EVENTS") != -1: 
                R_OUTPUT=line[:-1] # remove the newline 
                break 

        FILE.close()

        if OUTPUT != R_OUTPUT :
            logging.error("Output is not as expected. We get output '%s' while expected '%s'",R_OUTPUT,OUTPUT)
            raise GeneralError("Check output","Not expected output. (Get %s expect %s)"%(R_OUTPUT,OUTPUT))
        else:
            logging.info("Output is as expected. Test OK")


    logging.info("End of regression test for bug 70824")
