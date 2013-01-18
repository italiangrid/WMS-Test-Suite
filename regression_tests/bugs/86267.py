#
# Bug: 86267
# Title: queryDb has 2 bugs handling user options (see ggus ticket for more info)
# Link: https://savannah.cern.ch/bugs/?86267
#
#

import logging

from libutils.Exceptions import *

def run(utils):

    bug='86267'

    status_counter={
                'REGISTERED':0,
                'PENDING':0,
                'IDLE':0,
                'RUNNING':0,
                'REALLY-RUNNING':0,
                'CANCELLED':0,
                'HELD':0,
                'ABORTED':0,
                'DONE-OK':0,
                'DONE-FAILED':0,
                'UNKNOWN':0,
                'PURGED':0
             }

    status=[
                "REGISTERED",
                "PENDING",
                "IDLE",
                "RUNNING",
                "REALLY-RUNNING",
                "CANCELLED",
                "HELD",
                "ABORTED",
                "DONE-OK",
                "DONE-FAILED",
                "UNKNOWN",
                "PURGED"
            ]

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Try option -v without any other options")

    output=utils.execute_remote_cmd_fail(ssh,"/usr/bin/queryDb --conf glite_wms.conf -v")

    logging.info("Check command's message")

    if output.find("Options --verbose|-v requires at least one of the options --userdn,--creamjobid,--gridjobid,--userproxy,--cream-url,--myproxy-url,--status,--lease-id,--delegation-id,--worker-node,--jdl,--modified-jdl,--sequence-code")==-1:
        ssh.close()
        logging.error("Command's output is not the expected")
        raise GeneralError("Check command's message","Command's output is not the expected")

    logging.info("Get all info")

    output=utils.execute_remote_cmd(ssh,"/usr/bin/queryDb --conf glite_wms.conf -vS")

    total=output.count("[")
    
    for line in output.split("\n"):
        for sta in status:
            if line.find(sta)!=-1:
                 status_counter[sta]=status_counter[sta]+1

    logging.info("Total Jobs:%s",total)
    logging.info("Details:\n%s",status_counter)

    query1_count=status_counter['IDLE']+status_counter['UNKNOWN']
    query2_count=status_counter['REALLY-RUNNING']
    query3_count=status_counter['RUNNING']
    
    logging.info("Query for job with status IDLE or UNKNOWN")

    result=utils.execute_remote_cmd(ssh,"/usr/bin/queryDb --conf glite_wms.conf -vS -s IDLE,UNKNOWN")

    if result.count("[")!=query1_count:
         ssh.close()
         logging.error("Wrong number of jobs with status IDLE or UNKNOWN. Find %s while expecting %s"%(result.count("["),query1_count))
         raise GeneralError("Check job's count","Wrong number of jobs with status IDLE or UNKNOWN. Find %s while expecting %s"%(result.count("["),query1_count))
    else:
         logging.info("Get %s jobs as expected"%(query1_count))

    logging.info("Query for job with status REALLY-RUNNING")

    result=utils.execute_remote_cmd(ssh,"/usr/bin/queryDb --conf glite_wms.conf -vS -s REALLY-RUNNING")

    if result.count("[")!=query2_count:
         ssh.close()
         logging.error("Wrong number of jobs with status REALLY-RUNNING. Find %s while expecting %s"%(result.count("["),query2_count))
         raise GeneralError("Check job's count","Wrong number of jobs with status REALLY-RUNNING. Find %s while expecting %s"%(result.count("["),query2_count))
    else:
         logging.info("Get %s jobs as expected"%(query2_count))


    logging.info("Query for job with status RUNNING")

    result=utils.execute_remote_cmd(ssh,"/usr/bin/queryDb --conf glite_wms.conf -vS -s RUNNING")

    if result.count("[")!=query3_count:
         ssh.close()
         logging.error("Wrong number of jobs with status RUNNING. Find %s while expecting %s"%(result.count("["),query3_count))
         raise GeneralError("Check job's count","Wrong number of jobs with status RUNNING. Find %s while expecting %s"%(result.count("["),query3_count))
    else:
         logging.info("Get %s jobs as expected"%(query3_count))


    ssh.close()
  
    logging.info("End of regression test for bug %s",bug)

