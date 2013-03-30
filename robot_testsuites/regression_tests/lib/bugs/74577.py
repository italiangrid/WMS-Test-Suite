#
# Bug:74577
# Title: Wrong counter in ICE database is set at the job creation
# Link: https://savannah.cern.ch/bugs/?74577
#
#

import time

from lib.Exceptions import *


def run(utils):

    bug='74577'

    utils.log_info("Start regression test for bug %s"%(bug))
  
    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    utils.log_info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())
    utils.add_jdl_attribute(utils.get_jdl_file(),'MyProxyServer',"%s"%utils.get_MYPROXY_SERVER())

    utils.set_destination_ce(utils.get_jdl_file(),'/cream-')

    #Get current user identity ant primary attribute
    result=utils.run_command("voms-proxy-info -all")

    for line in result.split("\n"):
        if line.find("identity")!=-1:
            identity=line.split(":")[1].strip()
        if line.find("attribute")!=-1: 
            attribute=line.split(":")[1].strip()
            break

 
    utils.log_info("Connect to WMS host: %s"%(utils.get_WMS()))

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Query database for counter value before job submission")

    CMD="sqlite3 /var/ice/persist_dir/ice.db \"select counter from proxy where myproxyurl='%s' and userdn like '%s-%s%%';\""%(utils.get_MYPROXY_SERVER(),identity, attribute)

    value_before=utils.execute_remote_cmd(ssh,CMD)

    value_before=value_before.strip(' \n')

    if len(value_before)==0:
        value_before=0

    utils.log_info("Submit the job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    time.sleep(20)

    utils.log_info("Query database for counter value after job submission")
  
    value_after=utils.execute_remote_cmd(ssh,CMD)

    value_after=value_after.strip(' \n')

    if len(value_after)==0 :
        value_after=0

    ssh.close()
 
    utils.log_info("Cancel the submitted job")

    utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))

    utils.log_info("Check if values of attribute counter differ by one")

    if int(value_after)-int(value_before) == 1 :
        utils.log_info("The counter has been increased by one as expected")
    else:
      utils.log_info("ERROR: Wrong counter value. Get %s while before submission was %s"%(value_after,value_before))
      raise GeneralError("","Error !!! Counter value has not been increased by one as expected. Get %s while before submission was %s"%(value_after,value_before))
       
    
    utils.log_info("End of regression test for bug %s"%(bug))
