import commands
import time

from Exceptions import *

def test_perusal(utils,options,jobid=''):

    if len(jobid)>0:
        exec_str="%s %s"%(options,jobid)
    else:
        exec_str=options 
  
    utils.log_info('Execute command: glite-wms-job-perusal %s'%(exec_str))

    OUTPUT=commands.getstatusoutput("glite-wms-job-perusal %s"%(exec_str))
             
    if OUTPUT[0]!=0:
          utils.log_info('Command glite-wms-job-perusal failed. Failure message: %s'%(OUTPUT[1]))
          raise RunCommandError('','Command glite-wms-job-perusal failed. Check log file for details')
 
    utils.log_info('Command output:\n%s'%(OUTPUT[1]),'DEBUG')
       
    return OUTPUT[1]



                    
