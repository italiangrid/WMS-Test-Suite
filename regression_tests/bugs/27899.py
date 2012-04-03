#
# Bug:27899
# Title: VO override does not work with JdlDefaultAttributes
# Link: https://savannah.cern.ch/bugs/?27899
#
#

import logging
import socket

from libutils.Exceptions import *

def run(utils):

    bug='27899'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need root access to UI. You have to set USERNAME,PASSWORD and PROXY_PASSWORD attributes at configuration file")

    if utils.USERNAME=='' or utils.PASSWORD=='' or utils.PROXY_PASSWORD=='':
        logging.error("Missing required variables USERNAME,PASSWORD,PROXY_PASSWORD from configuration file")
        raise GeneralError("Missing required variables","To verify this bug it is necessary to set USERNAME,PASSWORD and PROXY_PASSWORD in the configuration file")

    configuration_file="/etc/glite-wms/%s/glite_wms.conf"%(utils.VO)

    logging.info("Edit configuration file %s by changing the VO attribute in JdlDefaultAttributes section")

    logging.info("Create new configuration file")

    FILE = open(configuration_file)
    lines=FILE.readlines()
    FILE.close()

    for line in lines:
        if line.find("JdlDefaultAttributes =  [")!=-1:
             start_index=lines.index(line)
        if line.find("];")!=-1:
             end_index=lines.index(line)

    section=lines[start_index:end_index]

    new_file=lines[0:start_index]

    find=0

    for line in section:
        if line.lower().find("virtualorganisation")!=-1:
            section[section.index(line)]="    Virtualorganisation = \"%s_test\";\n"%(utils.VO)
            new_file[start_index+1:end_index]=section
            new_file[end_index+1:]=lines[end_index:]
            find=1
            break

    if find==0:
        section.append("    Virtualorganisation = \"%s_test\";\n"%(utils.VO))
        new_file[start_index+1:end_index+1]=section
        new_file[end_index+2:]=lines[end_index:]


    FILE=open("%s/local_conf"%(utils.get_tmp_dir()),"w")
    FILE.writelines(new_file)
    FILE.close()

    ssh=utils.open_ssh(socket.gethostname(), utils.USERNAME, utils.PASSWORD)

    utils.execute_remote_cmd(ssh,"cp -f %s %s.bak"%(configuration_file,configuration_file))
    utils.execute_remote_cmd(ssh,"cp -f %s/local_conf %s"%(utils.get_tmp_dir(),configuration_file))
  
    logging.info("Create a new proxy")

    utils.run_command_continue_on_error("echo %s | voms-proxy-init -voms %s -pwstdin"%(utils.PROXY_PASSWORD,utils.VO))

    utils.use_utils_jdl()

    logging.info("Submit job")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Get job's info")

    job_info=utils.run_command_continue_on_error("glite-wms-job-info --jdl %s"%(JOBID))

    logging.info("Cancel the submitted job")

    utils.run_command_continue_on_error("glite-wms-job-cancel --noint %s"%(JOBID))

    logging.info("Check that the generated jdl has the same VO as the one used to generate the user proxy")

    VO=''

    for line in job_info.split("\n"):
        if line.find("VirtualOrganisation = ")!=-1:
            VO=line.split(" = ")[1].strip(" \"\t\n;")
            break

    if VO!=utils.VO:
       utils.execute_remote_cmd(ssh,"cp -f %s.bak %s"%(configuration_file,configuration_file))
       ssh.close()
       logging.error("Error the generated jdl hasn't the same VO as the one used to generate the user proxy")
       raise GeneralError("","Error the generated jdl hasn't the same VO as the one used to generate the user proxy")
    else:
       logging.info("The generated jdl has the same VO as the one used to generate the user proxy")

    utils.execute_remote_cmd(ssh,"cp -f %s.bak %s"%(configuration_file,configuration_file))
    ssh.close()
    
    logging.info("TEST OK")

    logging.info("End of regression test for bug %s",bug)
