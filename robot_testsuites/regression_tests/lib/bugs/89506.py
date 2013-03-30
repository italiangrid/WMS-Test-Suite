#
# Bug:89506
# Title: EMI WMS wmproxy rpm doesn't set execution permissions as it used to do in gLite
# Link: https://savannah.cern.ch/bugs/?89506
#
#


from lib.Exceptions import *


def run(utils):

    bug='89506'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

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

    utils.log_info("Check the execution permissions")

    errors=[]

    for executable in executables:

        output=utils.execute_remote_cmd(ssh,"ls -l %s"%(executable))

        utils.log_info("Check owner and group for %s"%(executable))

        if output.find("root root")!=-1:
            utils.log_info("Check ok , find root root")
        else:
            utils.log_info("ERROR: Wrong owner,group. Details: %s"%(output))
            errors.append(output)

        utils.log_info("Check the execution permission for: %s"%(executable))

        permission=permissions[executables.index(executable)]

        if output.find(permission)!=-1:
            utils.log_info("Check ok , find %s as expected"%(permission))
        else:
            utils.log_info("ERROR: Wrong permission. Details: %s"%(output))
            errors.append(output)

    utils.close_ssh(ssh)

    #remove possible duplicate entries
    errors=set(errors)

    if len(errors)>0:
        utils.log_info("ERROR: Test failed, execution permissions haven't been set correctly")
        utils.log_info("ERROR - Details: %s "%(' '.join(errors)))
        raise GeneralError("Check execution permissions","Test failed, execution permissions haven't been set correctly.")
    
    
    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))
