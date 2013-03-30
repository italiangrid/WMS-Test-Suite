#
# Bug:77004
# Title: Wrong myproxyserver string processing in ICE
# Link: https://savannah.cern.ch/bugs/?77004
#
#


from lib.Exceptions import *


def run(utils):

    bug='77004'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
 
    utils.log_info("Prepare jdl file for submission")

    utils.use_external_jdl("%s.jdl"%(bug))
    
    #Get current user identity
    result=utils.run_command("voms-proxy-info")

    for line in result.split("\n"):
        if line.find("identity") !=-1 :
           identity=line.split(":")[1].strip()


    utils.log_info("Submit the job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Connect to WMS host: %s"%(utils.get_WMS()))

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Query database table proxy of ice in the WMS")

    CMD="sqlite3 /var/ice/persist_dir/ice.db \"select myproxyurl from proxy where userdn like '%s%%';\""%(identity)

    result=utils.execute_remote_cmd(ssh,CMD)
   
    result=result.strip(' \n')

    ssh.close()
 
    utils.log_info("Cancel the submitted job")

    utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))

    utils.log_info("Check if command's output is empty")

    if len(result) == 0 :
        utils.log_info("Field myproxyurl is empty as expected")
    else:
      utils.log_info("ERROR: Field 'myproxyurl' is not empty as expected. Get %s while nothing expected"%(result))
      raise GeneralError("","Error !!! Field 'myproxyurl' is not empty as expected. Get %s while nothing expected "%(result))
       
    
    utils.log_info("End of regression test for bug %s"%(bug))
