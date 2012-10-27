#
# Bug:91488
# Title: remove several dismissed parameters from the WMS configuration
# Link: https://savannah.cern.ch/bugs/?91488
#
#

import logging

from libutils.Exceptions import *


def run(utils):

    bug='91488'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.ssh_get_file(ssh,"/etc/glite-wms/glite_wms.conf", "%s/local_copy"%(utils.get_tmp_dir()))

    utils.close_ssh(ssh)

    dismissed_params=[
        'log_file_max_size',
        'log_rotation_base_file',
        'log_rotation_max_file_number',
        'ice.input_type',
        'wmp.input_type',
        'wmp.locallogger',
        'wm.dispatcher_type',
        'wm.enable_bulk_mm',
        'wm.ism_ii_ldapsearch_async'
    ]

    logging.info("Check that dismissed parameters have been removed from the glite_wms.conf file")

    FILE=open("%s/local_copy"%(utils.get_tmp_dir()))
    conf_file=' '.join(FILE.readlines())
    FILE.close()

    params=[]

    for value in dismissed_params:
        logging.info("Check for dismissed parameter: %s"%(value))
        if conf_file.find(value)!=-1:
             params.append(value)
             logging.error("glite_wms.conf contains dismissed parameter:%s"%(value))

    if len(params)==0:
        logging.info("All dismissed parameters have been removed from the glite_wms.conf")
    else:
        logging.error("Test failed, there are some dismissed parameters in glite_wms.conf : ( %s )"%(' , '.join(params)))
        raise GeneralError("Check logfile name","Test failed, there are some dismissed parameters in glite_wms.conf : ( %s )"%(' , '.join(params)))
    
    
    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
