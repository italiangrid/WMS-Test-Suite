#
# Bug:52617
# Title: [ yaim-wms ] host{cert,key}.pem in /home/glite
# Link: https://savannah.cern.ch/bugs/?52617
#
#


import logging

from libutils.Exceptions import *

def run(utils):

    bug='52617'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Check for hostcert.pem at /etc/grid-security")

    result=utils.execute_remote_cmd(ssh,"ls -l /etc/grid-security/hostcert.pem")

    res=result.split(" ")
    
    if res[0].find("-rw-r--r--")==-1:
      logging.error("Wrong file access permissions  for /etc/grid-security/hostcert.pem")
      raise GeneralError("","Error !!! Wrong file access permissions  for /etc/grid-security/hostcert.pem")

    logging.info("Check for hostkey.pem at /etc/grid-security")

    result=utils.execute_remote_cmd(ssh,"ls -l /etc/grid-security/hostkey.pem")

    res=result.split(" ")

    if res[0].find("-r--------")==-1:
      logging.error("Wrong file access permissions  for /etc/grid-security/hostkey.pem")
      raise GeneralError("","Error !!! Wrong file access permissions  for /etc/grid-security/hostkey.pem")


    logging.info("Check if directory /home/glite is empty")

    res=utils.execute_remote_cmd(ssh,"ls -l /home/glite")

    if res.find("total 0")==-1:
      logging.error("Directory /home/glite is not empty")
      raise GeneralError("","Error !!! Directory /home/glite is not empty")

    ssh.close()

    logging.info("End of regression test for bug %s",bug)
