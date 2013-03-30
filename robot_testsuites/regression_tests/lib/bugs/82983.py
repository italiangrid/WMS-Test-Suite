#
# Bug: 82983
# Title: [yaim-wms] authorization problem in WMS EMI-1
# Link: https://savannah.cern.ch/bugs/?82983
#
#

from lib.Exceptions import *

def run(utils):

    bug='82983'

    utils.log_info("Start regression test for bug %s"%(bug))
 
    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    file="/etc/glite-wms/glite_wms_wmproxy.gacl"

    utils.log_info("Get file %s from remote host"%(file))

    utils.ssh_get_file(ssh,file,"%s/glite_wms_wmproxy.gacl_local"%(utils.get_tmp_dir()))

    ssh.close()

    utils.log_info("Check if in file glite_wms_wmproxy.gacl there are not entries with the word ROLE in upper case")

    F=open("%s/glite_wms_wmproxy.gacl_local"%(utils.get_tmp_dir()))
    lines=F.readlines()
    F.close()

    error=0

    for line in lines:

      if line.find("ROLE")!=-1:
         error=1

    if error==0:
         utils.log_info("Test OK,  There are not entries in file glite_wms_wmproxy.gacl with the word ROLE in upper case")
    else:
        utils.log_info("ERROR: Test failed - There are entries in file glite_wms_wmproxy.gacl with the word ROLE in upper case")
        raise GeneralError("Test failed","Error !!! There are entries in file glite_wms_wmproxy.gacl with the word ROLE in upper case")

    
    utils.log_info("End of regression test for bug %s"%(bug))
