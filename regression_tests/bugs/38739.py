#
# Bug: 38739
# Title:WMProxy Server: doesn't allow exec if there's only user DN in gacl file
# Link: https://savannah.cern.ch/bugs/?38739
#


import logging

from libutils.Exceptions import *


def create_test_gacl(utils,userdn):

    FILE=open("%s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()),"w")

    FILE.write("<?xml version=\"1.0\"?>\n")
    FILE.write("<gacl version=\"0.0.1\">\n")
    FILE.write("<entry>\n")
    FILE.write("<any-user>\n")
    FILE.write("</any-user>\n")
    FILE.write("<deny><exec/></deny>\n")
    FILE.write("</entry>\n")
    FILE.write("<entry>\n")
    FILE.write("<voms>\n")
    FILE.write("<fqan>%s</fqan>\n"%(utils.VO))
    FILE.write("</voms>\n")
    FILE.write("<deny><exec/></deny>\n")
    FILE.write("</entry>\n")
    FILE.write("<entry>\n")
    FILE.write("<person>\n")
    FILE.write("<dn>%s</dn>\n"%(userdn))
    FILE.write("</person>\n")
    FILE.write("<allow><exec/></allow>\n")
    FILE.write("</entry>\n")
    FILE.write("</gacl>\n")

    FILE.close()


def run(utils):

    bug='38739'

    userdn=''

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have to set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    logging.info("Get current user DN")

    OUTPUT=utils.run_command_continue_on_error("voms-proxy-info")

    for line in OUTPUT.split("\n"):
        if line.find("identity") != -1:
            userdn=line.split(":")[1].strip()

    logging.info("Create file glite_wms_wmproxy.gacl which will be used during test execution")

    create_test_gacl(utils,userdn)
    
    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())
    
    logging.info("Transfer new glite_wms_wmproxy.gacl file to WMS and restart WMProxy")
    #back up old
    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms_wmproxy.gacl /etc/glite-wms/glite_wms_wmproxy.gacl.bak")
    #upload new
    utils.ssh_put_file(ssh,"%s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()),"/etc/glite-wms/glite_wms_wmproxy.gacl")
    #Restart service
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())

    logging.info("Try delegation")

    utils.run_command_continue_on_error("glite-wms-job-delegate-proxy --config %s -d test_delegate"%(utils.get_config_file()))

    logging.info("Try list match")
     
    utils.run_command_continue_on_error("glite-wms-job-list-match %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
  
    logging.info("Try job submission")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Try job cancel")

    utils.run_command_continue_on_error("glite-wms-job-cancel --config %s --noint %s"%(utils.get_config_file(),JOBID))

    
    logging.info("Restore the initial glite_wms_wmproxy.gacl file")
    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms_wmproxy.gacl.bak /etc/glite-wms/glite_wms_wmproxy.gacl")
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
    
    ssh.close()
        
    logging.info("End of regression test for bug %s"%(bug))
    