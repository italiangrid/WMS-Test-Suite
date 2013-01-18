#
# Bug: 89508
# Title: EMI WMS WM might abort resubmitted jobs 
# Link: https://savannah.cern.ch/bugs/?89508
#
#

import logging
import time

from libutils.Exceptions import *

def run(utils):

    bug='89508'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Get available top level BDIIs")

    BDIIs=utils.run_command_continue_on_error("lcg-infosites --vo %s bdii_top"%(utils.VO)).split("\n")

    logging.info("Query available top level BDIIs to find a CE which doesn't publish GlueCEInfoHostName.")

    ce_info=[]
    ce_id=[]

    if len(BDIIs)==0 or ( len(BDIIs)==1 and len(BDIIs[0])==0) :
        logging.error("Unable to find any top level BDII to query for CE information")
        raise GeneralError("Get availabel top level BDIIs","Unable to find any top level BDII to query for CE information")

    for bdii in BDIIs:

        logging.info("Use BDII: %s"%(bdii))

        H_bdii=bdii.split("/mds-vo-name")[0]

        utils.run_command_continue_on_error("ldapsearch -x -H %s -b mds-vo-name=local,o=grid | egrep 'dn: GlueCEUniqueID|GlueCEInfoHostName' > %s/ces.txt"%(H_bdii,utils.get_tmp_dir()))

        info=utils.run_command_continue_on_error("grep GlueCEInfoHostName %s/ces.txt"%(utils.get_tmp_dir())).split("\n")

        id=utils.run_command_continue_on_error("grep GlueCEUniqueID %s/ces.txt"%(utils.get_tmp_dir())).split("\n")

        if len(id)>len(info):
            ce_info=info
            ce_id=id
            break

    if len(ce_info)==0:
        logging.error("Test not executed. Unable to find a CE which which doesn't publish GlueCEInfoHostName")
        raise GeneralError("Search for a CE which doesn't publish GlueCEInfoHostName","Test not executed. Unable to find a CE which which doesn't publish GlueCEInfoHostName")

    target_ce=''

    logging.info("Extract queue for submission")

    for info in ce_info:
        info=info.split(":")[1].strip(" \n\t")
        for id in ce_id:
            if id.find(info)==-1:
                target_ce=id.split("GlueCEUniqueID=")[1].split(",Mds-Vo-name")[0]
                break

    logging.info("Target CE during test: %s"%(target_ce))
    utils.use_utils_jdl()
    utils.set_destination_ce(utils.get_jdl_file(),target_ce)

    logging.info("Submit job")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Check that job's submitted successfully")

    counter=0

    utils.job_status(JOBID)
    
    while utils.get_job_status().find("Ready")!=-1 or utils.get_job_status().find("Waiting")!=-1 :

            if counter >= 10 :
                logging.error("Job not submitted successfully. Job's status: %s",utils.get_job_status())
                raise TimeOutError("","Job not submitted successfully. Job's status: %s"%(utils.get_job_status()))

            logging.info("Job's %s status is %s ... sleeping %s seconds ( %s/10 )",JOBID,utils.JOBSTATUS,utils.SLEEP_TIME,counter)
            time.sleep(int(utils.SLEEP_TIME))
            counter=counter+1

    utils.wait_until_job_finishes(JOBID)

    logging.info("Check job's final status")

    utils.job_status(JOBID)

    if utils.get_job_status().find("Done") != -1 :
        logging.info("Job finishes with status %s",utils.get_job_status())
    else:
        logging.error("Job finishes with status %s",utils.get_job_status())
        raise GeneralError("","Job finishes with status: %s"%(utils.get_job_status()))
        
    logging.info("Test OK")

    logging.info("End of regression test for bug %s"%(bug))
