#
# task #23845
# Title: Semi-automated service backends configuration for WMS
# Link: https://savannah.cern.ch/task/?23845
#
#

import logging

from libutils.Exceptions import *

def run(utils):

    bug='task23845'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Get /etc/my.cnf file from WMS")

    utils.ssh_get_file(ssh,"/etc/my.cnf","%s/my.cnf"%(utils.get_tmp_dir()))

    ssh.close()

    FILE=open("%s/my.cnf"%(utils.get_tmp_dir()))
    lines=FILE.readlines()
    FILE.close()

    logging.info("Gheck for expected attributes innodb_flush_log_at_trx_commit and innodb_buffer_pool_size in the my.cnf file")

    innodb_flush=''
    innodb_buffer=''
    
    for line in lines:
        if line.find("innodb_flush_log_at_trx_commit=2")!=-1:
            innodb_flush=line
        if line.find("innodb_buffer_pool_size=500M")!=-1:
            innodb_buffer=line

    if len(innodb_flush)==0:
        logging.error("Unable to find the expected setting innodb_flush_log_at_trx_commit=2 in the /etc/my.cnf file")
        raise GeneralError("Check for setting innodb_flush_log_at_trx_commit","Unable to find the expected setting innodb_flush_log_at_trx_commit=2 in the /etc/my.cnf file")
    else:
        logging.info("Find the expected setting innodb_flush_log_at_trx_commit=2 in the /etc/my.cnf file")

    if len(innodb_buffer)==0:
        logging.error("Unable to find the expected setting innodb_buffer_pool_size=500M in the /etc/my.cnf file")
        raise GeneralError("Check for setting innodb_buffer_pool_size","Unable to find the expected setting innodb_buffer_pool_size=500M in the /etc/my.cnf file")
    else:
        logging.info("Find the expected setting innodb_buffer_pool_size=500M in the /etc/my.cnf file")

    logging.info("Test OK")

    logging.info("End of regression test for bug %s"%(bug))
