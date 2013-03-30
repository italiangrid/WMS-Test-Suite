#
# Bug: 91115
# Title: Make some WMS init scripts System V compatible
# Link: https://savannah.cern.ch/bugs/?91115
#
#

from lib.Exceptions import *


def run(utils):

    bug='91115'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    scripts=[
        '/etc/init.d/glite-wms-ice',
        '/etc/init.d/glite-wms-wmproxy'
    ]
    
    utils.log_info("Check if WMS init scripts are System V compatible")

    errors=[]

    for script in scripts:

        index=scripts.index(script)

        utils.ssh_get_file(ssh,script,"%s/local_%s"%(utils.get_tmp_dir(),index))

        FILE=open("%s/local_%s"%(utils.get_tmp_dir(),index))
        init_script=' '.join(FILE.readlines())
        FILE.close()

        utils.log_info("Check script %s for chkconfig and description"%(script))

        if init_script.find("# chkconfig:")!=-1 and init_script.find("# description:")!=-1:
            utils.log_info("Check OK")
        else:
            utils.log_info("ERROR: Unable to find both chkconfig and description at script %s"%(script))
            errors.append(script)


    utils.close_ssh(ssh)

    if len(errors)>0:
        utils.log_info("ERROR: Test failed, not all scripts are System V compatible")
        utils.log_info("ERRPR: Not compatible scripts: %s "%(' , '.join(errors)))
        raise GeneralError("Check if script are System V compatible","Test failed, not all scripts are System V compatible")
    
    
    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))

