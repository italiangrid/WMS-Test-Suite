#! /usr/bin/python

import sys
import signal
import traceback

from Exceptions import *

import Test_utils
import SSH_utils


def test1(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        limit_values="--load1 0.001 --load5 20 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 150000  --ftpconn 300"

        job_submit="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobSubmit %s\""%(limit_values)

        job_register="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobRegister %s\""%(limit_values)

        utils.info("Set jobSubmit  = %s; and jobRegister  = %s; to glite_wms.conf at WMS"%(job_submit,job_register))

        SSH_utils.change_remote_file(utils,ssh,"/etc/glite-wms/glite_wms.conf", ['jobSubmit','jobRegister'],['*','*'],[job_submit,job_register])
        
        utils.info("Restart workload manager proxy glite-wms-wmproxy")

        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

        utils.set_isb_jdl(utils.get_jdl_file())

        utils.info("Submit a job , submission should be failed")
        
        OUTPUT=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()),1).split("\n")

        utils.info("Check failed message")

        find=0

        for line in OUTPUT:
            if line.find("System load is too high")!=-1:
                utils.info("Check OK, the detected failure reason is: 'System load is too high'")
                find=1
                break

        if find==0:
            utils.error("Faulure reason is not 'System load is too high' as expected.")
            raise GeneralError("Check faulure reason","Failure reason is not 'System load is too high' as expected")

        utils.info("Check if the detected threshold is for parameter --load1, 'Load Average(1 min)'")

        find=0

        for line in OUTPUT:
            if line.find("Threshold for Load Average(1 min):")!=-1:
                utils.info("Check OK, detected threshold is for parameter --load1 'Load Average(1 min)' as expected")
                find=1
                break

        if find==0:
            utils.error("Detected thershold is not for parameter load1 ('Load Average(1 min)') as expected")
            raise GeneralError("Check the parameter of the limiter mechanism","Detected threshold is not for parameter load1 ('Load Average(1 min)') as expected ")


        for line in OUTPUT:
            if line.find("Method")!=-1:
               utils.info("Get Method: %s"%(line))
               break
        
        utils.info("Test OK")
    
        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
       
        
    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
        return 1

    return 0

def test2(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        limit_values="--load1 22 --load5 0.01 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 150000  --ftpconn 300"

        job_submit="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobSubmit %s\""%(limit_values)

        job_register="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobRegister %s\""%(limit_values)

        utils.info("Set jobSubmit  = %s; and jobRegister  = %s; to glite_wms.conf at WMS"%(job_submit,job_register))

        SSH_utils.change_remote_file(utils,ssh,"/etc/glite-wms/glite_wms.conf", ['jobSubmit','jobRegister'],['*','*'],[job_submit,job_register])

        utils.info("Restart workload manager proxy glite-wms-wmproxy")

        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

        utils.set_isb_jdl(utils.get_jdl_file())

        utils.info("Submit a job , submission should be failed")

        OUTPUT=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()),1).split("\n")

        utils.info("Check failed message")

        find=0

        for line in OUTPUT:
            if line.find("System load is too high")!=-1:
                utils.info("Check OK, the detected failure reason is: 'System load is too high'")
                find=1
                break

        if find==0:
            utils.error("Faulure reason is not 'System load is too high' as expected.")
            raise GeneralError("Check faulure reason","Failure reason is not 'System load is too high' as expected")

        utils.info("Check if the detected threshold is for parameter --load5, 'Load Average(5 min)'")

        find=0

        for line in OUTPUT:
            if line.find("Threshold for Load Average(5 min):")!=-1:
                utils.info("Check OK, detected threshold is for parameter --load5 'Load Average5 min)' as expected")
                find=1
                break

        if find==0:
            utils.error("Detected threshold is not for parameter load5 ('Load Average(5 min)') as expected")
            raise GeneralError("Check the parameter of the limiter mechanism","Detected threshold is not for parameter load5 ('Load Average(5 min)') as expected ")


        for line in OUTPUT:
            if line.find("Method")!=-1:
               utils.info("Get Method: %s"%(line))
               break

        utils.info("Test OK")

        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
        return 1

    return 0


