from Exceptions import *


def get_section_attributes(utils,file,section):

    utils.log_info("Get attributes for section %s"%(section))

    skip_attributes=['ListMatchParadise','II_Contact','WMExpiryPeriod','MatchRetryPeriod','LBServer','IsmIiLDAPCEFilterExt','RuntimeMalloc','ExpiryPeriod','MaxPerusalFiles','listener_port']

    #Read contents from file
    FILE=open(file,"r")
    lines=FILE.readlines()
    FILE.close()

    row_start=0
    row_end=0

    attributes=[]

    for line in lines:
      if line.find("%s = "%(section))!=-1:
          row_start=lines.index(line)+1
          break

    lines=lines[row_start:]

    for line in lines:
      if line.find("    ];")!=-1:
          row_end=lines.index(line)

    for line in lines[:row_end]:

        value=[line[:-1].lstrip().split("=")[0].strip(' \t\n\r')]

        z=set(skip_attributes)&set(value)

        if(len(z))==0:
          attributes.append(line[:-1].lstrip())

    return attributes


def check_section(utils,section,expected_attributes):

 
    attributes=get_section_attributes(utils,"%s/glite_wms.conf_local"%(utils.get_tmp_dir()),section)

    z=set(attributes)^set(expected_attributes)

    if(len(z)>0): 
        utils.log_info("Section: %s , problem with following attributes: %s"%(section,z))
        raise GeneralError("","Section: %s , problem with following attributes: %s"%(section,z))
         
####
####  YAIM_FILE local copy of the yaim configuration file ( NOTE!!!! Test does not download the corresponding configuration 
###   file from the WMS host.)
####
def check_variables(utils):
  
    fail_msg=[]
   
    utils.log_info("Read yaim configuration file %s"%(utils.YAIM_FILE))

    FILE = open(utils.YAIM_FILE,"r")
    lines=FILE.readlines()
    FILE.close()

    utils.log_info("Read wms configuration file")

    FILE = open("%s/glite_wms.conf_local"%(utils.get_tmp_dir()),"r")
    conf_lines=FILE.readlines()
    FILE.close()

    wms_expiry_period=''
    wms_match_retry_period=''
    conf_wms_expiry_period=''
    conf_wms_match_retry_period=''

    for line in lines:

        if line.find("BDII_HOST") != -1 :
           bdii_host=line.split("=")[1].strip(" \"\n\t")
        
        if line.find("LB_HOST") != -1 :
           lb_host=line.split("=")[1].strip(" \"\n\t")

        if line.find("VOS") != -1 :
            vos=line.split("=")[1].strip(" \"\n\t").split(" ")

        if line.find("WMS_EXPIRY_PERIOD") != -1 :
           wms_expiry_period=line.split("=")[1].strip(" \"\n\t")

        if line.find("WMS_MATCH_RETRY_PERIOD") != -1 :
            wms_match_retry_period=line.split("=")[1].strip(" \"\n\t")

    for line in conf_lines:

        if line.find("II_Contact") != -1 :
           ii_contact=line.split("=")[1].strip(" ;\"\"\n\t")

        if line.find("LBServer") != -1 :
           lb_server=line.split("=")[1].strip(" \"\n\t")

        if line.find("IsmIiLDAPCEFilterExt") != -1 :
            ism_filter=line.split("IsmIiLDAPCEFilterExt  =")[1].strip(" ;\"\n\t")

        if line.find("WMExpiryPeriod") != -1 :
           conf_wms_expiry_period=line.split("=")[1].strip(" ;\"\n\t")

        if line.find("MatchRetryPeriod") != -1 :
           conf_wms_match_retry_period=line.split("=")[1].strip(" ;\"\n\t")

    utils.log_info("Check value of II_Contact attribute")

    if bdii_host.find(ii_contact)==-1:
       utils.log_info("Error, for attribute II_Contact value is %s while expected %s"%(ii_contact,bdii_host))
       #raise GeneralError("","Error, for attriute II_Contact value is %s while expected %s"%(ii_contact,bdii_host))
       fail_msg.append("Error, for attriute II_Contact value is %s while expected %s"%(ii_contact,bdii_host))
    else:
       utils.log_info("II_Contact attribute: OK ")

    utils.log_info("Check value of LBServer attribute")

    if lb_server.find(lb_host)==-1:
       utils.log_info("Error, for attribute LBServer value is %s while expected %s"%(lb_server,lb_host))
       #raise GeneralError("","Error, for attribute LBServer value is %s while expected %s"%(lb_server,lb_host))
       fail_msg.append("Error, for attribute LBServer value is %s while expected %s"%(lb_server,lb_host))
    else:
       utils.log_info("II_Contact attribute: OK ")


    for vo in vos:
        
        utils.log_info("Check value of IsmIiLDAPCEFilterExt attribute for VO: %s"%(vo))

        if ism_filter.find("GlueCEAccessControlBaseRule=VO:%s"%(vo))==-1:
            utils.log_info("Error, not find GlueCEAccessControlBaseRule=VO:%s for VO %s"%(vo,vo))
            #raise GeneralError("","Error, not find GlueCEAccessControlBaseRule=VO:%s for VO %s"%(vo,vo))
            fail_msg.append("Error, not find GlueCEAccessControlBaseRule=VO:%s for VO %s"%(vo,vo)) 
        else:
            utils.log_info("Find GlueCEAccessControlBaseRule=VO:%s for VO %s"%(vo,vo))

        if ism_filter.find("GlueCEAccessControlBaseRule=VOMS:/%s/*"%(vo))==-1:
            utils.log_info("Error, not find GlueCEAccessControlBaseRule=VOMS:/%s/* for VO %s"%(vo,vo))
            #raise GeneralError("","Error, not find GlueCEAccessControlBaseRule=VOMS:/%s/* for VO %s"%(vo,vo))
            fail_msg.append("Error, not find GlueCEAccessControlBaseRule=VOMS:/%s/* for VO %s"%(vo,vo))
        else:
            utils.log_info("Find GlueCEAccessControlBaseRule=VOMS:/%s/* for VO %s"%(vo,vo))


    if wms_expiry_period!='':
    
        utils.log_info("Check value of WMExpiryPeriod attribute")

        if int(conf_wms_expiry_period) != int(wms_expiry_period):
            utils.log_info("Error, for attribute WMExpiryPeriod value is %s while expected %s"%(conf_wms_expiry_period,wms_expiry_period))
            #raise GeneralError("","Error, for attribute WMExpiryPeriod value is %s while expected %s"%(conf_wms_expiry_period,wms_expiry_period))
            fail_msg.append("Error, for attribute WMExpiryPeriod value is %s while expected %s"%(conf_wms_expiry_period,wms_expiry_period))
        else:
            utils.log_info("WMExpiryPeriod attribute: OK ")
        

    if wms_match_retry_period!='':

        utils.log_info("Check value of MatchRetryPeriod attribute")

        if int(conf_wms_match_retry_period) != int(wms_match_retry_period):
            utils.log_info("Error, for attribute MatchRetryPeriod value is %s while expected %s"%(conf_wms_match_retry_period,wms_match_retry_period))
            #raise GeneralError("","Error, for attribute MatchRetryPeriod value is %s while expected %s"%(conf_wms_match_retry_period,wms_match_retry_period))
            fail_msg.append("Error, for attribute WMExpiryPeriod value is %s while expected %s"%(conf_wms_expiry_period,wms_expiry_period))
        else:
            utils.log_info("MatchRetryPeriod attribute: OK ")

    if len(fail_msg)>0:
       raise GeneralError("",'  '.join(fail_msg))        
