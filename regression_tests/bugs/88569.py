#
# Bug: 88569
# Title: WMS: LCMAPS should log on file only and not on syslog
# Link: https://savannah.cern.ch/bugs/?88569
#
#

import logging
import commands

from libutils.Exceptions import *


def run(utils):

    bug='88569'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.WMS_USERNAME,utils.WMS_PASSWORD)

    # Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()

    utils.set_jdl(utils.get_jdl_file())

    log_file="/var/log/glite/lcmaps.log"

    logging.info("Check if dedicated log file %s exists"%(log_file))

    utils.execute_remote_cmd(ssh,"ls -l %s"%(log_file))

    logging.info("Compute number of lines in log file %s before job submission"%(log_file))

    log_file_lines_before=utils.execute_remote_cmd(ssh,"grep LCMAPS %s | wc -l "%(log_file))

    logging.info("Submit a job")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Cancel submitted job")

    utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))

    logging.info("Check that no messages about LCMPAS is logged by the wmproxy on syslog during submission")

    files=utils.execute_remote_cmd(ssh,"ls /var/log/messages*").split(" ")

    counter=0
 
    for file in files:
      file=file.strip(" \n")
      utils.ssh_get_file(ssh, "%s"%(file), "%s/file_%s"%(utils.get_tmp_dir(),counter))
      counter=counter+1

    output=commands.getstatusoutput("grep glite_wms_wmproxy_server %s/file_* | grep -i \"LCMAPS\""%(utils.get_tmp_dir()))

    if output[0]==0: #return code 0 means find messages in syslog
       logging.error("Find LCMAPS messages by the wmproxy on syslog")
       raise GeneralError("Check syslog for LCMAPS messages by the wmproxy","Find LCMAPS messages by the wmproxy on syslog")
    
    logging.info("Check if messages about LCMAPS are saved in dedicated log file: %s"%(log_file))

    log_file_lines_after=utils.execute_remote_cmd(ssh,"grep LCMAPS %s | wc -l "%(log_file))

    if int(log_file_lines_after) > int(log_file_lines_before) :
       logging.info("Check OK. Find LCMAPS messages in dedicated log file: %s"%(log_file))
    else:
       logging.error("Unable to find LCMAPS messages in dedicated log file: %s"%(log_file))
       raise GeneralError("Check dedicated log file %s for LCMAPS messages"%(log_file),"Unable to find LCMAPS messages in dedicated log file:%s"%(log_file))

    logging.info("Test OK")

    logging.info("End of regression test for bug %s"%(bug))