def test3(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        limit_values="--load1 22 --load5 20 --load15 0.01 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 150000  --ftpconn 300"

        job_submit="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobSubmit %s\""%(limit_values)

        job_register="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobRegister %s\""%(limit_values)

        utils.info("Set jobSubmit  = %s; and jobRegister  = %s; to glite_wms.conf at WMS"%(job_submit,job_register))

        SSH_utils.change_remote_file(utils,ssh,"/etc/glite-wms/glite_wms.conf", ['jobSubmit','jobRegister'],['*','*'],[job_submit,job_register])

        utils.info("Restart workload manager proxy glite-wms-wmproxy")

        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

        utils.set_isb_jdl(utils.get_jdl_file())

        utils.info("Submit a job , submission should be failed")

        OUTPUT=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()),1).split("\n")

        utils.info("Check failed message")

        find=0

        for line in OUTPUT:
            if line.find("System load is too high")!=-1:
                utils.info("Check OK, the detected failure reason is: 'System load is too high'")
                find=1
                break

        if find==0:
            utils.error("Faulure reason is not 'System load is too high' as expected.")
            raise GeneralError("Check faulure reason","Failure reason is not 'System load is too high' as expected")

        utils.info("Check if the detected threshold is for parameter --load15, 'Load Average(15 min)'")

        find=0

        for line in OUTPUT:
            if line.find("Threshold for Load Average(15 min):")!=-1:
                utils.info("Check OK, detected threshold is for parameter --load15 'Load Average15 min)' as expected")
                find=1
                break

        if find==0:
            utils.error("Detected threshold is not for parameter load15 ('Load Average(15 min)') as expected")
            raise GeneralError("Check the parameter of the limiter mechanism","Detected threshold is not for parameter load15 ('Load Average(15 min)') as expected ")


        for line in OUTPUT:
            if line.find("Method")!=-1:
               utils.info("Get Method: %s"%(line))
               break

        utils.info("Test OK")

        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
        return 1

    return 0


def test4(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        limit_values="--load1 22 --load5 20 --load15 18 --memusage 1 --diskusage 95 --fdnum 1000 --jdnum 150000  --ftpconn 300"

        job_submit="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobSubmit %s\""%(limit_values)

        job_register="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobRegister %s\""%(limit_values)

        utils.info("Set jobSubmit  = %s; and jobRegister  = %s; to glite_wms.conf at WMS"%(job_submit,job_register))

        SSH_utils.change_remote_file(utils,ssh,"/etc/glite-wms/glite_wms.conf", ['jobSubmit','jobRegister'],['*','*'],[job_submit,job_register])

        utils.info("Restart workload manager proxy glite-wms-wmproxy")

        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

        utils.set_isb_jdl(utils.get_jdl_file())

        utils.info("Submit a job , submission should be failed")

        OUTPUT=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()),1).split("\n")

        utils.info("Check failed message")

        find=0

        for line in OUTPUT:
            if line.find("System load is too high")!=-1:
                utils.info("Check OK, the detected failure reason is: 'System load is too high'")
                find=1
                break

        if find==0:
            utils.error("Faulure reason is not 'System load is too high' as expected.")
            raise GeneralError("Check faulure reason","Failure reason is not 'System load is too high' as expected")

        utils.info("Check if the detected threshold is for parameter --memusage, 'Memory Usage'")

        find=0

        for line in OUTPUT:
            if line.find("Threshold for Memory Usage:")!=-1:
                utils.info("Check OK, detected threshold is for parameter --memusage 'Memory Usage)' as expected")
                find=1
                break

        if find==0:
            utils.error("Detected threshold is not for parameter --memusage ('Memory Usage') as expected")
            raise GeneralError("Check the parameter of the limiter mechanism","Detected threshold is not for parameter --memusage ('Memory Usage') as expected ")


        for line in OUTPUT:
            if line.find("Method")!=-1:
               utils.info("Get Method: %s"%(line))
               break

        utils.info("Test OK")

        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
        return 1

    return 0


