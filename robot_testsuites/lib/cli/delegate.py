import commands
import time

from Exceptions import *

def test_delegate(utils,options,more_options=""):

    if len(more_options)>0:
        exec_str="%s %s"%(options,more_options)
    else:
        exec_str=options
  
    utils.log_info('Execute command: glite-wms-job-delegate-proxy %s'%(exec_str))

    OUTPUT=commands.getstatusoutput("glite-wms-job-delegate-proxy %s"%(exec_str))
             
    if OUTPUT[0]!=0:
          utils.log_info('Command glite-wms-job-delegate-proxy failed. Failure message: %s'%(OUTPUT[1]))
          raise RunCommandError('','Command glite-wms-job-delegate-proxy failed. Check log file for details')
 
    utils.log_info('Command output:\n%s'%(OUTPUT[1]),'DEBUG')
       
    return OUTPUT[1]

def export_delegation_id(utils,input):

    delegationid=''

    utils.log_info("Export delagation identifier from glite-wms-job-delegate-proxy output")
   
    for line in input.split("\n"):
       if line.find("with the delegation identifier:")!=-1:
           delegationid=line.split("with the delegation identifier:")[1]
           delegationid=delegationid.strip(" \t\n")
           break

    if len(delegationid)==0:
      utils.log_info(" == ERROR == Unable to export delegation identifier")
      raise GeneralError("","Unable to export delegation identifier from glite-wms-job-delegate-proxy output.")
    else:
      utils.log_info("Delegation id is: %s"%(delegationid))

    return delegationid

def export_deleg_endpoint(input):

    endpoint=''
    lines=input.split("\n")
    for line in lines:
        if line.find("Your proxy has been successfully delegated to the WMProxy(s)")!=-1:
           value=lines[lines.index(line)+1]
           endpoint=value.strip(" \n\t")
           break
                       
    return endpoint


def check_delegation(utils,delegationid):

    utils.log_info("Check if delegation %s exists , try a submit and finally cancel the unused job"%(delegationid))

    utils.log_info("Verify the delegation")

    utils.run_command("glite-wms-job-info -d %s --config %s"%(delegationid,utils.get_config_file()))

    utils.log_info("Try a submit")

    JOBID=utils.run_command("glite-wms-job-submit -d %s --config %s --nomsg %s"%(delegationid,utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info ("Cancel the unused job")
    utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))


def check_time_left(utils,input):
 
    timeleft=''

    for line in input.split("\n"):
       if line.find("Timeleft")!=-1:
           timeleft=line.split(" : ")[1].strip(" \t\n")
           break
    
    values=timeleft.split(" ")

    if int(values[0])>10 or values[1]!='min':
       utils.log_info("== ERROR == Wrong timeleft delegating proxy")
       raise GeneralError("","Wrong timeleft delegating proxy")
    else:
        utils.log_info("Check OK")
           

