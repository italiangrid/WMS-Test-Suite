#
# Bug:50009
# Title: Request for a feature allowing propagation of generic parameters from JDL to LRMS
# Link: https://savannah.cern.ch/bugs/?50009
#
#

from lib.Exceptions import *

def create_test_gacl(utils,userdn):

    FILE=open("%s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()),"w")

    FILE.write("<?xml version=\"1.0\"?>\n")
    FILE.write("<gacl version=\"0.0.1\">\n")
    
    FILE.write("<entry>\n")
    FILE.write("<person>\n")
    FILE.write("<dn>%s</dn>\n"%(userdn))
    FILE.write("</person>\n")
    FILE.write("<allow><exec/></allow>\n")
    FILE.write("</entry>\n")

    FILE.write("<entry>\n")
    FILE.write("<voms>\n")
    FILE.write("<fqan>%s/ROLE=lcgadmin</fqan>\n"%(utils.VO))
    FILE.write("</voms>\n")
    FILE.write("<allow><exec/></allow>\n")
    FILE.write("</entry>\n")

    FILE.write("<entry>\n")
    FILE.write("<voms>\n")
    FILE.write("<fqan>%s/ROLE=production</fqan>\n"%(utils.VO))
    FILE.write("</voms>\n")
    FILE.write("<allow><exec/></allow>\n")
    FILE.write("</entry>\n")

    FILE.write("<entry>\n")
    FILE.write("<voms>\n")
    FILE.write("<fqan>%s</fqan>\n"%(utils.VO))
    FILE.write("</voms>\n")
    FILE.write("<allow><exec/></allow>\n")
    FILE.write("</entry>\n")

    FILE.write("</gacl>\n")

    FILE.close()


def run(utils):

    bug='50009'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    utils.log_info("Create file glite_wms_wmproxy.gacl which will be used during test execution")

    create_test_gacl(utils,"foo")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Transfer new glite_wms_wmproxy.gacl file to WMS and restart WMProxy")
    #back up old
    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms_wmproxy.gacl /etc/glite-wms/glite_wms_wmproxy.gacl.bak")
    #upload new
    utils.ssh_put_file(ssh,"%s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()),"/etc/glite-wms/glite_wms_wmproxy.gacl")
    #Restart service
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())

    utils.log_info("Try job submission")

    output=utils.run_command_fail("glite-wms-job-submit %s --config %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
   
    utils.log_info("Restore the initial glite_wms_wmproxy.gacl file")
    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms_wmproxy.gacl.bak /etc/glite-wms/glite_wms_wmproxy.gacl")
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

    ssh.close()

    utils.log_info("End of regression test for bug %s"%(bug))
