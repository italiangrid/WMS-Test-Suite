#
# Bug: 64416
# Title: The proxycache purger needs to be made compatible with the latest gridsite releases
# Link: https://savannah.cern.ch/bugs/?64416
#
#


import time

from lib.Exceptions import *


def get_expired_certificates(ssh,utils,certificates):

    exp_certificates=[]

    for certificate in certificates:

        if certificate.find("userkey.pem")==-1:

            expiry_date=utils.execute_remote_cmd(ssh,"openssl x509 -in %s -noout -enddate"%(certificate.strip())).split("=")[1].strip("\n")

            now_epoch=time.time()

            expiry_epoch=utils.execute_remote_cmd(ssh,"date +%%s -d\"%s\""%(expiry_date))

            if now_epoch>expiry_epoch:
                exp_certificates.append(certificate)

    
    return exp_certificates


def run(utils):

    bug='64416'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    target_dir='/var/proxycache'

    utils.log_info("Get the list of the certificates")

    list_of_certificates=utils.execute_remote_cmd(ssh,"find %s -name *.pem"%(target_dir)).split("\n")[:-1]

    utils.log_info("Check which of them are exprired")

    expired_certificates=get_expired_certificates(ssh,utils,list_of_certificates)

    if len(expired_certificates)>0:

        utils.log_info("Run the proxycache purger ")

        utils.execute_remote_cmd(ssh,"cd %s && /usr/bin/glite-wms-wmproxy-purge-proxycache"%(target_dir))

        utils.log_info("Get the list of the certificates after proxycache purging")

        certificates_after_purging=utils.execute_remote_cmd(ssh,"find %s -name *.pem"%(target_dir)).split("\n")[:-1]

        for certificate in certificates_after_purging:
            certificates_after_purging[certificates_after_purging.index(certificate)]=certificate.lstrip()
    
        ssh.close()

        z=set(expired_certificates)&set(certificates_after_purging)

        if len(z)>0:
            utils.log_info("ERROR: The following exprired certificates have not removed after proxycache purging. Certificates: %s"%(z))
            raise GeneralError("Error found expired certificates","Error, the following expired certificates have not removed after purging. Certificates: %s"%(z))
        else:
            utils.log_info("Test OK")

        utils.log_info("End of regression test for bug %s"%(bug))

    else:
        ssh.close()
        utils.log_info("ERROR: Unable to find any expired proxy to test the proxycache purger operation")
        raise GeneralError("","Unable to find any expired proxy to test the proxycache purger operation")
