#! /usr/bin/python

import sys
import signal
import logging

import Test_utils
import SSH_utils

from Exceptions import *


def get_section_attributes(file,section):

    logging.info("Get attributes for section %s"%(section))

    skip_attributes=['ListMatchParadise','II_Contact','WMExpiryPeriod','MatchRetryPeriod','LBServer','RuntimeMalloc','ExpiryPeriod','MaxPerusalFiles','listener_port']

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


def check_section(utils,title,section,expected_attributes):

    fails=0

    utils.show_progress(title)

    utils.info(title)

    attributes=get_section_attributes("%s/glite_wms.conf_local"%(utils.get_tmp_dir()),section)

    z=set(attributes)^set(expected_attributes)

    if(len(z)>0): 
        utils.log_error(title)
        utils.log_error("Section: %s , problem with following attributes: %s"%(section,z))
        utils.log_error("")
        logging.error("Section: %s , problem with following attributes: %s"%(section,z))

        fails=fails+1
        
    else:
        utils.info("Test OK")


    return fails


def check_variables(utils,title):

    fails=0

    fail_msg=[]

    utils.show_progress(title)

    utils.info(title)
    
    logging.info("Read yaim configuration file %s"%(utils.YAIM_FILE))

    FILE = open(utils.YAIM_FILE,"r")
    lines=FILE.readlines()
    FILE.close()

    logging.info("Read wms configuration file")

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

    logging.info("Check value of II_Contact attribute")

    if bdii_host.find(ii_contact)==-1:
       logging.error("Error, for attribute II_Contact value is %s while expected %s"%(ii_contact,bdii_host))
       fail_msg.append("Error, for attriute II_Contact value is %s while expected %s"%(ii_contact,bdii_host))
       fails=fails+1
    else:
       logging.info("II_Contact attribute: OK ")

    logging.info("Check value of LBServer attribute")

    if lb_server.find(lb_host)==-1:
       logging.error("Error, for attribute LBServer value is %s while expected %s"%(lb_server,lb_host))
       fail_msg.append("Error, for attribute LBServer value is %s while expected %s"%(lb_server,lb_host))
       fails=fails+1
    else:
       logging.info("II_Contact attribute: OK ")


    for vo in vos:
        
        logging.info("Check value of IsmIiLDAPCEFilterExt attribute for VO: %s"%(vo))

        if ism_filter.find("GlueCEAccessControlBaseRule=VO:%s"%(vo))==-1:
            logging.error("Error, not find GlueCEAccessControlBaseRule=VO:%s for VO %s"%(vo,vo))
            fail_msg.append("Error, not find GlueCEAccessControlBaseRule=VO:%s for VO %s"%(vo,vo))
            fails=fails+1
        else:
            logging.info("Find GlueCEAccessControlBaseRule=VO:%s for VO %s"%(vo,vo))

        if ism_filter.find("GlueCEAccessControlBaseRule=VOMS:/%s/*"%(vo))==-1:
            logging.error("Error, not find GlueCEAccessControlBaseRule=VOMS:/%s/* for VO %s"%(vo,vo))
            fail_msg.append("Error, not find GlueCEAccessControlBaseRule=VOMS:/%s/* for VO %s"%(vo,vo))
            fails=fails+1
        else:
            logging.info("Find GlueCEAccessControlBaseRule=VOMS:/%s/* for VO %s"%(vo,vo))


    if wms_expiry_period!='':
    
        logging.info("Check value of WMExpiryPeriod attribute")

        if int(conf_wms_expiry_period) != int(wms_expiry_period):
            logging.error("Error, for attribute WMExpiryPeriod value is %s while expected %s"%(conf_wms_expiry_period,wms_expiry_period))
            fail_msg.append("Error, for attribute WMExpiryPeriod value is %s while expected %s"%(conf_wms_expiry_period,wms_expiry_period))
            fails=fails+1
        else:
            logging.info("WMExpiryPeriod attribute: OK ")
        

    if wms_match_retry_period!='':

        logging.info("Check value of MatchRetryPeriod attribute")

        if int(conf_wms_match_retry_period) != int(wms_match_retry_period):
            logging.error("Error, for attribute MatchRetryPeriod value is %s while expected %s"%(conf_wms_match_retry_period,wms_match_retry_period))
            fail_msg.append("Error, for attribute MatchRetryPeriod value is %s while expected %s"%(conf_wms_match_retry_period,wms_match_retry_period))
            fails=fails+1
        else:
            logging.info("MatchRetryPeriod attribute: OK ")
        

    if fails > 0:
      utils.log_error(title)
      utils.log_error(fail_msg)
      utils.log_error("")

    return fails


