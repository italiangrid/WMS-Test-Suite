#
# Bug: 78484
# Title: [ YAIM_WMS ] Multiple parameter configuration added in condor_config.local
# Link: https://savannah.cern.ch/bugs/?78484
#
#

import logging

from libutils.Exceptions import *

def run(utils):

    bug='78484'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Get the list of GRID_MONITOR* variables")

    short_hostname=utils.execute_remote_cmd(ssh,"/bin/hostname -s")[:-1]

    result=utils.execute_remote_cmd(ssh,"cat /opt/condor-c/local.%s/condor_config.local"%(short_hostname))

    result=result.split("\n")

    grid_monitor=[]

    for line in result:
        if line.find("GRID_MONITOR")!=-1:
           grid_monitor.append(line)


    logging.info("Run yaim (site-info.def should be presented in /opt/glite/yaim/examples/siteinfo directory)")

    utils.execute_remote_cmd(ssh,"/opt/glite/yaim/bin/yaim -c -s /opt/glite/yaim/examples/siteinfo/site-info.def -n WMS")

    logging.info("Get the list of GRID_MONITOR* variables after yaim")

    result=utils.execute_remote_cmd(ssh,"cat /opt/condor-c/local.%s/condor_config.local"%(short_hostname))

    result=result.split("\n")

    grid_monitor_after=[]

    for line in result:
        if line.find("GRID_MONITOR")!=-1:
           grid_monitor_after.append(line)

    
    z=set(grid_monitor)^set(grid_monitor_after)


    if len(z) >0 :
           ssh.close()
           logging.error("Error!!!. After yaim found these new entries: %s"%(z))
           raise GeneralError("Check GRID_MONITOR* variables","After yaim found these new entries: %s"%(z))

    logging.info("Test OK")

    ssh.close()

    logging.info("End of regression test for bug %s"%(bug))
