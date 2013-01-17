#
# Bug: 90640
# Title: cron job deletes /var/proxycache
# Link: https://savannah.cern.ch/bugs/?90640
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='90640'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())
    
    script = "/usr/bin/glite-wms-wmproxy-purge-proxycache"

    logging.info("Check if find at %s uses the '-mindepth 1' option"%(script))
    
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
        
        logging.error("Script %s does not contain find command"%(script))
        raise GeneralError("","Script %s does not contain find command"%(script))

    else:

        if cmd_line.find("-mindepth 1")!=-1 :
            logging.info("Check OK")
        else:
            logging.error("Command does not use the '-mindepth 1' option. We get ( %s )"%(cmd_line))
            raise GeneralError("","Command does not use the '-mindepth 1' option. We get ( %s )"%(cmd_line))

    utils.close_ssh(ssh)

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
