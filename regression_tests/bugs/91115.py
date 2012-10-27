#
# Bug: 91115
# Title: Make some WMS init scripts System V compatible
# Link: https://savannah.cern.ch/bugs/?91115
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='91115'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    scripts=[
        '/etc/init.d/glite-wms-ice',
        '/etc/init.d/glite-wms-wmproxy'
    ]
    
    logging.info("Check if WMS init scripts are System V compatible")

    errors=[]

    for script in scripts:

        index=scripts.index(script)

        utils.ssh_get_file(ssh,script,"%s/local_%s"%(utils.get_tmp_dir(),index))

        FILE=open("%s/local_%s"%(utils.get_tmp_dir(),index))
        init_script=' '.join(FILE.readlines())
        FILE.close()

        logging.info("Check script %s for chkconfig and description"%(script))

        if init_script.find("# chkconfig:")!=-1 and init_script.find("# description:")!=-1:
            logging.info("Check OK")
        else:
            logging.error("Unable to find both chkconfig and description at script %s"%(script))
            errors.append(script)


    utils.close_ssh(ssh)

    if len(errors)>0:
        logging.error("Test failed, not all scripts are System V compatible")
        logging.error("Not compatible scripts: %s "%(' , '.join(errors)))
        raise GeneralError("Check if script are System V compatible","Test failed, not all scripts are System V compatible")
    
    
    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))

