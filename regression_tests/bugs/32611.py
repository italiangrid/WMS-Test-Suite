#
# Bug:32611
# Title: JobController logfile name is misspelled
# Link: https://savannah.cern.ch/bugs/?32611
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='32611'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.ssh_get_file(ssh,"/etc/glite-wms/glite_wms.conf", "%s/local_copy"%(utils.get_tmp_dir()))

    logging.info("Check JobController logfile name")

    FILE=open("%s/local_copy"%(utils.get_tmp_dir()))
    lines=FILE.readlines()
    FILE.close()
    
    start_index=lines.index("JobController =  [\n")

    lines=lines[start_index:]

    logfile=''

    for line in lines:
        if line.find("LogFile")!=-1:
            logfile=line
            break

    if logfile.find("jobcontroller_events.log")!=-1:
        logging.info("Logfile name is as expected")
    else:
        logging.error("Test failed, JobController logfile name is misspelled. Get: %s , while expected jobcontroller_events.log"%(logfile))
        raise GeneralError("Check logfile name","Test failed, JobController logfile name is misspelled. Get: %s , while expected jobcontroller_events.log"%(logfile))

    utils.close_ssh(ssh)

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
