#
# Bug: 78406
# Title: [ yaim-wms ] yaim should set IsmIiLDAPCEFilterExt according to the supported VO(s)
# Link: https://savannah.cern.ch/bugs/?78406
#
#

import logging

from libutils.Exceptions import *

def run(utils):

    bug='78406'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Get glite_wms.conf file from WMS")

    utils.ssh_get_file(ssh,"/etc/glite-wms/glite_wms.conf","%s/glite_wms.conf"%(utils.get_tmp_dir()))

    logging.info("Get the list of the supported VOs")

    result=utils.execute_remote_cmd(ssh,"cd /etc/grid-security/vomsdir && ls -d */")

    result=result.split("\n")

    vos=[]

    for vo in result:
        if vo!='':
           vos.append(vo[:-1].lstrip())

    ssh.close()

    logging.info("Get the IsmIiLDAPCEFilterExt attribute from glite_wms.conf")

    FILE=open("%s/glite_wms.conf"%(utils.get_tmp_dir()))
    lines=FILE.readlines()
    FILE.close()

    attribute=''

    for line in lines:
        if line.lstrip().find("IsmIiLDAPCEFilterExt")!=-1:
           attribute=line.lstrip().split("IsmIiLDAPCEFilterExt  =  ")[1][:-1]

    for vo in vos:
        logging.info("Check IsmIiLDAPCEFilterExt expression for VO %s"%(vo))
        if attribute.find("GlueCEAccessControlBaseRule=VO:%s"%(vo))==-1 or attribute.find("GlueCEAccessControlBaseRule=VOMS:/%s/"%(vo))==-1 :
           logging.error("Unable to find the expected expression at IsmIiLDAPCEFilterExt for VO: %s"%(vo))
           raise GeneralError("Check IsmIiLDAPCEFilterExt","Unable to find the expected expression at IsmIiLDAPCEFilterExt for VO: %s"%(vo))

    logging.info("Test OK")

    logging.info("End of regression test for bug %s"%(bug))