def test5(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        limit_values="--load1 22 --load5 20 --load15 18 --memusage 99 --diskusage 99 --swapusage 0.1 --fdnum 1000 --jdnum 150000  --ftpconn 300"

        job_submit="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobSubmit %s\""%(limit_values)

        job_register="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobRegister %s\""%(limit_values)

        utils.info("Set jobSubmit  = %s; and jobRegister  = %s; to glite_wms.conf at WMS"%(job_submit,job_register))

        SSH_utils.change_remote_file(utils,ssh,"/etc/glite-wms/glite_wms.conf", ['jobSubmit','jobRegister'],['*','*'],[job_submit,job_register])

        utils.info("Restart workload manager proxy glite-wms-wmproxy")

        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

        utils.set_isb_jdl(utils.get_jdl_file())

        utils.info("Submit a job , submission should be failed")

        OUTPUT=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()),1).split("\n")

        utils.info("Check failed message")

        find=0

        for line in OUTPUT:
            if line.find("System load is too high")!=-1:
                utils.info("Check OK, the detected failure reason is: 'System load is too high'")
                find=1
                break

        if find==0:
            utils.error("Faulure reason is not 'System load is too high' as expected.")
            raise GeneralError("Check faulure reason","Failure reason is not 'System load is too high' as expected")

        utils.info("Check if the detected threshold is for parameter --swapusage, 'Swap Usage'")

        find=0

        for line in OUTPUT:
            if line.find("Threshold for Swap Usage:")!=-1:
                utils.info("Check OK, detected threshold is for parameter --swapusage 'Swap Usage' as expected")
                find=1
                break

        if find==0:
            utils.error("Detected threshold is not for parameter --swapusage ('Swap Usage') as expected")
            raise GeneralError("Check the parameter of the limiter mechanism","Detected threshold is not for parameter --swapusage ('Swap Usage') as expected ")


        for line in OUTPUT:
            if line.find("Method")!=-1:
               utils.info("Get Method: %s"%(line))
               break

        utils.info("Test OK")

        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
        return 1

    return 0


def test6(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        limit_values="--load1 22 --load5 20 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 150000  --ftpconn 0"

        job_submit="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobSubmit %s\""%(limit_values)

        job_register="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobRegister %s\""%(limit_values)

        utils.info("Set jobSubmit  = %s; and jobRegister  = %s; to glite_wms.conf at WMS"%(job_submit,job_register))

        SSH_utils.change_remote_file(utils,ssh,"/etc/glite-wms/glite_wms.conf", ['jobSubmit','jobRegister'],['*','*'],[job_submit,job_register])

        utils.info("Restart workload manager proxy glite-wms-wmproxy")

        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

        utils.set_isb_jdl(utils.get_jdl_file())

        utils.info("Submit a job , submission should be failed")

        OUTPUT=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()),1).split("\n")

        utils.info("Check failed message")

        find=0

        for line in OUTPUT:
            if line.find("System load is too high")!=-1:
                utils.info("Check OK, the detected failure reason is: 'System load is too high'")
                find=1
                break

        if find==0:
            utils.error("Faulure reason is not 'System load is too high' as expected.")
            raise GeneralError("Check faulure reason","Failure reason is not 'System load is too high' as expected")

        utils.info("Check if the detected threshold is for parameter --ftpconn, 'FTP Connection'")

        find=0

        for line in OUTPUT:
            if line.find("Threshold for FTP Connection:")!=-1:
                utils.info("Check OK, detected threshold is for parameter --ftpconn 'FTP Connection' as expected")
                find=1
                break

        if find==0:
            utils.error("Detected threshold is not for parameter --ftpconn ('FTP Connection') as expected")
            raise GeneralError("Check the parameter of the limiter mechanism","Detected threshold is not for parameter --ftpconn ('FTP Connection') as expected ")


        for line in OUTPUT:
            if line.find("Method")!=-1:
               utils.info("Get Method: %s"%(line))
               break

        utils.info("Test OK")

        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
        return 1

    return 0

