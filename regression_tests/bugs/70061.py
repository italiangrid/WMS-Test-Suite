#
# Bug:70061
# Title:WMS hates collections with 192 nodes!
# Link: https://savannah.cern.ch/bugs/?70061
#
#

import logging
import os.path
import time


from libutils.Exceptions import *



def run(utils):

    bug='70061'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Submit job collection with 192 nodes!")

    utils.use_utils_jdl()

    utils.set_isb_jdl(utils.get_jdl_file())

    # create 192 jdl files based on basic jdl file
    logging.info("Create 192 jdl files based on basic jdl file %s",utils.get_jdl_file())

    if os.path.isdir("%s/collection_jdls"%(utils.get_tmp_dir())):
         os.system("rm -rf %s/collection_jdls"%(utils.get_tmp_dir()))

    os.mkdir("%s/collection_jdls"%(utils.get_tmp_dir()))

    for x in range(1,193) :
       os.system("cp %s %s/collection_jdls/%s.jdl"%(utils.get_jdl_file(),utils.get_tmp_dir(),x))
    

    logging.info("Now submit the job collection")

    JOBID=utils.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg --collection %s/collection_jdls"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_tmp_dir()))

    logging.info("Job submitted successfuly. Returned JOBID: %s",JOBID)
   
    time.sleep(60)

    if utils.job_is_finished(JOBID) == 0 :
        logging.info("Cancel the job collection")
        utils.run_command_continue_on_error ("glite-wms-job-cancel --noint %s"%(JOBID))

    logging.info("End of regression test for bug %s"%(bug))

