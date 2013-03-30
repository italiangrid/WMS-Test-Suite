#
# Bug: 91834
# Title:  Pid file of ICE and WM has glite ownership
# Link: https://savannah.cern.ch/bugs/?91834
#
#

from lib.Exceptions import *

def run(utils):

    bug='91834'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Stop Workload Manager")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm stop")

    utils.log_info("Stop ICE")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-ice stop")
     
    utils.log_info("Remove any previous pid files")

    utils.execute_remote_cmd(ssh,"rm -f /var/run/glite-wms-workload_manager.pid")
    utils.execute_remote_cmd(ssh,"rm -f /var/run/glite-wms-ice-safe.pid")

    utils.log_info("Start Workload Manager and ICE")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm start")
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-ice start")

    utils.log_info("Check ownership of WM pid file")

    output=utils.execute_remote_cmd(ssh,"ls -l /var/run/glite-wms-workload_manager.pid" )
    
    output=output.split(" ")

    target='root'

    if output[2]!=target or output[3]!=target:
        ssh.close()
        utils.log_info('ERROR: Test failed - Ownership of WM pid file is not %s.%s as expected. Instead we get %s.%s'%(target,target,output[2],output[3]))
        raise GeneralError("Test failed","Ownership of WM pid file is not %s.%s as expected. Instead we get %s.%s"%(target,target,output[2],output[3]))
    else:
        utils.log_info('Ownership of WM pid file is root.root as expected')

    utils.log_info("Check ownership of ICE pid file")

    output=utils.execute_remote_cmd(ssh,"ls -l /var/run/glite-wms-ice-safe.pid" )

    output=output.split(" ")

    target='root'

    if output[2]!=target or output[3]!=target:
        ssh.close()
        utils.log_info('ERROR: Test failed - Ownership of ICE pid file is not %s.%s as expected. Instead we get %s.%s'%(target,target,output[2],output[3]))
        raise GeneralError("Test failed","Ownership of ICE pid file is not %s.%s as expected. Instead we get %s.%s"%(target,target,output[2],output[3]))
    else:
        utils.log_info('Ownership of ICE pid file is root.root as expected')

    
    ssh.close()
  
    utils.log_info("End of regression test for bug %s"%(bug))
