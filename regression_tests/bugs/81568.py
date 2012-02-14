#
# Bug: 81568
# Title: some inconsistencies in locations for logs and configuration
# Link: https://savannah.cern.ch/bugs/?81568
#
#


import logging

from libutils.Exceptions import *

def run(utils):

    bug='81568'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Check the environment variable WMS_LOCATION_LOG")

    output=utils.execute_remote_cmd(ssh,"echo $WMS_LOCATION_LOG").strip(" \n")

    target='/var/log/wms'

    if output!=target:
        ssh.close()
        logging.error("Test failed: Environment variable WMS_LOCAITON_LOG is %s instead of %s"%(output,target))
        raise GeneralError("Test failed","Error !!! Environment  variable WMS_LOCATION_LOG is %s instead of %s"%(output,target))
    else:
       logging.info("Environment variable WMS_LOCATION_LOG is %s as expected"%(target))

    logging.info("Check for file /etc/wmproxy_logrotate.conf")

    stdin,stdout,stderr=ssh.exec_command("ls /etc/wmproxy_logrotate.conf")

    errors=stderr.readlines()
    output_lines=stdout.readlines()

    output=' '.join(output_lines)

    if len(errors)!=0 :        
        logging.info('File /etc/wmproxy_logrotate.conf not exist as expected')
    else:
        ssh.close()
        logging.error('Test failed: File /etc/wmproxy_logrotate.conf exists while should not exist')
        raise GeneralError("Test failed","File /etc/wmproxy_logrotate.conf exists while should not exist")

 
    logging.info("Check for wmproxy_logrotate.conf at $GLITE_WMS_CONFIG_DIR")

    stdin,stdout,stderr=ssh.exec_command("ls $GLITE_WMS_CONFIG_DIR/wmproxy_logrotate.conf")

    errors=stderr.readlines()
    output_lines=stdout.readlines()

    output=' '.join(output_lines)

    if len(errors)!=0 :
        ssh.close()
        logging.error('Test failed:  File wmproxy_logrotate.conf is not at $GLITE_WMS_CONFIG_DIR as expected')
        raise GeneralError("Test failed","File wmproxy_logrotate.conf is not at $GLITE_WMS_CONFIG_DIR as expected")
    else:
        logging.info('File wmproxy_logrotate.conf is at $GLITE_WMS_CONFIG_DIR as expected')
       
    ssh.close()
  
    logging.info("End of regression test for bug %s",bug)
