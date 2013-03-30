#
# Bug: 87261
# Title: WMproxy GACLs do not support wildcards (as they used to do)
# Link: https://savannah.cern.ch/bugs/?87261
#
#

from lib.Exceptions import *


def run(utils):

    bug='87261'

    cases=[
       '<gacl version="0.0.1"><entry> <voms> <fqan>/%s*</voms> <allow> <exec/> </allow> </entry></gacl>'%(utils.VO[:-1]),
       '<gacl version="0.0.1"><entry> <voms> <fqan>/%s%s*</voms> <allow> <exec/> </allow> </entry></gacl>'%(utils.VO[:-1],utils.VO[-1].capitalize()),
       '<gacl version="0.0.1"><entry> <voms> <fqan>/%s</voms> <allow> <exec/> </allow> </entry></gacl>'%(utils.VO),
       '<gacl version="0.0.1"><entry> <voms> <fqan>/%s</voms> <allow> <exec/> </allow></entry><entry> <voms> <fqan>/%s/*</voms> <allow> <exec/> </allow> </entry></gacl>'%(utils.VO,utils.VO)
    ]
  
    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")


    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    #back up existing glite_wms_wmproxy.gacl    
    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms_wmproxy.gacl /etc/glite-wms/glite_wms_wmproxy.gacl.bak")

    try:

        utils.log_info("TEST CASE 1")

        utils.log_info("Create file glite_wms_wmproxy.gacl which will be used during test execution")

        FILE=open("%s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()),"w")
        FILE.write(cases[0])
        FILE.close()

        utils.log_info("Use glite_wms_wmproxy.gacl:\n%s"%(utils.run_command("cat %s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()))))

        utils.log_info("Transfer new glite_wms_wmproxy.gacl file to WMS and restart WMProxy")

        utils.ssh_put_file(ssh,"%s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()),"/etc/glite-wms/glite_wms_wmproxy.gacl")
        utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

        utils.log_info("Try job list-match")
        utils.run_command("glite-wms-job-list-match %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
        utils.log_info("list-match executed successfully as expected")

        utils.log_info("TEST CASE 2")

        utils.log_info("Create file glite_wms_wmproxy.gacl which will be used during test execution")

        FILE=open("%s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()),"w")
        FILE.write(cases[1])
        FILE.close()

        utils.log_info("Use glite_wms_wmproxy.gacl:\n%s"%(utils.run_command("cat %s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()))))

        utils.log_info("Transfer new glite_wms_wmproxy.gacl file to WMS and restart WMProxy")

        utils.ssh_put_file(ssh,"%s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()),"/etc/glite-wms/glite_wms_wmproxy.gacl")
        utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

        utils.log_info("Try job list-match")
        utils.run_command_fail("glite-wms-job-list-match %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
        utils.log_info("list-match failed as expected")

        utils.log_info("TEST CASE 3")

        utils.log_info("Create file glite_wms_wmproxy.gacl which will be used during test execution")

        FILE=open("%s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()),"w")
        FILE.write(cases[2])
        FILE.close()

        utils.log_info("Use glite_wms_wmproxy.gacl:\n%s"%(utils.run_command("cat %s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()))))

        utils.log_info("Transfer new glite_wms_wmproxy.gacl file to WMS and restart WMProxy")

        utils.ssh_put_file(ssh,"%s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()),"/etc/glite-wms/glite_wms_wmproxy.gacl")
        utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

        utils.log_info("Try job list-match")
        utils.run_command_fail("glite-wms-job-list-match %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
        utils.log_info("list-match failed as expected")

        utils.log_info("TEST CASE 4")

        utils.log_info("Create file glite_wms_wmproxy.gacl which will be used during test execution")

        FILE=open("%s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()),"w")
        FILE.write(cases[3])
        FILE.close()

        utils.log_info("Use glite_wms_wmproxy.gacl:\n%s"%(utils.run_command("cat %s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()))))

        utils.log_info("Transfer new glite_wms_wmproxy.gacl file to WMS and restart WMProxy")

        utils.ssh_put_file(ssh,"%s/test-glite_wms_wmproxy.gacl"%(utils.get_tmp_dir()),"/etc/glite-wms/glite_wms_wmproxy.gacl")
        utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

        utils.log_info("Try job list-match")
        utils.run_command("glite-wms-job-list-match %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
        utils.log_info("list-match executed successfully as expected")


    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_info("Restore the initial glite_wms_wmproxy.gacl file")
        utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms_wmproxy.gacl.bak /etc/glite-wms/glite_wms_wmproxy.gacl")
        utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
        utils.close_ssh(ssh)
        raise GeneralError(e.expression,e.message)


    utils.log_info("Restore the initial glite_wms_wmproxy.gacl file")
    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms_wmproxy.gacl.bak /etc/glite-wms/glite_wms_wmproxy.gacl")
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
    utils.close_ssh(ssh)

    utils.log_info("End of regression test for bug %s"%(bug))