common_attributes=['HostProxyFile  =  "${WMS_LOCATION_VAR}/glite/wms.proxy";','LBProxy  =  true;','DGUser  =  "${GLITE_WMS_USER}";']

jobcontroller_attributes=['Input  =  "${WMS_LOCATION_VAR}/jobcontrol/jobdir/";',
    'ContainerRefreshThreshold  =  1000;',
    'CondorQuery  =  "${CONDORG_INSTALL_PATH}/bin/condor_q";',
    'LogFile  =  "${WMS_LOCATION_LOG}/jobcontroller_events.log";',
    'MaximumTimeAllowedForCondorMatch  =  1800;',
    'CondorRelease  =  "${CONDORG_INSTALL_PATH}/bin/condor_release";',
    'OutputFileDir  =  "${WMS_LOCATION_VAR}/jobcontrol/condorio";',
    'CondorRemove  =  "${CONDORG_INSTALL_PATH}/bin/condor_rm";',
    'LockFile  =  "${WMS_LOCATION_VAR}/jobcontrol/lock";',
    'SubmitFileDir  =  "${WMS_LOCATION_VAR}/jobcontrol/submit";',
    'CondorSubmit  =  "${CONDORG_INSTALL_PATH}/bin/condor_submit";',
    'LogLevel  =  5;']

networkserver_attributes=['II_Timeout  =  100;',
    'EnableQuotaManagement  =  false;',
    'QuotaInsensibleDiskPortion  =  2.0;',
    'SandboxStagingPath  =  "${WMS_LOCATION_VAR}/SandboxDir";',
    'II_DN  =  "mds-vo-name=local, o=grid";',
    'MasterThreads  =  8;',
    'ConnectionTimeout  =  300;',
    'LogFile  =  "${WMS_LOCATION_LOG}/networkserver_events.log";',
    'LogLevel  =  5;',
    'II_Port   =  2170;',
    'QuotaAdjustmentAmount  =  10000;',
    'DispatcherThreads  =  10;',
    'Gris_DN  =  "mds-vo-name=local, o=grid";',
    'Gris_Port  =  2170;',
    'DLI_SI_CatalogTimeout  =  60;',
    'EnableDynamicQuotaAdjustment  =  false;',
    'Gris_Timeout  =  20;',
    'BacklogSize  =  64;',
    'ListeningPort  =  7772;',
    'MaxInputSandboxSize  =  10000000;'
]

logmonitor_attributes = ['CondorLogRecycleDir  =  "${WMS_LOCATION_VAR}/logmonitor/CondorG.log/recycle";',
    'LockFile  =  "${WMS_LOCATION_VAR}/logmonitor/lock";',
    'AbortedJobsTimeout  =  600;',
    'CondorLogDir  =  "${WMS_LOCATION_VAR}/logmonitor/CondorG.log";',
    'MonitorInternalDir  =  "${WMS_LOCATION_VAR}/logmonitor/internal";',
    'MainLoopDuration  =  5;',
    'GlobusDownTimeout  =  7200;',
    'LogLevel  =  5;',
    'JobsPerCondorLog  =  1000;',
    'LogFile  =  "${WMS_LOCATION_LOG}/logmonitor_events.log";',
    'ExternalLogFile  =  "${WMS_LOCATION_LOG}/logmonitor_external.log";',
    'RemoveJobFiles  =  true;',
    'IdRepositoryName  =  "irepository.dat";',
    'ForceCancellationRetries  =  2;'
]

