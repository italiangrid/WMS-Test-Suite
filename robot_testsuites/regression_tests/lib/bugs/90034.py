#
# Bug: 90034
# Title: LB failover mechanism in WMproxy needs to be reviewed
# Link: https://savannah.cern.ch/bugs/?90034
#
#

from lib.Exceptions import *

def add_lb_server(utils,ssh):

    utils.remove("%s/local_copy"%(utils.get_tmp_dir()))

    file="/etc/glite-wms/glite_wms.conf"

    try:

            utils.execute_remote_cmd(ssh, "cp -f %s %s.bak"%(file,file))

            ftp = ssh.open_sftp()

            utils.log_info("Get file %s"%(file))

            #Get required file from remote host
            ftp.get(file,"%s/local_copy"%(utils.get_tmp_dir()))

            utils.log_info("Read file %s"%(file))

            #Read contents from file
            FILE=open("%s/local_copy"%(utils.get_tmp_dir()),"r")
            lines=FILE.readlines()
            FILE.close()

            lb_server_init=""

            for line in lines:
                if line.find("LBServer")!=-1:
                     lb_server_init=line
                     break
 
            start =lb_server_init.index("{")+1
            end =  lb_server_init.index("}")

            old=lb_server_init[start:end]

            new='"someunknown.somehost.org:9000",%s'%(old)

            utils.log_info("For attribute LBServer change the value from %s to %s"%(old,new))

            find=0
            
            for line in lines:

                    if line.find("=")!= -1:

                       attr=line.split("=")

                       if attr[0].strip()=="LBServer":
                            utils.log_info("Attribute LBServer found")
                            lines[lines.index(line)]=line.replace(old,new)
                            find=1
                            break

            if find==0:
                utils.log_info("ERROR: Unable to find attribute LBServer")
                raise GeneralError("Method change_remote_file","Unable to find attribute LBServer")

            #write changes to local copy of file
            utils.log_info("Save changes to %s/local_copy"%(utils.get_tmp_dir()))
            FILE=open("%s/local_copy"%(utils.get_tmp_dir()),"w")
            FILE.writelines(lines)
            FILE.close()

            #Save file again to remote host
            utils.log_info("Upload new version of file %s to remote host"%(file))
            ftp.put("%s/local_copy"%(utils.get_tmp_dir()),file)

            ftp.close()

            return old

    except Exception, e:
            utils.log_info("Error while edit file %s at remote host",file)
            utils.log_info("Error Description: %s",e)
            raise GeneralError("Method change_remote_file","Error while edit file %s at remote host"%(file))


def run(utils):

    bug='90034'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("Put an invalid URL for the first LB in the WorkloadManagerProxy configuration file")

    init_lb_servers=add_lb_server(utils,ssh)

    utils.log_info("Restart Workload Manager Proxy")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

    utils.log_info("Prepare jdl file for submission")

    utils.use_utils_jdl()

    utils.log_info("Submit a job")

    try:

         JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    except (RunCommandError,GeneralError) , e :
            utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
            utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
            utils.close_ssh(ssh)
            utils.log_info("Job submission failed")
            utils.log_info("Error Description: %s",e.message)
            raise GeneralError("Job submission failed","Job submission failed: %s"%(e.message))
    
    lb_hostname=JOBID.split("https://")[1].split(":9000")[0]
    
    utils.log_info("Job submitted successfully")

    utils.log_info("Check if some other LB (not the first) from the vector was picked up ")

    if init_lb_servers.find(lb_hostname)!=-1:
        utils.log_info("OK some other LB from the vector was picked up")
    else:
        utils.log_info("ERROR: An unknown LB was picked up , not from the LBServers vector")
        raise GeneralError("Check the used LB","An unknown LB was picked up , not from the LBServers vector")

    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
    utils.close_ssh(ssh)

    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))

