#
# Bug: 96136
# Title: WMS stops accepting submissions when no swap is available
# Link: https://savannah.cern.ch/bugs/?96136
#
#


from lib.Exceptions import *


def run(utils):

    bug='96136'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())
  
    utils.log_info("Get available swap partitions at WMS host")
 
    output=utils.execute_remote_cmd(ssh,"cat /proc/swaps")

    swaps=[]

    for line in output.split("\n"):
        if len(line)>0 and line.find("Filename")==-1:
           line=line.strip()
           swaps.append(line.split(" ")[0])

    utils.log_info("Disable all available swap partitions")

    for swap in swaps:
        utils.execute_remote_cmd(ssh,"swapoff %s"%(swap))

    utils.log_info("Check that all swap partitions have been disabled")

    output=utils.execute_remote_cmd(ssh,"cat /proc/swaps")

    sw=[]

    for line in output.split("\n"):
        if len(line)>0 and line.find("Filename")==-1:
           line=line.strip()
           sw.append(line.split(" ")[0])

    if len(sw)==0:
        utils.log_info("All swap partitions have been disabled")
    else:
        utils.log_info("ERROR: There are swap partitions enabled: %s"%(sw))
        for swap in swaps:
           utils.execute_remote_cmd(ssh,"swapon %s"%(swap))
        raise GeneralError("Check that all swap partitions have been disable","There are swap partitions enabled: %s"%(sw))

    utils.log_info("Try to submit a job")

    try:

       utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    except:
       utils.log_info("ERROR: Submission failed")
       utils.log_info("Enable again all swap partitions")
       for swap in swaps:
           utils.execute_remote_cmd(ssh,"swapon %s"%(swap))
       raise GeneralError("","Job submission failed")

    utils.log_info("Job submitted successfully")

    utils.log_info("Enable again all swap partitions")

    for swap in swaps:
        utils.execute_remote_cmd(ssh,"swapon %s"%(swap))

    utils.close_ssh(ssh)

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))