workloadmanager_attributes = [
    'SbRetryDifferentProtocols  =  true;', 
    'DisablePurchasingFromGris  =  true;',
    'IsmBlackList  =  {};',
    'JobWrapperTemplateDir  =  "${WMS_JOBWRAPPER_TEMPLATE}";',
    'IsmDump  =  "${WMS_LOCATION_VAR}/workload_manager/ismdump.fl";',
    'IsmIiPurchasingRate  =  480;',
    'MaxReplansCount  =  5;',
    'EnableRecovery  =  true;',
    'LogLevel  =  5;',
    'LogFile   =  "${WMS_LOCATION_LOG}/workload_manager_events.log";',
    'DliServiceName  =  "data-location-interface";',
    'IsmUpdateRate  =  600;',
    'WmsRequirements   =  ((ShortDeadlineJob =?= TRUE ? RegExp(".*sdj$", other.GlueCEUniqueID) : !RegExp(".*sdj$", other.GlueCEUniqueID)) && (other.GlueCEPolicyMaxTotalJobs == 0 || other.GlueCEStateTotalJobs < other.GlueCEPolicyMaxTotalJobs) && (EnableWmsFeedback =?= TRUE ? RegExp("cream", other.GlueCEImplementationName, "i") : true) && (member(CertificateSubject,other.GlueCEAccessControlBaseRule) || member(strcat("VO:",VirtualOrganisation),other.GlueCEAccessControlBaseRule) || FQANmember(strcat("VOMS:", VOMS_FQAN), other.GlueCEAccessControlBaseRule)) is true && FQANmember(strcat("DENY:",VOMS_FQAN), other.GlueCEAccessControlBaseRule) isnt true && (IsUndefined(other.OutputSE) || member(other.OutputSE, other.GlueCESEBindGroupSEUniqueID)));',
    'CeMonitorAsynchPort  =  0;',
    'QueueSize  =  1000;',
    'EnableBulkMM  =  true;',
    'MaxRetryCount  =  10;',
    'SiServiceName  =  "org.glite.SEIndex";',
    'IsmThreads  =  false;',
    'MaxOutputSandboxSize  =  -1;',
    'CeMonitorServices  =  {};',
    'ReplanGracePeriod  =  3600;',
    'Input  =  "${WMS_LOCATION_VAR}/workload_manager/jobdir";',
    'WorkerThreads  =  5;',
    'IsmIiG2LDAPCEFilterExt  =  "(|(&(objectclass=GLUE2ComputingService)(|(GLUE2ServiceType=org.glite.ce.ARC)(GLUE2ServiceType=org.glite.ce.CREAM)))(|(objectclass=GLUE2ComputingManager)(|(objectclass=GLUE2ComputingShare)(|(&(objectclass=GLUE2ComputingEndPoint)(GLUE2EndpointInterfaceName=org.glite.ce.CREAM))(|(objectclass=GLUE2ToStorageService)(|(&(objectclass=GLUE2MappingPolicy)(GLUE2PolicyScheme=org.glite.standard))(|(&(objectclass=GLUE2AccessPolicy)(GLUE2PolicyScheme=org.glite.standard))(|(objectclass=GLUE2ExecutionEnvironment)(|(objectclass=GLUE2ApplicationEnvironment)(|(objectclass=GLUE2Benchmark)))))))))))";',
    'IsmIiLDAPCEFilterExt  =  "(|(GlueCEAccessControlBaseRule=VO:testers.eu-emi.eu)(GlueCEAccessControlBaseRule=VOMS:/testers.eu-emi.eu/*)(GlueCEAccessControlBaseRule=VO:testers2.eu-emi.eu)(GlueCEAccessControlBaseRule=VOMS:/testers2.eu-emi.eu/*)(GlueCEAccessControlBaseRule=VO:cms)(GlueCEAccessControlBaseRule=VOMS:/cms/*)(GlueCEAccessControlBaseRule=VO:dteam)(GlueCEAccessControlBaseRule=VOMS:/dteam/*)(GlueCEAccessControlBaseRule=VO:infngrid)(GlueCEAccessControlBaseRule=VOMS:/infngrid/*))";',
    'CeForwardParameters  =  {"GlueHostMainMemoryVirtualSize","GlueHostMainMemoryRAMSize","GlueCEPolicyMaxCPUTime", "GlueCEPolicyMaxObtainableCPUTime", "GlueCEPolicyMaxObtainableWallClockTime", "GlueCEPolicyMaxWallClockTime" };',
    'IiGlueLib  =  "libglite_wms_ism_ii_purchaser.so.0";',
    'IsmIiG2LDAPSEFilterExt   =  "(|(objectclass=GLUE2StorageService)(|(objectclass=GLUE2StorageManager)(|(objectclass=GLUE2StorageShare)(|(objectclass=GLUE2StorageEndPoint)(|(objectclass=GLUE2MappingPolicy)(|(objectclass=GLUE2AccessPolicy)(|(objectclass=GLUE2DataStore)(|(objectclass=GLUE2StorageServiceCapacity)(|(objectclass=GLUE2StorageShareCapacity))))))))))";;',
    'EnableIsmIiGlue13Purchasing  =  true;',
    'EnableIsmIiGlue20Purchasing  =  false;',
    'BrokerLib  =  "libglite_wms_helper_broker_ism.so.0";'
]

