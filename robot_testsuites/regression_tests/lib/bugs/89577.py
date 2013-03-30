#
# Bug: 85777
# Title: EMI WMS wmproxy init.d script stop/start problems
# Link: https://savannah.cern.ch/bugs/?85777
#
#

import time

from lib.Exceptions import *


def run(utils):

    bug='85777'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
    
    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("CASE 1: Check if restart command for workload manager proxy restart httpd")

    result=utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy status")

    if result.find("is running")==-1:
         utils.log_info("Workload manager proxy is not running , try to start it")
         utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy start")

    utils.log_info("Get pids before restart")

    lines=utils.execute_remote_cmd(ssh,"ps ax -o \"%u : %p : %a\" |  grep http").split("\n")

    pids_before=[]

    for line in lines:
        if line.find("/usr/sbin/httpd")!=-1:
           pids_before.append(line.split(" : ")[1])
                 
    utils.log_info("Restart workload manager proxy")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

    time.sleep(60)

    utils.log_info("Get pids after restart")

    lines=utils.execute_remote_cmd(ssh,"ps ax -o \"%u : %p : %a\" |  grep http").split("\n")

    pids_after=[]

    for line in lines:
        if line.find("/usr/sbin/httpd")!=-1:
           pids_after.append(line.split(" : ")[1])

    if len(pids_before)!=len(pids_after):
        utils.log_info("ERROR: The number of pids don't match after workload manager proxy restart")
        raise GeneralError("Check if restart command for workload manager proxy restart httpd","The number of pids don't match after workload manager proxy restart")

    utils.log_info("Check the returned pids before and after workload manager proxy restart")

    z=set(pids_before)&set(pids_after)

    if len(z)>0:
        utils.log_info("ERROR : The restart command for workload manager proxy don't restart httpd. pids before: %s , pids after: %s"%(" , ".join(pids_before)," , ".join(pids_after)))
        raise GeneralError("Check if restart command for workload manager proxy restart httpd","Restart command for workload manager proxy don't restart httpd. pids before: %s , pids after: %s"%(" , ".join(pids_before)," , ".join(pids_after)))

    utils.log_info("Case 2:  A start immediately following a stop often fails and has to be repeated to get the service working again")

    utils.log_info("Stop workload manager and imeediately start it")
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy stop; /etc/init.d/glite-wms-wmproxy start")

    utils.log_info("Check workload manager proxy status")

    output=utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy status")

    if output.find("is running")!=-1:
         utils.log_info("Workload manager proxy is running as expected")
    else:
         utils.log_info("ERROR: Test Failed. Workload manager proxy is not running")
         raise GeneralError("Check workload manager proxy status","Workload manager proxy is not running")


    utils.log_info("Case 3: Try to stop and start workload manager proxy via ssh")

    stdin,stdout,stderr=ssh.exec_command("/etc/init.d/glite-wms-wmproxy stop;/etc/init.d/glite-wms-wmproxy start")

    errors=stderr.readlines()

    if len(errors)>0:
         ssh.close()
         utils.log_info("ERROR: Test failed - During the workload manager proxy restart via ssh we get the following error: %s"%(' '.join(errors)))
         raise GeneralError("Test failed","During the workload manager proxy restart via ssh we get the following error: %s"%(' '.join(errors)))

    utils.log_info("Command Output: %s",' '.join(stdout))

    utils.log_info("Check workload manager proxy status")

    output=utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy status")

    if output.find("is running")!=-1:
         utils.log_info("Workload manager proxy is running as expected")
    else:
         utils.log_info("ERROR: Test Failed. Workload manager proxy is not running")
         raise GeneralError("Check workload manager proxy status","Workload manager proxy is not running")

    utils.log_info("Test OK, workload manager proxy restart via ssh was successful")

    utils.close_ssh(ssh)

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))
