#
# Bug:70331
# Title: glite-wms-create-proxy "ambiguous redirect"
# Link: https://savannah.cern.ch/bugs/?70331
#
#

import time

from lib.Exceptions import *

def run(utils):

    bug='70331'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Test script glite-wms-create-proxy.sh")

    chan=ssh.invoke_shell()

    cmd="/usr/sbin/glite-wms-create-proxy.sh /var/wms.proxy /var/log/wms/create_proxy.log"

    chan.send("su - glite \n")

    tCheck=0

    while not chan.recv_ready():
        time.sleep(1)
        tCheck+=1
        if tCheck >= 6:
            utils.log_info("ERROR: Time out while waiting response from remote host %s"%(utils.get_WMS()))
            raise TimeOutError("","Time out while waiting response from remote host %s"%(utils.get_WMS()))

    chan.recv(1024)

    chan.send(cmd +"\n")

    tCheck=0

    while not chan.recv_ready():
        time.sleep(1)
        tCheck+=1
        if tCheck >= 6:
            utils.log_info("ERROR: Time out while waiting response from remote host %s"%(utils.get_WMS()))
            raise TimeOutError("","Time out while waiting response from remote host %s"%(utils.get_WMS()))
    
    output = chan.recv(1024).split("\n")

    if len(output)==2:
        utils.log_info("Check OK. Command: %s , executed with no error messages"%(cmd))
    else:

        if len(output)==3:
            ssh.close()
            utils.log_info("ERROR: Command %s returns the following error message:\n%s\n"%(cmd,output[1]))
            raise GeneralError("","Command %s returns the following error message:\n%s\n"%(cmd,output[1]))
        else:
            ssh.close()
            utils.log_info("ERROR: General error. Output from remote host %s"%(''.join(output)))
            raise GeneralError("","General error. Output from remote host %s"%(''.join(output)))

    ssh.close()

    utils.log_info("Test OK")

    utils.log_info("End of regression test for bug %s"%(bug))
