#
# Bug: 86485
# Title: ICE doesn't send the iceId to CREAM
# Link: https://savannah.cern.ch/bugs/?86485
#
#

import logging
import time

from libutils.Exceptions import *

def run(utils):

    bug='86485'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you need access to a CREAM CE and to WMS")

    if utils.WMS_USERNAME=='' or utils.WMS_PASSWORD=='' or utils.OTHER_HOST=='' or utils.USERNAME=='' or utils.PASSWORD=='':
        logging.error("Missing required variables WMS_USERNAME,WMS_PASSWORD,OTHER_HOST,USERNAME and PASSWORD from configuration file")
        raise GeneralError("Missing required variables","To verify this bug it is necessary to set WMS_USERNAME,WMS_PASSWORD,OTHER_HOST,USERNAME and PASSWORD in the configuration file")
    
   
    logging.info("Set CREAM CE %s in debug mode"%(utils.OTHER_HOST))

    ssh=utils.open_ssh(utils.OTHER_HOST,utils.USERNAME,utils.PASSWORD)

    file='/etc/glite-ce-cream/log4j.properties'

    logging.info("Change attributes at remote file %s"%(file))

    utils.remove("%s/local_copy"%(utils.get_tmp_dir()))

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

            logging.info("For attribute 'log4j.rootLogger change the value to debug")

            find=0

            for line in lines:

                 if line.find("=")!= -1:

                       attr=line.split("=")

                       if attr[0].strip()=='log4j.rootLogger' :
                            logging.info("Attribute log4j.rootLogger found")
                            lines[lines.index(line)]=line.replace(attr[1].strip(" \n"),'debug, fileout')
                            find=1

            if find==0:
                logging.error("Unable to find attribute log4j.rootLogger")
                raise GeneralError("Set CREAM in debug mode","Unable to find attribute log4j.rootLogger")

        
            #write changes to local copy of file
            logging.info("Save changes to %s/local_copy"%(utils.get_tmp_dir()))
            FILE=open("%s/local_copy"%(utils.get_tmp_dir()),"w")
            FILE.writelines(lines)
            FILE.close()

            #Save file again to remote host
            logging.info("Upload new version of file %s to remote host"%(file))
            ftp.put("%s/local_copy"%(utils.get_tmp_dir()),file)

            ftp.close()


    except Exception, e:
            logging.error("Error while edit file %s at remote host",file)
            logging.error("Error Description: %s",e)
            raise GeneralError("Set CREAM in debug mode","Error while edit file %s at remote host"%(file))


    logging.info("Back up current log file and then clear it")

    utils.execute_remote_cmd(ssh,"cp -f /var/log/cream/glite-ce-cream.log /var/log/cream/glite-ce-cream.log.bak")

    utils.execute_remote_cmd(ssh,"rm -f /var/log/cream/glite-ce-cream.log")

    logging.info("Restart tomcat")

    utils.execute_remote_cmd(ssh,"/etc/init.d/tomcat5 restart")

    logging.info("Prepare jdl for submission")

    utils.use_utils_jdl()

    utils.set_jdl(utils.get_jdl_file())

    utils.set_destination_ce(utils.get_jdl_file(),utils.OTHER_HOST)

    logging.info("Submit job")

    JOBID=utils.run_command_continue_on_error("glite-wms-job-submit %s -c %s --nomsg %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Wait 3 minutes")
    time.sleep(180)

    logging.info("Check in the CREAM log file if the iceid is reported")

    utils.ssh_get_file(ssh, "/var/log/cream/glite-ce-cream.log", "%s/local_copy"%(utils.get_tmp_dir()))

    FILE=open("%s/local_copy"%(utils.get_tmp_dir()))
    lines=FILE.readlines()
    FILE.close()

    find=0

    for line in lines:
        if line.find("selectToRetrieveJobStatusQuery")!=-1:
            if line.find("job.iceId =")!=-1:
               result=line
               find=1
               break

    if find==0:
        logging.error("Unable to find any entry in the cream log file with parameter 'selectToRetrieveJobStatusQuery'")
        raise GeneralError("","Unable to find any entry in the cream log file with parameter 'selectToRetrieveJobStatusQuery'")


    result=result.split("and")

    iceId=''

    for res in result:
        if res.find("job.iceId =")!=-1:
            iceId=res.split(" = ")[1].strip(" '\t\n")

    cream_id=''

    for line in lines:
        if line.find("jobId = https://%s:8443/ce-cream/services"%(utils.OTHER_HOST))!=-1:
            line=line.split(" = ")[1]
            cream_id=line.split("ce-cream/services/CREAM2/")[1].strip(" \n\t")
            break

    logging.info("Create SQL script file")

    utils.execute_remote_cmd(ssh,"echo \"SELECT iceId FROM job WHERE id='%s';\" > /root/test.sql"%(cream_id))

    logging.info("Check in the CREAM DB if the iceId is set for the job %s"%(JOBID))

    mysql_cmd="mysql -u %s --password=%s creamdb < /root/test.sql"%(utils.USERNAME,utils.PASSWORD)

    output=utils.execute_remote_cmd(ssh,mysql_cmd)

    if output.find(iceId)==-1:
        logging.error("Unable to find the iceId in the creamdb for the job %s"%(JOBID))
        raise GeneralError("","Unable to find the iceId in the creamdb for the jod %s"%(JOBID))


    ssh.close()

    ssh=utils.open_ssh(utils.WMS,utils.WMS_USERNAME,utils.WMS_PASSWORD)

    logging.info("Check the ice log file on the WMS for Returned CREAM-JOBID for job %s"%(JOBID))

    output=utils.execute_remote_cmd(ssh,"grep \"For GridJobID \[%s\] CREAM Returned CREAM-JOBID\" /var/log/wms/ice.log"%(JOBID))

    if output.find(cream_id)==-1:
        logging.error("Unable to find 'Returned CREAM-JOBID'entry for job %s in ice log file"%(JOBID))
        raise GeneralError("","Unable to find 'Returned CREAM-JOBID'entry for job %s in ice log file"%(JOBID))


    logging.info("Test OK")

    ssh.close()

    logging.info("End of regression test for bug %s"%(bug))
