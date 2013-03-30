#
# Bug: 90640
# Title: cron job deletes /var/proxycache
# Link: https://savannah.cern.ch/bugs/?90640
#
#

from lib.Exceptions import *


def run(utils):

    bug='90640'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())
    
    script = "/usr/bin/glite-wms-wmproxy-purge-proxycache"

    utils.log_info("Check if find at %s uses the '-mindepth 1' option"%(script))
    
    utils.ssh_get_file(ssh,script,"%s/local_copy"%(utils.get_tmp_dir()))

    FILE=open("%s/local_copy"%(utils.get_tmp_dir()))
    lines=FILE.readlines()
    FILE.close()

    cmd_line=''

    for line in lines:
        if line.find("find")!=-1 :
            cmd_line=line.strip(" \n\t")
            break

    if len(cmd_line)==0:
        
        utils.log_info("ERROR: Script %s does not contain find command"%(script))
        raise GeneralError("","Script %s does not contain find command"%(script))

    else:

        if cmd_line.find("-mindepth 1")!=-1 :
            utils.log_info("Check OK")
        else:
            utils.log_info("ERROR: Command does not use the '-mindepth 1' option. We get ( %s )"%(cmd_line))
            raise GeneralError("","Command does not use the '-mindepth 1' option. We get ( %s )"%(cmd_line))

    utils.close_ssh(ssh)

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))