wmproxy_attributes = [

    'EnableServiceDiscovery  =  false;',
    'ListMatchRootPath  =  "/tmp";',
    'OperationLoadScripts =  [',
    'jobSubmit  =  "${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobSubmit --load1 22 --load5 20 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 1500  --ftpconn 300";',
    'jobRegister  =  "${WMS_LOCATION_SBIN}/glite_wms_wmproxy_load_monitor --oper jobRegister --load1 22 --load5 20 --load15 18 --memusage 99 --diskusage 95 --fdnum 1000 --jdnum 1500 --ftpconn 300";',
    '];',
    'MinPerusalTimeInterval  =  1000;',
    'MaxServedRequests  =  50;',
    'ServiceDiscoveryInfoValidity  =  3600;',
    'LBServiceDiscoveryType  =  "org.glite.lb.server";',
    'LogLevel  =  5;',
    'SandboxStagingPath  =  "${WMS_LOCATION_VAR}/SandboxDir";',
    'WeightsCacheValidity  =  86400;',
    'LogFile  =  "${WMS_LOCATION_LOG}/wmproxy.log";',
    'AsyncJobStart  =  true;',
    'GridFTPPort  =  2811;',
    'MaxInputSandboxSize  =  100000000;',
    'ArgusAuthz  =  false;',
    'ArgusPepdEndpoints  =  {};'
]

ice_attributes = [

    'job_cancellation_threshold_time   =   300;',
    'max_logfile_size   =   100*1024*1024;',
    'cream_url_prefix   =   "https://";',
    'start_subscription_updater   =   true;',
    'max_ice_mem  =  2096000;',
    'subscription_update_threshold_time   =   3600;',
    'ice_log_level   =   300;',
    'listener_enable_authn   =   true;',
    'listener_enable_authz   =   true;',
    'poller_status_threshold_time   =   30*60;',
    'lease_update_frequency   =   20*60;',
    'lease_delta_time   =   0;',
    'cream_url_postfix   =   "/ce-cream/services/CREAM2";',
    'subscription_duration   =   86400;',
    'start_lease_updater   =   false;',
    'notification_frequency   =   3*60;',
    'creamdelegation_url_postfix   =   "/ce-cream/services/gridsite-delegation";',
    'ice_host_cert   =   "${GLITE_HOST_CERT}";',
    'cemon_url_postfix   =   "/ce-monitor/services/CEMonitor";',
    'ice_topic   =   "CREAM_JOBS";',
    'start_proxy_renewer   =   true;',
    'Input   =   "${WMS_LOCATION_VAR}/ice/jobdir";',
    'max_logfile_rotations   =   10;',
    'start_poller   =   true;',
    'poller_delay   =   2*60;',
    'creamdelegation_url_prefix   =   "https://";',
    'purge_jobs   =   false;',
    'start_listener   =   false;',
    'proxy_renewal_frequency   =   600;',
    'bulk_query_size   =   100;',
    'soap_timeout   =   60;',
    'persist_dir   =   "${WMS_LOCATION_VAR}/ice/persist_dir";',
    'log_on_file  =  true;',
    'logfile   =   "${WMS_LOCATION_LOG}/ice.log";',
    'ice_host_key   =   "${GLITE_HOST_KEY}";',
    'max_ice_threads   =   10;',
    'log_on_console  =  false;',
    'cemon_url_prefix   =   "https://";',
    'ice_empty_threshold  =  600;',

]