def test7(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        limit_values="--load1 22 --load5 20 --load15 18 --memusage 99 --diskusage 1 --fdnum 1000 --jdnum 150000  --ftpconn 300"

        job_submit="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobSubmit %s\""%(limit_values)

        job_register="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobRegister %s\""%(limit_values)

        utils.info("Set jobSubmit  = %s; and jobRegister  = %s; to glite_wms.conf at WMS"%(job_submit,job_register))

        SSH_utils.change_remote_file(utils,ssh,"/etc/glite-wms/glite_wms.conf", ['jobSubmit','jobRegister'],['*','*'],[job_submit,job_register])

        utils.info("Restart workload manager proxy glite-wms-wmproxy")

        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

        utils.set_isb_jdl(utils.get_jdl_file())

        utils.info("Submit a job , submission should be failed")

        OUTPUT=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()),1).split("\n")

        utils.info("Check failed message")

        find=0

        for line in OUTPUT:
            if line.find("System load is too high")!=-1:
                utils.info("Check OK, the detected failure reason is: 'System load is too high'")
                find=1
                break

        if find==0:
            utils.error("Faulure reason is not 'System load is too high' as expected.")
            raise GeneralError("Check faulure reason","Failure reason is not 'System load is too high' as expected")

        utils.info("Check if the detected threshold is for parameter --diskusage, 'Disk Usage'")

        find=0

        for line in OUTPUT:
            if line.find("Threshold for Disk Usage:")!=-1:
                utils.info("Check OK, detected threshold is for parameter --diskusage 'Disk Usage' as expected")
                find=1
                break

        if find==0:
            utils.error("Detected threshold is not for parameter --diskusage ('Disk Usage') as expected")
            raise GeneralError("Check the parameter of the limiter mechanism","Detected threshold is not for parameter --diskusage ('Disk Usage') as expected ")


        for line in OUTPUT:
            if line.find("Method")!=-1:
               utils.info("Get Method: %s"%(line))
               break

        utils.info("Test OK")

        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
        return 1

    return 0


def test8(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        limit_values="--load1 22 --load5 20 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000000 --jdnum 150000  --ftpconn 300"

        job_submit="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobSubmit %s\""%(limit_values)

        job_register="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobRegister %s\""%(limit_values)

        utils.info("Set jobSubmit  = %s; and jobRegister  = %s; to glite_wms.conf at WMS"%(job_submit,job_register))

        SSH_utils.change_remote_file(utils,ssh,"/etc/glite-wms/glite_wms.conf", ['jobSubmit','jobRegister'],['*','*'],[job_submit,job_register])

        utils.info("Restart workload manager proxy glite-wms-wmproxy")

        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

        utils.set_isb_jdl(utils.get_jdl_file())

        utils.info("Submit a job , submission should be failed")

        OUTPUT=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()),1).split("\n")

        utils.info("Check failed message")

        find=0

        for line in OUTPUT:
            if line.find("System load is too high")!=-1:
                utils.info("Check OK, the detected failure reason is: 'System load is too high'")
                find=1
                break

        if find==0:
            utils.error("Faulure reason is not 'System load is too high' as expected.")
            raise GeneralError("Check faulure reason","Failure reason is not 'System load is too high' as expected")

        utils.info("Check if the detected threshold is for parameter --fdnum, 'Threshold for used file descriptor'")

        find=0

        for line in OUTPUT:
            if line.find("Threshold for Free FD:")!=-1:
                utils.info("Check OK, detected threshold is for parameter --fdnum 'Threshold for used file descriptor' as expected")
                find=1
                break

        if find==0:
            utils.error("Detected threshold is not for parameter --fdnum ('Threshold for used file descriptor') as expected")
            raise GeneralError("Check the parameter of the limiter mechanism","Detected threshold is not for parameter --fdnum ('Threshold for used file descriptor') as expected ")


        for line in OUTPUT:
            if line.find("Method")!=-1:
               utils.info("Get Method: %s"%(line))
               break

        utils.info("Test OK")

        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
        return 1

    return 0


