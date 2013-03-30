#
# Bug: 78484
# Title: [ YAIM_WMS ] Multiple parameter configuration added in condor_config.local
# Link: https://savannah.cern.ch/bugs/?78484
#
#


from lib.Exceptions import *


def run(utils):

    bug='78484'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Get the list of GRID_MONITOR* variables")

    short_hostname=utils.execute_remote_cmd(ssh,"/bin/hostname -s")[:-1]

    result=utils.execute_remote_cmd(ssh,"cat /opt/condor-c/local.%s/condor_config.local"%(short_hostname))

    result=result.split("\n")

    grid_monitor=[]

    for line in result:
        if line.find("GRID_MONITOR")!=-1:
           grid_monitor.append(line)


    utils.log_info("Run yaim (site-info.def should be presented in /opt/glite/yaim/examples directory)")

    utils.execute_remote_cmd(ssh,"/opt/glite/yaim/bin/yaim -c -s /opt/glite/yaim/examples/site-info.def -n WMS")

    utils.log_info("Get the list of GRID_MONITOR* variables after yaim")

    result=utils.execute_remote_cmd(ssh,"cat /opt/condor-c/local.%s/condor_config.local"%(short_hostname))

    result=result.split("\n")

    grid_monitor_after=[]

    for line in result:
        if line.find("GRID_MONITOR")!=-1:
           grid_monitor_after.append(line)

    
    z=set(grid_monitor)^set(grid_monitor_after)


    if len(z) >0 :
           ssh.close()
           utils.log_info("ERROR: After executing yaim found these new entries: %s"%(z))
           raise GeneralError("Check GRID_MONITOR* variables","After executing yaim found these new entries: %s"%(z))

    utils.log_info("Test OK")

    ssh.close()

    utils.log_info("End of regression test for bug %s"%(bug))
