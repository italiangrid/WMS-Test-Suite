import time
#
# Bug: 86490
# Title: EMI WMS stops accepting jobs after 31999th submission for the same DN (on ext3)
# Link: https://savannah.cern.ch/bugs/?86490
#
#

import logging
import time
import datetime

from libutils.Exceptions import *


def run(utils):

    bug='86490'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    wms_location_var=utils.execute_remote_cmd(ssh,"echo $WMS_LOCATION_VAR")[:-1]

    logging.info("Check inside $WMS_LOCATION_VAR/proxycache for expired proxies for more than 6 hours")

    proxies=utils.execute_remote_cmd(ssh,"find %s/proxycache/ -name userproxy.pem"%(wms_location_var)).split("\n")

    for proxy in proxies:

       if proxy.strip()!='':

             expiry_date=utils.execute_remote_cmd(ssh,"openssl x509 -in %s -noout -enddate"%(proxy.strip())).split("=")[1].strip("\n")

             ddate_str=time.strptime(expiry_date,"%b %d %H:%M:%S %Y %Z")[0:8]

             dt = datetime.datetime(ddate_str[0],ddate_str[1],ddate_str[2],ddate_str[3],ddate_str[4],ddate_str[5],ddate_str[6])

             now_dt = datetime.datetime.now()

             diff=now_dt-dt

             minutes, seconds = divmod(diff.seconds, 60)
             hours, minutes = divmod(minutes, 60)

             if diff.days>=0:

                #Maybe it is necessary to check and minutes
                if hours>=6:
                   logging.error("Find expired proxy for more than 6 hours. Proxy is %s"%(proxy))
                   raise GeneralError("Check for expired proxies for more than 6 hours","Find expired proxy for more than 6 hours. Proxy is %s"%(proxy))

    logging.info("Check if there are empty directories")

    dirs = utils.execute_remote_cmd(ssh,"ls /%s/proxycache"%(wms_location_var)).split(" ")

    for dir in dirs:

       dir=dir.strip(" \n\t")

       if dir.find("cache")==-1:

          logging.info("Check directory: %s"%(dir))
          subdirs=utils.execute_remote_cmd(ssh,"find /var/proxycache/%s -name userproxy.pem | wc -l"%(dir))
          total_subdirs=utils.execute_remote_cmd(ssh,"ls -l /var/proxycache/%s | grep glite | wc -l"%(dir))

          if total_subdirs == subdirs :
               logging.info("Check OK, there are no empty directories in %s"%(dir))
          else:
               logging.error("Test Failed. There are empty directories in %s"%(dir))
               raise GeneralError("Check for emptry directories","Test Failed. There are empty directories in %s"%(dir))

    
    logging.info("Test OK")

    ssh.close()

    logging.info("End of regression test for bug %s"%(bug))
