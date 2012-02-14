#
# Bug: 86682
# Title: [yaim-wms] yaim changes ownership of /var
# Link: https://savannah.cern.ch/bugs/?86682
#
#

import logging

from libutils.Exceptions import *

def run(utils):

    bug='86682'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Check ownership of /var system directory")

    output=utils.execute_remote_cmd(ssh,"ls -ld /var" )

    output=output.split(" ")

    target='root'

    if output[2]!=target or output[3]!=target:
        ssh.close()
        logging.error('Test failed:  Ownership of system directory /var is not %s.%s as expected. Instead we get %s.%s'%(target,target,output[2],output[3]))
        raise GeneralError("Test failed","Ownership of system directory /var is not %s.%s as expected. Instead we get %s.%s"%(target,target,output[2],output[3]))
    else:
        logging.info('Ownership of system directory /var is root.root as expected')


    logging.info("Check ownership of /var/log system directory")

    output=utils.execute_remote_cmd(ssh,"ls -ld /var/log" )

    output=output.split(" ")

    target='root'

    if output[2]!=target or output[3]!=target:
        ssh.close()
        logging.error('Test failed:  Ownership of system directory /var/log is not %s.%s as expected. Instead we get %s.%s'%(target,target,output[2],output[3]))
        raise GeneralError("Test failed","Ownership of system directory /var/log is not %s.%s as expected. Instead we get %s.%s"%(target,target,output[2],output[3]))
    else:
        logging.info('Ownership of system directory /var/log is root.root as expected')


    ssh.close()
  
    logging.info("End of regression test for bug %s",bug)
