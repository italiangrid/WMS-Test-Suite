#
# Bug: 86682
# Title: [yaim-wms] yaim changes ownership of /var
# Link: https://savannah.cern.ch/bugs/?86682
#
#

from lib.Exceptions import *

def run(utils):

    bug='86682'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Check ownership of /var system directory")

    output=utils.execute_remote_cmd(ssh,"ls -ld /var" )

    output=output.split(" ")

    target='root'

    if output[2]!=target or output[3]!=target:
        ssh.close()
        utils.log_info('ERROR: Test failed - Ownership of system directory /var is not %s.%s as expected. Instead we get %s.%s'%(target,target,output[2],output[3]))
        raise GeneralError("Test failed","Ownership of system directory /var is not %s.%s as expected. Instead we get %s.%s"%(target,target,output[2],output[3]))
    else:
        utils.log_info('Ownership of system directory /var is root.root as expected')


    utils.log_info("Check ownership of /var/log system directory")

    output=utils.execute_remote_cmd(ssh,"ls -ld /var/log")

    output=output.split(" ")

    target='root'

    if output[2]!=target or output[3]!=target:
        ssh.close()
        utils.log_info('ERROR: Test failed - Ownership of system directory /var/log is not %s.%s as expected. Instead we get %s.%s'%(target,target,output[2],output[3]))
        raise GeneralError("Test failed","Ownership of system directory /var/log is not %s.%s as expected. Instead we get %s.%s"%(target,target,output[2],output[3]))
    else:
        utils.log_info('Ownership of system directory /var/log is root.root as expected')

    ssh.close()
  
    utils.log_info("End of regression test for bug %s"%bug)
