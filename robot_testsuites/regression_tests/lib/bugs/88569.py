#
# Bug: 88569
# Title: WMS: LCMAPS should log on file only and not on syslog
# Link: https://savannah.cern.ch/bugs/?88569
#
#

import commands

from lib.Exceptions import *


def run(utils):

    bug='88569'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.WMS_USERNAME,utils.WMS_PASSWORD)

    # Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()

    utils.set_jdl(utils.get_jdl_file())

    log_file="/var/log/glite/lcmaps.log"

    utils.log_info("Check if dedicated log file %s exists"%(log_file))

    utils.execute_remote_cmd(ssh,"ls -l %s"%(log_file))

    utils.log_info("Compute number of lines in log file %s before job submission"%(log_file))

    log_file_lines_before=utils.execute_remote_cmd(ssh,"grep LCMAPS %s | wc -l "%(log_file))

    utils.log_info("Submit a job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Cancel submitted job")

    utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))

    utils.log_info("Check that no messages about LCMPAS is logged by the wmproxy on syslog during submission")

    files=utils.execute_remote_cmd(ssh,"ls /var/log/messages*").split(" ")

    counter=0
 
    for file in files:
      file=file.strip(" \n")
      utils.ssh_get_file(ssh, "%s"%(file), "%s/file_%s"%(utils.get_tmp_dir(),counter))
      counter=counter+1

    output=commands.getstatusoutput("grep glite_wms_wmproxy_server %s/file_* | grep -i \"LCMAPS\""%(utils.get_tmp_dir()))

    if output[0]==0: #return code 0 means find messages in syslog
       utils.log_info("ERROR: Find LCMAPS messages by the wmproxy on syslog")
       raise GeneralError("Check syslog for LCMAPS messages by the wmproxy","Find LCMAPS messages by the wmproxy on syslog")
    
    utils.log_info("Check if messages about LCMAPS are saved in dedicated log file: %s"%(log_file))

    log_file_lines_after=utils.execute_remote_cmd(ssh,"grep LCMAPS %s | wc -l "%(log_file))

    if int(log_file_lines_after) > int(log_file_lines_before) :
       utils.log_info("Check OK. Find LCMAPS messages in dedicated log file: %s"%(log_file))
    else:
       utils.log_info("ERROR: Unable to find LCMAPS messages in dedicated log file: %s"%(log_file))
       raise GeneralError("Check dedicated log file %s for LCMAPS messages"%(log_file),"Unable to find LCMAPS messages in dedicated log file:%s"%(log_file))

    utils.log_info("Test OK")

    utils.log_info("End of regression test for bug %s"%(bug))
