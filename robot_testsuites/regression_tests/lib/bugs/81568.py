#
# Bug: 81568
# Title: some inconsistencies in locations for logs and configuration
# Link: https://savannah.cern.ch/bugs/?81568
#
#

from lib.Exceptions import *

def run(utils):

    bug='81568'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Check the environment variable WMS_LOCATION_LOG")

    output=utils.execute_remote_cmd(ssh,"echo $WMS_LOCATION_LOG").strip(" \n")

    target='/var/log/glite'

    if output!=target:
        ssh.close()
        utils.log_info("ERROR: Test failed - Environment variable WMS_LOCAITON_LOG is %s instead of %s"%(output,target))
        raise GeneralError("Test failed","Error !!! Environment  variable WMS_LOCATION_LOG is %s instead of %s"%(output,target))
    else:
        utils.log_info("Environment variable WMS_LOCATION_LOG is %s as expected"%(target))

    utils.log_info("Check for file /etc/wmproxy_logrotate.conf")

    stdin,stdout,stderr=ssh.exec_command("ls /etc/wmproxy_logrotate.conf")

    errors=stderr.readlines()
    output_lines=stdout.readlines()

    output=' '.join(output_lines)

    if len(errors)!=0 :        
        utils.log_info('File /etc/wmproxy_logrotate.conf not exist as expected')
    else:
        ssh.close()
        utils.log_info('ERROR: Test failed - File /etc/wmproxy_logrotate.conf exists while should not exist')
        raise GeneralError("Test failed","File /etc/wmproxy_logrotate.conf exists while should not exist")

 
    utils.log_info("Check for wmproxy_logrotate.conf at $GLITE_WMS_CONFIG_DIR")

    stdin,stdout,stderr=ssh.exec_command("ls $GLITE_WMS_CONFIG_DIR/wmproxy_logrotate.conf")

    errors=stderr.readlines()
    output_lines=stdout.readlines()

    output=' '.join(output_lines)

    if len(errors)!=0 :
        ssh.close()
        utils.log_info('ERROR: Test failed - File wmproxy_logrotate.conf is not at $GLITE_WMS_CONFIG_DIR as expected')
        raise GeneralError("Test failed","File wmproxy_logrotate.conf is not at $GLITE_WMS_CONFIG_DIR as expected")
    else:
        utils.log_info('File wmproxy_logrotate.conf is at $GLITE_WMS_CONFIG_DIR as expected')
       
    ssh.close()
  
    utils.log_info("End of regression test for bug %s"%bug)
