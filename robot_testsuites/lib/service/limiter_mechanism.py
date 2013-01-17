
import SSH_utils
import commands

from Exceptions import *

limit_values = [ 

	'--load1 0 --load5 20 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 150000 --ftpconn 300',
	'--load1 22 --load5 0 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 150000 --ftpconn 300',
	'--load1 22 --load5 20 --load15 0.001 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 150000 --ftpconn 300',
	'--load1 22 --load5 20 --load15 18 --memusage 1 --diskusage 95 --fdnum 1000 --jdnum 150000 --ftpconn 300',
	'--load1 22 --load5 20 --load15 18 --memusage 99 --diskusage 99 --swapusage 0.1 --fdnum 1000 --jdnum 150000 --ftpconn 300',
	'--load1 22 --load5 20 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 150000 --ftpconn 0',
	'--load1 22 --load5 20 --load15 18 --memusage 99 --diskusage 1 --fdnum 1000 --jdnum 150000 --ftpconn 300',
	'--load1 22 --load5 20 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000000 --jdnum 150000 --ftpconn 300',
	'--load1 22 --load5 20 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 0 --ftpconn 300',
	'--load1 22 --load5 20 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 150000 --ftpconn 300 --jdsize 0.001'
  
]


def get_limit_values(testid):

    return limit_values[int(testid)-1]


def set_limiter_values(utils,ssh,limit_values):

    try:

        job_submit="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobSubmit %s\""%(limit_values)

        job_register="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobRegister %s\""%(limit_values)

        utils.log_info("Set jobSubmit  = %s; and jobRegister  = %s; to glite_wms.conf at WMS"%(job_submit,job_register))

        SSH_utils.change_remote_file(utils,ssh,"/etc/glite-wms/glite_wms.conf", ['jobSubmit','jobRegister'],['*','*'],  [job_submit,job_register])
   
    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_info('ERROR - Command: %s'%(e.expression)) 
        utils.log_info('ERROR - Message: %s'%(e.message))
        restore_configuration_file(utils,ssh)          


def restore_configuration_file(utils,ssh):

    utils.log_info("Restore initial version of glite-wms.conf file") 
    SSH_utils.execute_remote_cmd(utils,ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
    SSH_utils.execute_remote_cmd(utils,ssh,"/etc/init.d/glite-wms-wmproxy restart")
 
