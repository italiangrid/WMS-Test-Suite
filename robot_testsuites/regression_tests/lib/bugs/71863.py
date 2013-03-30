#
# Bug: 71863
# Title: JobWrapper tries to use "test -eq" for string comparison
# Link: https://savannah.cern.ch/bugs/?71863
#
#

from lib.Exceptions import *

def run(utils):

    bug='71863'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Get JobWrapper template from WMS")

    utils.ssh_get_file(ssh,"/usr/share/glite-wms/jobwrapper.template.sh","%s/jobwrapper.template.sh"%(utils.get_tmp_dir()))

    ssh.close()
    
    utils.log_info("Look for expression 'if [ \"x$2\" == \"xOSB\" ]; then' at fatal_error() method")

    FILE=open("%s/jobwrapper.template.sh"%(utils.get_tmp_dir()))
    lines=FILE.readlines()
    FILE.close()
    
    found=0
    
    for line in lines:
       if line.find("if [ \"x$2\" == \"xOSB\" ]; then") != -1 :
          found=1
          break

    if found == 1:
        utils.log_info("Check OK")
    else:
        utils.log_info("ERROR: Unable to find expression 'if [ \"x$2\" == \"xOSB\" ]; then)' at fatal_error() method")
        raise GeneralError("Check jobwrapper file","Unable to find expression 'if [ \"x$2\" == \"xOSB\" ]; then)' at fatal_error() method")

    utils.log_info("Verify that expression \"test -eq\" is not present")

    found=0

    for line in lines:
       if line.find("test -eq") != -1 :
        found=1
        break

    if found == 0:
        utils.log_info("Check OK, expression \"test -eq\" is not present")
    else:
        utils.log_info("Find \"test -eq\" expression at fatal_error() method")
        raise GeneralError("Check jobwrapper file","Find \"test -eq\" expression at fatal_error() method")


    utils.log_info("Test OK")

    utils.log_info("End of regression test for bug %s"%(bug))
