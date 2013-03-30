#
# Bug:58878
# Title: Request for a feature allowing propagation of generic parameters from JDL to LRMS
# Link: https://savannah.cern.ch/bugs/?58878
#
#


from lib.Exceptions import *
from lib import Job_utils


def run(utils):

    bug='58878'

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    ssh=utils.open_ssh(utils.get_WMS(),utils.get_Username(),utils.get_Password())

    utils.log_info("CASE 1 : Use LCG-CE")

    utils.log_info("Insert into the Workload Management section of glite_wms.conf the PropagageToLRMS section")

    value="{\n [ name = \"smpgranularity\"; value = jdl.SMPGranularity ],\n[ name = \"wholenodes\"; value = jdl.WholeNodes ; requires = jdl.WholeNodes == true; ],\n[ name = \"hostsmpsize\"; value = ce.GlueHostArchitectureSMPSize ],\n[ name = \"mpi_type\"; value = jdl.MpiType; requires = ce.GlueCEInfoLRMSType == \"lsf\"; ],\n[ name = \"hostmainmem\"; value = ce.GlueHostMainMemoryRAMSize; requires = ce.GlueCEInfoLRMSType == \"pbs\"; ]\n}"

    utils.add_attribute_to_remote_file(ssh,"/etc/glite-wms/glite_wms.conf","WorkloadManager",['PropagateToLRMS'],[value])

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())

    smp_granularity=2
    mpi_type="mvapich_gcc4"

    utils.log_info("Append the jdl file with the required attributes")
    utils.add_jdl_general_attribute(utils.get_jdl_file(),"SMPGranularity",smp_granularity)
    utils.add_jdl_attribute(utils.get_jdl_file(),"MpiType",mpi_type)
    utils.set_destination_ce(utils.get_jdl_file(),"2119/jobmanager")

    utils.log_info("Submit the job to LCG-CE and wait to finish")

    JOBID=Job_utils.submit_wait_finish(utils,"2119/jobmanager")

    utils.log_info("Check job status")

    output=utils.run_command("glite-wms-job-logging-info -v 3 --event Enqueued %s"%(JOBID))

    for line in output.split("\n"):
        if line.find("GlobusRSL")!=-1:
            arguments=line.split("arguments=")[1][1:-5]
            break

    output=utils.run_command("glite-wms-job-status %s"%(JOBID)).split("\n")

    for line in output:
        if line.find("Destination:")!=-1:
            line=line.split("Destination:")[1]
            CE=line.split(":2119")[0].strip(" \t\n")

    lrms_type=utils.run_command("ldapsearch -x -h %s:2170 -b o=grid | grep GlueCEInfoLRMSType"%(CE))
    lrms_type=lrms_type.split(":")[1].strip(" \t\n")

    smp_size=utils.run_command("ldapsearch -x -h %s:2170 -b o=grid | grep GlueHostArchitectureSMPSize"%(CE))
    smp_size=smp_size.split(":")[1].strip(" \t\n")

    host_mem=utils.run_command("ldapsearch -x -h %s:2170 -b o=grid | grep GlueHostMainMemoryRAMSize"%(CE))
    host_mem=host_mem.split(":")[1].strip(" \t\n")

    arguments=arguments.split(",")

    target=['smpgranularity=%s'%(smp_granularity),'hostsmpsize=%s'%(smp_size)]

    if lrms_type=="pbs":
        target.append("hostmainmem=%s"%(host_mem))
    elif lrms_type=="lsf":
        target.append("mpi_type=%s"%(mpi_type))


    z=set(target)&set(arguments)

    if len(z)!=len(target):
       utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
       utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
       ssh.close()
       utils.log_info("ERROR: Unable to find all the expected attributes. \n Passed: %s \n Expected: %s"%(arguments,target))
       raise GeneralError("","Unable to find all the expected attributes. \n Passed: %s \n Expected: %s"%(arguments,target))
    else:
       utils.log_info("CASE 1 OK.\n Passed: %s \nExpected: %s"%(arguments,target))
    
    utils.log_info("CASE 2 : Use CREAM CE")

    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())

    smp_granularity=1
    mpi_type="mvapich_gcc4"

    utils.log_info("Append the jdl file with the required attributes")
    utils.add_jdl_general_attribute(utils.get_jdl_file(),"SMPGranularity",smp_granularity)
    utils.add_jdl_attribute(utils.get_jdl_file(),"MpiType",mpi_type)
    utils.set_destination_ce(utils.get_jdl_file(),"/cream-")

    utils.log_info("Submit the job to CREAM CE and wait to finish")

    JOBID=Job_utils.submit_wait_finish(utils,"/cream-")

    utils.log_info("Check job status")

    output=utils.run_command("glite-wms-job-logging-info -v 3 --event Transfer %s"%(JOBID))


    for line in output.split("\n"):
        if line.find("CeRequirements")!=-1:
            arguments=line.split("CeRequirements = ")[1]
            arguments=arguments.split(") )&&")[1][:-3]
            break

    
    output=utils.run_command("glite-wms-job-status %s"%(JOBID)).split("\n")

    for line in output:
        if line.find("Destination:")!=-1:
            line=line.split("Destination:")[1]
            CE=line.split(":8443")[0].strip(" \t\n")

    lrms_type=utils.run_command("ldapsearch -x -h %s:2170 -b o=grid | grep GlueCEInfoLRMSType"%(CE))
    lrms_type=lrms_type.split(":")[1].strip(" \t\n")

    smp_size=utils.run_command("ldapsearch -x -h %s:2170 -b o=grid | grep GlueHostArchitectureSMPSize"%(CE))
    smp_size=smp_size.split(":")[1].strip(" \t\n")

    host_mem=utils.run_command("ldapsearch -x -h %s:2170 -b o=grid | grep GlueHostMainMemoryRAMSize"%(CE))
    host_mem=host_mem.split(":")[1].strip(" \t\n")

    arguments=arguments.split("&&")

    target=['smpgranularity==%s'%(smp_granularity),'hostsmpsize==%s'%(smp_size)]

    if lrms_type=="pbs":
        target.append("hostmainmem==%s"%(host_mem))
    elif lrms_type=="lsf":
        target.append("mpi_type==%s"%(mpi_type))


    z=set(target)&set(arguments)

    if len(z)!=len(target):
       utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")
       utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")
       ssh.close()
       utils.log_info("ERROR: Unable to find all the expected attributes. \n Passed: %s \n Expected: %s"%(arguments,target))
       raise GeneralError("","Unable to find all the expected attributes. \n Passed: %s \n Expected: %s"%(arguments,target))
    else:
       utils.log_info("CASE 2 OK.\n Passed: %s \nExpected: %s"%(arguments,target))

    utils.log_info("TEST OK")

    utils.log_info("Restore the initial glite_wms.conf file")

    utils.execute_remote_cmd(ssh, "cp -f /etc/glite-wms/glite_wms.conf.bak /etc/glite-wms/glite_wms.conf")

    utils.execute_remote_cmd(ssh,"/etc/init.d/glite-wms-wm restart")

    ssh.close()

    utils.log_info("End of regression test for bug %s"%(bug))
    
    
