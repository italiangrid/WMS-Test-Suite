#
# Bug: 82776
# Title: Typo in WMS jobwrapper
# Link: https://savannah.cern.ch/bugs/?82776
#
#


import logging

from libutils.Exceptions import *

def run(utils):

    bug='82776'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    file="/usr/share/glite-wms/jobwrapper.template.sh"

    logging.info("Get file %s from remote host"%(file))

    utils.ssh_get_file(ssh,file,"%s/jobwrapper.template.sh_local"%(utils.get_tmp_dir()))

    ssh.close()

    logging.info("Check if a space is inserted beetween push_in_LM_done_reason and the following word 'Taken...'")

    F=open("%s/jobwrapper.template.sh_local"%(utils.get_tmp_dir()))
    lines=F.readlines()
    F.close()

    ok=0

    for line in lines:

      if line.find("push_in_LM_done_reason \"Taken")!=-1:
         ok=1

    
    if ok==1:
         logging.info("Test OK, space is  found beetween push_in_LM_done_reason and the following word 'Taken...'")
    else:
        logging.error("Test failed: Space is not inserted beetween push_in_LM_done_reason and the following word 'Taken...' ")
        raise GeneralError("Test failed","Error !!! Space is not inserted beetween push_in_LM_done_reason and the following word 'Taken...'")

    
    logging.info("End of regression test for bug %s",bug)
