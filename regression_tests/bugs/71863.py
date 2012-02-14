#
# Bug: 71863
# Title: JobWrapper tries to use "test -eq" for string comparison
# Link: https://savannah.cern.ch/bugs/?71863
#
#

import logging

from libutils.Exceptions import *

def run(utils):

    bug='71863'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Get JobWrapper template from WMS")

    utils.ssh_get_file(ssh,"/usr/share/glite-wms/jobwrapper.template.sh","%s/jobwrapper.template.sh"%(utils.get_tmp_dir()))

    ssh.close()
    
    logging.info("Look for expression 'if [ \"x$2\" == \"xOSB\" ]; then' at fatal_error() method")

    FILE=open("%s/jobwrapper.template.sh"%(utils.get_tmp_dir()))
    lines=FILE.readlines()
    FILE.close()
    
    found=0
    
    for line in lines:
       if line.find("if [ \"x$2\" == \"xOSB\" ]; then") != -1 :
          found=1
          break

    if found == 1:
        logging.info("Check OK")
    else:
        logging.error("Unable to find expression 'if [ \"x$2\" == \"xOSB\" ]; then)' at fatal_error() method")
        raise GeneralError("Check jobwrapper file","Unable to find expression 'if [ \"x$2\" == \"xOSB\" ]; then)' at fatal_error() method")


    logging.info("Check if \"test -eq\" expression is present")

    found=0

    for line in lines:
       if line.find("test -eq") != -1 :
        found=1
        break

    if found == 0:
        logging.info("Check OK")
    else:
        logging.error("Find \"test -eq\" expression at fatal_error() method")
        raise GeneralError("Check jobwrapper file","Find \"test -eq\" expression at fatal_error() method")


    logging.info("Test OK")

    logging.info("End of regression test for bug %s"%(bug))
