#
# Bug: 90760
# Title: yaim-wms changes for Argus based authZ
# Link: https://savannah.cern.ch/bugs/?90760
#
#

import logging

from libutils.Exceptions import *

def run(utils):

    bug='90760'

    find_use_argus=0
    find_argus_pepd=0
    errors=[]

    if utils.YAIM_FILE=='':
        raise GeneralError("Missing required variable (YAIM_FILE)","To verify this bug it is necessary to set the YAIM_FILE in the configuration file")
    
    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.ssh_get_file(ssh, "%s"%(utils.YAIM_FILE), "%s/yaim_local_copy"%(utils.get_tmp_dir()))

    logging.info("Change yaim file")

    logging.info("Set USE_ARGUS=yes and ARGUS_PEPD_ENDPOINTS=\"https://argus01.lcg.cscs.ch:8154/authz https://argus02.lcg.cscs.ch:8154/authz https://argus03.lcg.cscs.ch:8154/authz\"")

    FILE=open("%s/yaim_local_copy"%(utils.get_tmp_dir()),"r")
    yaim=FILE.readlines()
    FILE.close()

    for line in yaim:

        if line.find("USE_ARGUS")!=-1:
             find_use_argus=1
             yaim[yaim.index(line)]="USE_ARGUS=true\n"
             
        if line.find("ARGUS_PEPD_ENDPOINTS")!=-1:
             find_argus_pepd=1
             yaim[yaim.index(line)]="ARGUS_PEPD_ENDPOINTS=\"https://argus01.lcg.cscs.ch:8154/authz https://argus02.lcg.cscs.ch:8154/authz https://argus03.lcg.cscs.ch:8154/authz\"\n"


    if find_use_argus==0:
        yaim.append("USE_ARGUS=true\n")

    if find_argus_pepd==0:
        yaim.append("ARGUS_PEPD_ENDPOINTS=\"https://argus01.lcg.cscs.ch:8154/authz https://argus02.lcg.cscs.ch:8154/authz https://argus03.lcg.cscs.ch:8154/authz\"\n")

    FILE=open("%s/new_yaim"%(utils.get_tmp_dir()),"w")
    FILE.writelines(yaim)
    FILE.close()

    logging.info("Backup initial yaim configuration file")

    utils.execute_remote_cmd(ssh,"cp -f %s %s_90760_bak"%(utils.YAIM_FILE,utils.YAIM_FILE))

    logging.info("Transfer new yaim configuration file")

    utils.ssh_put_file(ssh, "%s/new_yaim"%(utils.get_tmp_dir()), utils.YAIM_FILE)

    logging.info("Execute yaim configuration")

    utils.execute_remote_cmd(ssh,"/opt/glite/yaim/bin/yaim -c -s %s -n WMS"%(utils.YAIM_FILE))

    logging.info("Get glite-wms.conf file")

    utils.ssh_get_file(ssh, "/etc/glite-wms/glite_wms.conf", "%s/local_copy"%(utils.get_tmp_dir()))

    FILE=open("%s/local_copy"%(utils.get_tmp_dir()),"r")
    lines=FILE.readlines()
    FILE.close()

    logging.info("Check glite_wms.conf for ARGUS related parameters")

    logging.info("Check configuration parameter ArgusAuthz")

    if " ".join(lines).find("ArgusAuthz")==-1:
         errors.append("Unable to find ArgusAuthz parameter")
    else:
        for line in lines:
            if line.find("ArgusAuthz")!=-1:
                 if line.find("true")==-1:
                     errors.append("Configuration parameter ArgusAuthz is not 'true'")
                     break
                     
    logging.info("Check configuration parameter ArgusPepdEndpoints")

    target='{"https://argus01.lcg.cscs.ch:8154/authz", "https://argus02.lcg.cscs.ch:8154/authz", "https://argus03.lcg.cscs.ch:8154/authz"};'

    if " ".join(lines).find("ArgusPepdEndpoints")==-1:
         errors.append("Unable to find ArgusPepdEndpoints parameter")
    else:
        for line in lines:
            if line.find("ArgusPepdEndpoints")!=-1:
                 if line.find(target)==-1:
                     errors.append("Configuration parameter ArgusPepdEndpoints is not '%s'"%(target))
                     break

    logging.info("Restore initial yaim configuration file")

    utils.execute_remote_cmd(ssh,"cp -f %s_90760_bak %s"%(utils.YAIM_FILE,utils.YAIM_FILE))

    logging.info("Execute yaim configuration")

    utils.execute_remote_cmd(ssh,"/opt/glite/yaim/bin/yaim -c -s %s -n WMS"%(utils.YAIM_FILE))

    ssh.close()

    if len(errors)>0:
        logging.error("Unable to find all the ARGUS related attributes in glite_wms.conf")
        logging.error("ERRORS:\n %s"%("\n ".join(errors)))
        raise GeneralError("Check glite_wms.conf for ARGUS related attributes","Unable to find all the ARGUS related attribures in glite_wms.conf")
    else:
        logging.info("Check OK")
        
    
    logging.info("End of regression test for bug %s",bug)
