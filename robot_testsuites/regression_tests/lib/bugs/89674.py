#
# Bug: 89674
# Title: glite-wms-check-daemons.sh should not restart daemons under the admin's nose
# Link: https://savannah.cern.ch/bugs/?89674
#
#


from lib.Exceptions import *


def run(utils):

    bug='89674'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Stop workload manager")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm stop")

    utils.log_info("Check if workload manager is not running")

    output=utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm status")

    if output.find("is not running")!=-1:
        utils.log_info("Workload Manager is stopped as expected")
    else:
        utils.log_info("ERROR: Workload Manager is not stopped as expected")
        raise GeneralError("Check Workload Manager status","Workload Manager is not stopped as expected")
        
    utils.log_info("Check /etc/cron.d/glite-wms-check-daemons.cron for executable script")

    output=utils.execute_remote_cmd(ssh,"cat /etc/cron.d/glite-wms-check-daemons.cron").split("\n")

    script=''

    for line in output:
        if line.find("glite-wms-check-daemons.sh")!=-1:
             script=line.split(" ; ")[1].split(" > ")[0]

    utils.log_info("Execute glite-wms-check-daemons.sh script")

    utils.execute_remote_cmd(ssh,script)

    utils.log_info("Check Workload Manager's status")

    output=utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm status")

    if output.find("is not running")!=-1:
         utils.log_info("glite-wms-check-daemons.sh script did't start Workload Manager as expected")
    else:
         utils.log_info("ERROR: Test Failed. glite-wms-check-daemons.sh script started Workload Manager")
         raise GeneralError("Check Workload Manager's status","glite-wms-check-daemons.sh script started Workload Manager")


    utils.log_info("Start Workload Manager")

    output=utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm start")

    output=utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm status")

    if output.find("is running")!=-1:
        utils.log_info("Workload Manager is started as expected")
    else:
        utils.log_info("ERROR: Workload Manager is not started as expected")
        raise GeneralError("Check Workload Manager status","Workload Manager is not started as expected")

    utils.log_info("Execute glite-wms-check-daemons.sh script")

    output=utils.execute_remote_cmd(ssh,script)

    if output.find("stopping workload manager... ok")!=-1 and output.find("starting workload manager... ok")!=-1 :
        utils.log_info("glite-wms-check-daemons.sh script restart workload manager as expected")
    else:
        utils.log_info("ERROR: glite-wms-check-daemons.sh script didn't restart workload manager")
        raise GeneralError("Execute glite-wms-check-daemons.sh script","glite-wms-check-daemons.sh script didn't restart workload manager")

    utils.log_info("Check Workload Manager's status")

    output=utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm status")

    if output.find("is running...")!=-1:
         utils.log_info("glite-wms-check-daemons.sh script restart Workload Manager as expected")
    else:
         utils.log_info("ERROR: Test Failed. glite-wms-check-daemons.sh didn't rescript started Workload Manager")
         raise GeneralError("Check Workload Manager's status","glite-wms-check-daemons.sh script didn't restart Workload Manager")

    utils.close_ssh(ssh)

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))
