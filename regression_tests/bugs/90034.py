#
# Bug: 90034
# Title: LB failover mechanism in WMproxy needs to be reviewed
# Link: https://savannah.cern.ch/bugs/?90034
#
#

import logging

from libutils.Exceptions import *


def add_lb_server(utils,ssh):

    utils.remove("%s/local_copy"%(utils.get_tmp_dir()))

    file="/etc/glite-wms/glite_wms.conf"

    try:

            utils.execute_remote_cmd(ssh, "cp -f %s %s.bak"%(file,file))

            ftp = ssh.open_sftp()

            logging.info("Get file %s"%(file))

            #Get required file from remote host
            ftp.get(file,"%s/local_copy"%(utils.get_tmp_dir()))

            logging.info("Read file %s"%(file))

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

            logging.info("For attribute LBServer change the value from %s to %s"%(old,new))

            find=0
            
            for line in lines:

                    if line.find("=")!= -1:

                       attr=line.split("=")

                       if attr[0].strip()=="LBServer":
                            logging.info("Attribute LBServer found")
                            lines[lines.index(line)]=line.replace(old,new)
                            find=1
                            break

            if find==0:
                logging.error("Unable to find attribute LBServer")
                raise GeneralError("Method change_remote_file","Unable to find attribute LBServer")

            #write changes to local copy of file
            logging.info("Save changes to %s/local_copy"%(utils.get_tmp_dir()))
            FILE=open("%s/local_copy"%(utils.get_tmp_dir()),"w")
            FILE.writelines(lines)
            FILE.close()

            #Save file again to remote host
            logging.info("Upload new version of file %s to remote host"%(file))
            ftp.put("%s/local_copy"%(utils.get_tmp_dir()),file)

            ftp.close()

            return old

    except Exception, e:
            logging.error("Error while edit file %s at remote host",file)
            logging.error("Error Description: %s",e)
            raise GeneralError("Method change_remote_file","Error while edit file %s at remote host"%(file))


def run(utils):

    bug='90034'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
    
    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    logging.info("Put an invalid URL for the first LB in the WorkloadManagerProxy configuration file")

    init_lb_servers=add_lb_server(utils,ssh)

    logging.info("Restart Workload Manager Proxy")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")

    logging.info("Prepare jdl file for submission")

    utils.use_utils_jdl()

    logging.info("Submit a job")

    try:

         JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    except (RunCommandError,GeneralError) , e :
            utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
            utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
            utils.close_ssh(ssh)
            logging.error("Job submission failed")
            logging.error("Error Description: %s",e.message)
            raise GeneralError("Job submission failed","Job submission failed: %s"%(e.message))
    
    lb_hostname=JOBID.split("https://")[1].split(":9000")[0]
    
    logging.info("Job submitted successfully")

    logging.info("Check if some other LB (not the first) from the vector was picked up ")

    if init_lb_servers.find(lb_hostname)!=-1:
        logging.info("OK some other LB from the vector was picked up")
    else:
        logging.error("An unknown LB was picked up , not from the LBServers vector")
        raise GeneralError("Check the used LB","An unknown LB was picked up , not from the LBServers vector")

    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wmproxy restart")
    utils.close_ssh(ssh)

    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))

