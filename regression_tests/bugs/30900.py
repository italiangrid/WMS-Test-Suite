#
# Bug: 30900
# Title: MinPerusalTimeInterval default is too low
# Link: https://savannah.cern.ch/bugs/?30900
#
#

import logging


from libutils.Exceptions import *


def run(utils):

    bug='30900'

    logging.info("Start regression test for bug %s"%(bug))
    
    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Check default value of MinPerusalTimeInterval at glite_wms.conf")

    utils.ssh_get_file(ssh, "/etc/glite-wms/glite_wms.conf","%s/local_glite_wms.conf"%(utils.get_tmp_dir()))

    FILE=open("%s/local_glite_wms.conf"%(utils.get_tmp_dir()))
    lines=FILE.readlines()
    FILE.close()

    MinPerusal=''

    for line in lines:
        if line.find("MinPerusalTimeInterval")!=-1:
            MinPerusal=line.split("=")[1][:-2].strip()

    if int(MinPerusal)!=1000 :
         logging.error("Default value of MinPerusalTimeInterval is not 1000")
         raise GeneralError("Check MinPerusalTimeInterval","Default value of MinPerusalTimeInterval is not 1000, we get '%s'"%(int(MinPerusal)))

   
    logging.info("Add new attribute MaxPerusalFiles to glite_wms.conf at WMS and set its value to 1")

    utils.add_attribute_to_remote_file(ssh,"/etc/glite-wms/glite_wms.conf",'WorkloadManagerProxy',['MaxPerusalFiles'],['1'])

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

    logging.info("Submit job")

    utils.use_external_jdl("%s.jdl"%(bug))

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Try to set perusal for files perusal.out and perusal.err")
    
    output=utils.run_command_fail_continue_on_error("glite-wms-job-perusal --set -f perusal.out -f perusal.err %s"%(JOBID))

    logging.info("Check failure reason (The maximum number of perusal files is reached)")

    if output.find("The maximum number of perusal files is reached")==-1:
       logging.error("Unexpected failure reason. Not found  'The maximum number of perusal files is reached'")
       logging.info("Restore the initial glite_wms.conf file")
       utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
       utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
       ssh.close()
       raise GeneralError("Check failure reason","Error !!! Unexpected failure reason. Not found 'The maximum number of perusal fils is reached'")

    utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))

    
    logging.info("Restore the initial glite_wms.conf file")
    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
    

    ssh.close()
    
    logging.info("End of regression test for bug %s"%(bug))
    