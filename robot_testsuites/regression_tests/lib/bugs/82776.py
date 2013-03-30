#
# Bug: 82776
# Title: Typo in WMS jobwrapper
# Link: https://savannah.cern.ch/bugs/?82776
#
#

from lib.Exceptions import *

def run(utils):

    bug='82776'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    file="/usr/share/glite-wms/jobwrapper.template.sh"

    utils.log_info("Get file %s from remote host"%(file))

    utils.ssh_get_file(ssh,file,"%s/jobwrapper.template.sh_local"%(utils.get_tmp_dir()))

    ssh.close()

    utils.log_info("Check if a space is inserted beetween push_in_LM_done_reason and the following word 'Taken...'")

    F=open("%s/jobwrapper.template.sh_local"%(utils.get_tmp_dir()))
    lines=F.readlines()
    F.close()

    ok=0

    for line in lines:

      if line.find("push_in_LM_done_reason \"Taken")!=-1:
         ok=1

    
    if ok==1:
         utils.log_info("Test OK, space is  found beetween push_in_LM_done_reason and the following word 'Taken...'")
    else:
         utils.log_info("ERROR: Test failed: Space is not inserted beetween push_in_LM_done_reason and the following word 'Taken...' ")
         raise GeneralError("Test failed","Error !!! Space is not inserted beetween push_in_LM_done_reason and the following word 'Taken...'")

    utils.log_info("End of regression test for bug %s"%bug)
