#
# Bug: 91563
# Title: yaim-wms: set ldap query filter expression for GLUE2 in WMS configuration
# Link: https://savannah.cern.ch/bugs/?91563
#
#

from lib.Exceptions import *

def run(utils):

    bug='91563'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Get glite_wms.conf file from WMS")

    utils.ssh_get_file(ssh,"/etc/glite-wms/glite_wms.conf","%s/glite_wms.conf"%(utils.get_tmp_dir()))

    ssh.close()

    FILE=open("%s/glite_wms.conf"%(utils.get_tmp_dir()))
    lines=FILE.readlines()
    FILE.close()

    utils.log_info("Gheck for IsmIiG2LDAPCEFilterExt and IsmIiG2LDAPSEFilterExt attributes in the glite_wms.conf file")

    ce_expr=''
    se_expr=''

    for line in lines:
        if line.lstrip().find("IsmIiG2LDAPCEFilterExt")!=-1:
            ce_expr=line.split(" = ")[1]
        if line.lstrip().find("IsmIiG2LDAPSEFilterExt")!=-1:
            se_expr=line.split(" = ")[1]

    if len(ce_expr)==0:
        utils.log_info("ERROR: Unable to find the expected IsmIiG2LDAPCEFilterExt attribute in the glite_wms.conf file")
        raise GeneralError("Check IsmIiG2LDAPCEFilterExt","Unable to find the expected IsmIiG2LDAPCEFilterExt attribute in the glite_wms.conf file")
    else:
        utils.log_info("Find the expected IsmIiG2LDAPCEFilterExt attribute in the glite_wms.conf file")
        utils.log_info("IsmIiG2LDAPCEFilterExt contents: %s"%ce_expr)

    if len(se_expr)==0:
        utils.log_info("ERROR: Unable to find the expected IsmIiG2LDAPSEFilterExt attribute in the glite_wms.conf file")
        raise GeneralError("Check for IsmIiG2LDAPSEFilterExt","Unable to find the expected IsmIiG2LDAPSEFilterExt attribute in the glite_wms.conf file")
    else:
        utils.log_info("Find the expected IsmIiG2LDAPSEFilterExt attribute in the glite_wms.conf file")
        utils.log_info("IsmIiG2LDAPSEFilterExt contents: %s"%se_expr)

    utils.log_info("Test OK")

    utils.log_info("End of regression test for bug %s"%(bug))
