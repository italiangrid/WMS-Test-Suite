#
# Bug: 91834
# Title:  Pid file of ICE and WM has glite ownership
# Link: https://savannah.cern.ch/bugs/?91834
#
#

import logging

from libutils.Exceptions import *

def run(utils):

    bug='91834'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Stop Workload Manager")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm stop")

    logging.info("Stop ICE")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-ice stop")
     
    logging.info("Remove any previous pid files")

    utils.execute_remote_cmd(ssh,"rm /var/run/glite-wms-workload_manager.pid")
    utils.execute_remote_cmd(ssh,"rm /var/run/glite-wms-ice-safe.pid")

    logging.info("Start Workload Manager and ICE")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm start")
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-ice start")

    logging.info("Check ownership of WM pid file")

    output=utils.execute_remote_cmd(ssh,"ls -l /var/run/glite-wms-workload_manager.pid" )
    
    output=output.split(" ")

    target='root'

    if output[2]!=target or output[3]!=target:
        ssh.close()
        logging.error('Test failed:  Ownership of WM pid file is not %s.%s as expected. Instead we get %s.%s'%(target,target,output[2],output[3]))
        raise GeneralError("Test failed","Ownership of WM pid file is not %s.%s as expected. Instead we get %s.%s"%(target,target,output[2],output[3]))
    else:
        logging.info('Ownership of WM pid file is root.root as expected')

    logging.info("Check ownership of ICE pid file")

    output=utils.execute_remote_cmd(ssh,"ls -l /var/run/glite-wms-ice-safe.pid" )

    output=output.split(" ")

    target='root'

    if output[2]!=target or output[3]!=target:
        ssh.close()
        logging.error('Test failed:  Ownership of ICE pid file is not %s.%s as expected. Instead we get %s.%s'%(target,target,output[2],output[3]))
        raise GeneralError("Test failed","Ownership of ICE pid file is not %s.%s as expected. Instead we get %s.%s"%(target,target,output[2],output[3]))
    else:
        logging.info('Ownership of ICE pid file is root.root as expected')

    
    ssh.close()
  
    logging.info("End of regression test for bug %s",bug)
