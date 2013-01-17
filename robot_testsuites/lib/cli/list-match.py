import commands

from Exceptions import *

def test_list_match(utils,options,jdl_file=""):

    if len(jdl_file)>0:
        exec_str="%s %s"%(options,jdl_file)
    else:
        exec_str=options 
  
    utils.log_info('Execute command: glite-wms-job-list-match %s'%(exec_str))

    OUTPUT=commands.getstatusoutput("glite-wms-job-list-match %s"%(exec_str))
             
    if OUTPUT[0]!=0:
          utils.log_info('Command glite-wms-job-list-match failed. Failure message: %s'%(OUTPUT[1]))
          raise RunCommandError('','Command glite-wms-job-list-match failed. Check log file for details')
 
    utils.log_info('Command output:\n%s'%(OUTPUT[1]),'DEBUG')
       
    return OUTPUT[1]

