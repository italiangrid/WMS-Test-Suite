
from Exceptions import *

def execute_delegation(utils,delegationid=''):

  if len(delegationid)==0:
     cmd="glite-wms-job-delegate-proxy --config %s --autm-delegation"%(utils.get_config_file())  
  else:
     cmd="glite-wms-job-delegate-proxy --config %s --delegationid %s"%(utils.get_config_file(),delegationid)  

  output=utils.run_command(cmd)

  return output


def get_delegationid(utils,data):
 
   delegationid=''

   for line in data.split("\n"):
       if line.find("with the delegation identifier")!=-1:
            delegationid=line.split(":")[1].strip(" \t\n")
            break

   utils.log_info("Delegation Id: %s"%(delegationid))

   return delegationid


#check if delegation exists and try a submit
def check_delegation(utils,delegationid):

   utils.log_info("Verify the delegation")

   utils.run_command("glite-wms-job-info -d %s --config %s"%(delegationid,utils.get_config_file()))

   utils.log_info("Try a submit")

   JOBID=utils.run_command("glite-wms-job-submit -d %s --config %s --nomsg %s"%(delegationid,utils.get_config_file(),utils.get_jdl_file()))

   utils.log_info("Cancel the unused job")

   utils.run_command("glite-wms-job-cancel --noint %s"%(JOBID))
   

def check_time_left(utils,data):
 
   text="NotFound"

   for line in data.split("\n"):
      if line.find("Timeleft")!=-1:
        utils.log_info(line)
        text=(line.split(":")[1]).split(" ")[2]
        value=(line.split(":")[1]).split(" ")[1]
        utils.log_info("Delegation is valid for at most '%s' '%s'"%(value,text))
        break
      
   if text!='min' or int(value)>10:
      utils.log_info("ERROR: Wrong timeleft delegating proxy")
      raise GeneralError("","Wrong timeleft delegating proxy")

