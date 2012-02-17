#
# Bug: 87994
# Title: yaim-wms doesn't fill the attributes get_acbr and get_owner in the conf file for Glue2
# Link: https://savannah.cern.ch/bugs/?87994
#
#

import logging

from libutils.Exceptions import *

def run(utils):

    bug='87994'


    if utils.YAIM_FILE=='':
        logging.error("To verify this bug it is necessary to set the YAIM_FILE in the configuration file")
        raise GeneralError("Missing required variable (YAIM_FILE)","To verify this bug it is necessary to set the YAIM_FILE in the configuration file")
    
    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    target="/etc/glite/info/service/glite-info-glue2-wmproxy.conf"

    utils.ssh_get_file(ssh, "%s"%(target), "%s/local_copy"%(utils.get_tmp_dir()))

    ssh.close()
    
    logging.info("Parse yaim file to find all the supported VOs")

    FILE=open(utils.YAIM_FILE,"r")
    yaim=FILE.readlines()
    FILE.close()

    for line in yaim:
        if line.find("VOS")!=-1:
            vos=line.split("=")[1].strip(" \"\n").split(" ")
            logging.info("Find the following VOs: %s"%(vos))
            break

    VOS=[]

    for vo in vos:
       VOS.append("VO:%s"%(vo))

    logging.info("Parse file /etc/glite/info/service/glite-info-glue2-wmproxy.conf  to find attributes get_acbr and get_owner")
    
    FILE=open("%s/local_copy"%(utils.get_tmp_dir()),"r")
    lines=FILE.readlines()
    FILE.close()

    get_acbr=''
    get_owner=''

    for line in lines:
        if line.find("get_acbr")!=-1:
             get_acbr=line
             logging.info("Attribute get_acbr: %s"%(get_acbr))
             
        if line.find("get_owner")!=-1:
             get_owner=line
             logging.info("Attribute get_owner: %s"%(get_owner))


    logging.info("Check attribute get_acbr")

    if get_owner.find("\\n".join(vos))==-1:
        logging.error("Unable to find all supported VOs in attribute get_acbr.")
        raise GeneralError("Check attribute get_acbr","Unable to find all the supported VOs in attribute get_acbr.")
    else:
        logging.info("Find all supported VOs in attribute get_acbr")

    logging.info("Check attribute get_owner")
    
    if get_acbr.find("\\n".join(VOS))==-1:
        logging.error("Unable to find all the supported VOs in attribute get_owner.")
        raise GeneralError("Check attribute get_owner","Unable to find all the supported VOs in attribute get_owner.")
    else:
        logging.info("Find all supported VOs in attribute get_owner")
        
    logging.info("Test OK")
  
    logging.info("End of regression test for bug %s",bug)