def test9(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        limit_values="--load1 22 --load5 20 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 0  --ftpconn 300"

        job_submit="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobSubmit %s\""%(limit_values)

        job_register="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobRegister %s\""%(limit_values)

        utils.info("Set jobSubmit  = %s; and jobRegister  = %s; to glite_wms.conf at WMS"%(job_submit,job_register))

        SSH_utils.change_remote_file(utils,ssh,"/etc/glite-wms/glite_wms.conf", ['jobSubmit','jobRegister'],['*','*'],[job_submit,job_register])

        utils.info("Restart workload manager proxy glite-wms-wmproxy")

        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

        utils.set_isb_jdl(utils.get_jdl_file())

        utils.info("Stop workload manager glite-wms-wm")

        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm stop")

        utils.info("Submit a job")

        jobid=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file())).split("\n")

        utils.info("Submit a job , submission should be failed")

        OUTPUT=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()),1).split("\n")

        utils.info("Check failed message")

        find=0

        for line in OUTPUT:
            if line.find("System load is too high")!=-1:
                utils.info("Check OK, the detected failure reason is: 'System load is too high'")
                find=1
                break

        if find==0:
            utils.error("Faulure reason is not 'System load is too high' as expected.")
            raise GeneralError("Check faulure reason","Failure reason is not 'System load is too high' as expected")

        utils.info("Check if the detected threshold is for parameter --jdnum, 'Threshold for number of unprocessed jobs (for jobdir)'")

        find=0

        for line in OUTPUT:
            if line.find("Threshold for WMS Input JobDir jobs:")!=-1:
                utils.info("Check OK, detected threshold is for parameter --jdnum 'Threshold for number of unprocessed jobs (for jobdir)' as expected")
                find=1
                break

        if find==0:
            utils.error("Detected threshold is not for parameter --jdnum ('Threshold for number of unprocessed jobs (for jobdir)') as expected")
            raise GeneralError("Check the parameter of the limiter mechanism","Detected threshold is not for parameter --jdnum ('Threshold for number of unprocessed jobs (for jobdir)') as expected ")


        for line in OUTPUT:
            if line.find("Method")!=-1:
               utils.info("Get Method: %s"%(line))
               break

        utils.info("Test OK")

        utils.info("Start workload manager glite-wms-wm")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm start")

        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        utils.info("Start workload manager glite-wms-wm")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm start")
        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
        return 1

    return 0



def test10(utils,ssh,title):

    utils.show_progress(title)
    utils.info(title)

    try:

        limit_values="--load1 22 --load5 20 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 150000  --ftpconn 300 --jdsize 0.001"

        job_submit="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobSubmit %s\""%(limit_values)

        job_register="\"${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobRegister %s\""%(limit_values)

        utils.info("Set jobSubmit  = %s; and jobRegister  = %s; to glite_wms.conf at WMS"%(job_submit,job_register))

        SSH_utils.change_remote_file(utils,ssh,"/etc/glite-wms/glite_wms.conf", ['jobSubmit','jobRegister'],['*','*'],[job_submit,job_register])

        utils.info("Restart workload manager proxy glite-wms-wmproxy")

        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

        utils.set_isb_jdl(utils.get_jdl_file())

        utils.info("Submit a job , submission should be failed")

        OUTPUT=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()),1).split("\n")

        utils.info("Check failed message")

        find=0

        for line in OUTPUT:
            if line.find("System load is too high")!=-1:
                utils.info("Check OK, the detected failure reason is: 'System load is too high'")
                find=1
                break

        if find==0:
            utils.error("Faulure reason is not 'System load is too high' as expected.")
            raise GeneralError("Check faulure reason","Failure reason is not 'System load is too high' as expected")

        utils.info("Check if the detected threshold is for parameter --jdsize, 'Threshold for input jobdir size (KB)'")

        find=0

        for line in OUTPUT:
            if line.find("Threshold for WMS Input JobDir size:")!=-1:
                utils.info("Check OK, detected threshold is for parameter --jdsize 'Threshold for input jobdir size (KB)' as expected")
                find=1
                break

        if find==0:
            utils.error("Detected threshold is not for parameter --jdsize ('Threshold for input jobdir size (KB)') as expected")
            raise GeneralError("Check the parameter of the limiter mechanism","Detected threshold is not for parameter --jdsize ('Threshold for input jobdir size (KB)') as expected ")


        for line in OUTPUT:
            if line.find("Method")!=-1:
               utils.info("Get Method: %s"%(line))
               break

        utils.info("Test OK")

        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        utils.info("Restore initial version of glite-wms.conf file")
        SSH_utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
        SSH_utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
        return 1

    return 0


    