def main():

    utils = Test_utils.Test_utils(sys.argv[0],"Check glite_wms.conf file")

    tests=["Test 1: Check common section"]
    tests.append("Test 2: Check JobController section")
    tests.append("Test 3: Check NetworkServer section")
    tests.append("Test 4: Check LogMonitor section")
    tests.append("Test 5: Check WorkloadManager section")
    tests.append("Test 6: Check WorkloadManagerProxy section")
    tests.append("Test 7: Check ICE section")
    tests.append("Test 8: Check if attributes match values of yaim variables")
   
    utils.prepare(sys.argv[1:],tests)

    if utils.WMS_USERNAME=='' or utils.WMS_PASSWORD=='':
       utils.warn("Please set the required variables WMS_USERNAME , WMS_PASSWORD in test's configuration file")
       utils.show_progress("Please set the required variables WMS_USERNAME , WMS_PASSWORD in test's configuration file")
       sys.exit(0)

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    fails=[]

    all_tests=utils.is_all_enabled()

    utils.info("Get glite_wms.conf file")

    try:

        logging.info("Get glite_wms.conf file from remote host %s"%(utils.get_WMS()))
         
        ssh=SSH_utils.open_ssh(utils.get_WMS(),utils.WMS_USERNAME,utils.WMS_PASSWORD)

        target='/etc/glite-wms/glite_wms.conf'
        
        SSH_utils.ssh_get_file(ssh,target,"%s/glite_wms.conf_local"%(utils.get_tmp_dir()))

        SSH_utils.close_ssh(ssh)

    except (GeneralError) , e:
        utils.log_error("Unable to get the glite_wms.conf from remote host: %s"%(utils.get_WMS()))
        utils.log_error(e)
        utils.exit_failure("Unable to get the glite_wms.conf from remote host: %s %s %s"%(utils.get_WMS(),utils.WMS_USERNAME,utils.WMS_PASSWORD))

         
    if all_tests==1 or utils.check_test_enabled(1)==1 :
            if check_section(utils,tests[0],"Common",common_attributes):
                fails.append(tests[0])

    if all_tests==1 or utils.check_test_enabled(2)==1 :
            if check_section(utils, tests[1],"JobController",jobcontroller_attributes):
               fails.append(tests[1])
  
    if all_tests==1 or utils.check_test_enabled(3)==1 :
            if check_section(utils, tests[2],"NetworkServer",networkserver_attributes):
                fails.append(tests[2])
                
    if all_tests==1 or utils.check_test_enabled(4)==1 :
            if check_section(utils, tests[3],"LogMonitor",logmonitor_attributes):
                fails.append(tests[3])
    
    if all_tests==1 or utils.check_test_enabled(5)==1 :
            if check_section(utils, tests[4],'WorkloadManager',workloadmanager_attributes):
                fails.append(tests[4])
    
    if all_tests==1 or utils.check_test_enabled(6)==1 :
            if check_section(utils, tests[5],"WorkloadManagerProxy",wmproxy_attributes):
                fails.append(tests[5])
    
    if all_tests==1 or utils.check_test_enabled(7)==1 :
            if check_section(utils, tests[6],"ICE",ice_attributes):
                fails.append(tests[6])

    if utils.YAIM_FILE!='':

       if all_tests==1 or utils.check_test_enabled(8)==1 :
            if check_variables(utils, tests[7]):
                fails.append(tests[7])
    else:
       utils.warn("There is one other test which requires the YAIM_FILE configuration variable. Please set the YAIM_FILE variable in the test's configuration file")
       utils.show_progress("There is one other test which requires the YAIM_FILE configuration variable. Please set the YAIM_FILE variable in the test's configuration file")


    if len(fails) > 0 :
      utils.exit_failure("%s test(s) fail(s): %s"%(len(fails), fails))
    else:
      utils.exit_success()


if __name__ == "__main__":
    main()
