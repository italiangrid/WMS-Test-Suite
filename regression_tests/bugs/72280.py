#
# Bug: 72280
# Title: WMProxy limiter should log more at info level
# Link: https://savannah.cern.ch/bugs/?72280
#
#

import logging
import time

from libutils.Exceptions import *


def run(utils):

    bug='72280'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    limit_values="--load1 0.0001 --load5 20 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 150000  --ftpconn 300"

    job_submit="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobSubmit %s\""%(limit_values)

    job_register="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobRegister %s\""%(limit_values)

    logging.info("Set jobSubmit  = %s; and jobRegister  = %s; to glite_wms.conf at WMS"%(job_submit,job_register))

    utils.change_remote_file(ssh,"/etc/glite-wms/glite_wms.conf", ['jobSubmit','jobRegister'],['*','*'],[job_submit,job_register])

    #necessary to avoid override of the glite_wms.conf.bak
    utils.execute_remote_cmd(ssh,"cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf.original")

    utils.change_attribute_at_remote_file_section(ssh,"/etc/glite-wms/glite_wms.conf","LogLevel","WorkloadManagerProxy","5")

    logging.info("Clear wmproxy.log file")

    utils.execute_remote_cmd(ssh,"mv /var/log/wms/wmproxy.log /var/log/wms/wmproxy.log_%s"%(time.strftime("%Y%m%d%H%M%S")))

    logging.info("Restart workload manager proxy glite-wms-wmproxy")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

    logging.info("Prepare jdl file for submission")

    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())

    logging.info("Submit a job (submission should be failed)")

    utils.run_command_fail_continue_on_error("glite-wms-job-submit %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Check wmproxy.log file")

    utils.ssh_get_file(ssh, "/var/log/wms/wmproxy.log","%s/local_copy"%(utils.get_tmp_dir()))

    FILE=open("%s/local_copy"%(utils.get_tmp_dir()))
    log_data=' '.join(FILE.readlines())
    FILE.close()

    logging.info("Restore initial version of glite-wms.conf file")
    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.original /etc/glite-wms/glite_wms.conf")
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

    utils.close_ssh(ssh)
    
    logging.info("Check wmproxy.log")

    details=["Fault description","Description: System load is too high:","Threshold for Load Average(1 min): 0.0001 => Detected value for Load Average(1 min):"]

    errors=[]

    for detail in details:
        if log_data.find(detail)==-1:
            errors.append(detail)

    if len(errors)==0:
        logging.info("Test OK")
    else:
        logging.info("Unable to find log information from WMProxy limiter")
        raise GeneralError("Check wmproxy.log","Unable to find log information from WMProxy limiter")
    
    logging.info("End of regression test for bug %s"%(bug))