def main():

    fails=[]

    tests=["Test 1: Test option --load1 threshold for load average (1 min)"]
    tests.append("Test 2: Test option --load5 threshold for load average (5 min)")
    tests.append("Test 3: Test option --load15 threshold for load average (15 min)")
    tests.append("Test 4: Test option --memusage threshold for memory usage (%)")
    tests.append("Test 5: Test option --swapusage threshold for swap usage (%)")
    tests.append("Test 6: Test option --ftpconn threshold for number of FTP connections")
    tests.append("Test 7: Test option --diskusage threshold for disk usage (%)")
    tests.append("Test 8: Test option --fdnum threshold for used file descriptor")
    tests.append("Test 9: Test option --jdnum threshold for number of unprocessed jobs (for jobdir)")
    tests.append("Test 10: Test option --jdsize threshold for input jobdir size (KB)")
    #tests.append("Test 11: Test option --flnum threshold for number of unprocessed jobs (for filelist)")
    #tests.append("Test 12: Test option --flsize threshold for input filelist size (KB)")
  
    utils = Test_utils.Test_utils(sys.argv[0],"WMS Limiter Mechanism")

    utils.prepare(sys.argv[1:],tests)

    signal.signal(signal.SIGINT,utils.exit_interrupt)


    if utils.WMS_USERNAME=='' or utils.WMS_PASSWORD=='':
       utils.warn("Please set the required variables WMS_USERNAME , WMS_PASSWORD in test's configuration file")
       utils.show_progress("Please set the required variables WMS_USERNAME , WMS_PASSWORD in test's configuration file")
       sys.exit(0)

    utils.info("WMS Limiter Mechanism Testing")

    all_tests=utils.is_all_enabled()

    try:

        ssh=SSH_utils.open_ssh(utils.get_WMS(),utils.WMS_USERNAME,utils.WMS_PASSWORD)

    except (GeneralError) , e:
        utils.log_error("Unable to connect to remote host: %s"%(utils.get_WMS()))
        utils.log_error(e)
        utils.exit_failure("Unable to connect to remote host: %s"%(utils.get_WMS()))


    if all_tests==1 or utils.check_test_enabled(1)==1 :
            if test1(utils,ssh,tests[0]):
                fails.append(tests[0])

    if all_tests==1 or utils.check_test_enabled(2)==1 :
            if test2(utils,ssh,tests[1]):
                fails.append(tests[1])

    if all_tests==1 or utils.check_test_enabled(3)==1 :
            if test3(utils,ssh,tests[2]):
                fails.append(tests[2])

    if all_tests==1 or utils.check_test_enabled(4)==1 :
            if test4(utils,ssh,tests[3]):
                fails.append(tests[3])
    
    if all_tests==1 or utils.check_test_enabled(5)==1 :
            if test5(utils,ssh,tests[4]):
                fails.append(tests[4])

    if all_tests==1 or utils.check_test_enabled(6)==1 :
            if test6(utils,ssh,tests[5]):
                fails.append(tests[5])

    if all_tests==1 or utils.check_test_enabled(7)==1 :
            if test7(utils,ssh,tests[6]):
                fails.append(tests[6])

    if all_tests==1 or utils.check_test_enabled(8)==1 :
            if test8(utils,ssh,tests[7]):
                fails.append(tests[7])

    if all_tests==1 or utils.check_test_enabled(9)==1 :
            if test9(utils,ssh,tests[8]):
                fails.append(tests[8])

    if all_tests==1 or utils.check_test_enabled(10)==1 :
            if test10(utils,ssh,tests[9]):
                fails.append(tests[9])


    SSH_utils.close_ssh(ssh)

    if len(fails) > 0 :
      utils.exit_failure("%s test(s) fail(s): %s"%(len(fails), fails))
    else:
      utils.exit_success()
    
    
  
if __name__ == "__main__":
    main()
