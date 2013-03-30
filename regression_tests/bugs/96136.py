#
# Bug: 96136
# Title: WMS stops accepting submissions when no swap is available
# Link: https://savannah.cern.ch/bugs/?96136
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='96136'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())
  
    logging.info("Get available swap partitions at WMS host")
 
    output=utils.execute_remote_cmd(ssh,"cat /proc/swaps")

    swaps=[]

    for line in output.split("\n"):
        if len(line)>0 and line.find("Filename")==-1:
           line=line.strip()
           swaps.append(line.split(" ")[0])

    logging.info("Disable all available swap partitions")

    for swap in swaps:
        utils.execute_remote_cmd(ssh,"swapoff %s"%(swap))

    logging.info("Check that all swap partitions have been disabled")

    output=utils.execute_remote_cmd(ssh,"cat /proc/swaps")

    sw=[]

    for line in output.split("\n"):
        if len(line)>0 and line.find("Filename")==-1:
           line=line.strip()
           sw.append(line.split(" ")[0])

    if len(sw)==0:
        logging.info("All swap partitions have been disabled")
    else:
        logging.error("There are swap partitions enabled: %s"%(sw))
        for swap in swaps:
           utils.execute_remote_cmd(ssh,"swapon %s"%(swap))
        raise GeneralError("Check that all swap partitions have been disable","There are swap partitions enabled: %s"%(sw))

    logging.info("Try to submit a job")

    try:

       utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    except:
       logging.error("Submission failed")
       logging.info("Enable again all swap partitions")
       for swap in swaps:
           utils.execute_remote_cmd(ssh,"swapon %s"%(swap))
       raise GeneralError("","Job submission failed")

    logging.info("Job submitted successfully")

    logging.info("Enable again all swap partitions")

    for swap in swaps:
        utils.execute_remote_cmd(ssh,"swapon %s"%(swap))

    utils.close_ssh(ssh)

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))

