#
# Bug:89506
# Title: EMI WMS wmproxy rpm doesn't set execution permissions as it used to do in gLite
# Link: https://savannah.cern.ch/bugs/?89506
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='89506'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    executables=[
        '/usr/bin/glite-wms-wmproxy-purge-proxycache',
        '/usr/bin/glite_wms_wmproxy_server',
        '/usr/sbin/glite_wms_wmproxy_load_monitor',
        '/usr/libexec/glite_wms_wmproxy_dirmanager'
    ]

    permissions=[
        '-rwxr-xr-x',
        '-rwxr-xr-x',
        '-rwsr-xr-x',
        '-rwsr-xr-x'
    ]

    logging.info("Check the execution permissions")

    errors=[]

    for executable in executables:

        output=utils.execute_remote_cmd(ssh,"ls -l %s"%(executable))

        logging.info("Check owner and group for %s"%(executable))

        if output.find("root root")!=-1:
            logging.info("Check ok , find root root")
        else:
            logging.error("Wrong owner,group. Details: %s"%(output))
            errors.append(output)

        logging.info("Check the execution permission for: %s"%(executable))

        permission=permissions[executables.index(executable)]

        if output.find(permission)!=-1:
            logging.info("Check ok , find %s as expected"%(permission))
        else:
            logging.error("Wrong permission. Details: %s"%(output))
            errors.append(output)

    utils.close_ssh(ssh)

    #remove possible duplicate entries
    errors=set(errors)

    if len(errors)>0:
        logging.error("Test failed, execution permissions haven't been set correctly")
        logging.error("Details: %s "%(' '.join(errors)))
        raise GeneralError("Check execution permissions","Test failed, execution permissions haven't been set correctly.")
    
    
    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
