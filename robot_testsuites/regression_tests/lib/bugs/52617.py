#
# Bug:52617
# Title: [ yaim-wms ] host{cert,key}.pem in /home/glite
# Link: https://savannah.cern.ch/bugs/?52617
#
#

from lib.Exceptions import *

def run(utils):

    bug='52617'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Check for hostcert.pem at /etc/grid-security")

    result=utils.execute_remote_cmd(ssh,"ls -l /etc/grid-security/hostcert.pem")

    res=result.split(" ")
    
    if res[0].find("-rw-r--r--")==-1:
      utils.log_info("ERROR: Wrong file access permissions  for /etc/grid-security/hostcert.pem")
      raise GeneralError("","Error !!! Wrong file access permissions  for /etc/grid-security/hostcert.pem")

    utils.log_info("Check for hostkey.pem at /etc/grid-security")

    result=utils.execute_remote_cmd(ssh,"ls -l /etc/grid-security/hostkey.pem")

    res=result.split(" ")

    if res[0].find("-r--------")==-1:
      utils.log_info("ERROR: Wrong file access permissions  for /etc/grid-security/hostkey.pem")
      raise GeneralError("","Error !!! Wrong file access permissions  for /etc/grid-security/hostkey.pem")

    utils.log_info("Check if directory /home/glite is empty")

    res=utils.execute_remote_cmd(ssh,"ls -l /home/glite")

    if res.find("total 0")==-1:
      utils.log_info("ERROR: Directory /home/glite is not empty")
      raise GeneralError("","Error !!! Directory /home/glite is not empty")

    ssh.close()

    utils.log_info("End of regression test for bug %s"%bug)
