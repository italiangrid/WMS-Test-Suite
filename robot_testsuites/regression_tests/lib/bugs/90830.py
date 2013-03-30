#
# Bug: 90830
# Title: ICE should use env vars in its configuration
# Link: https://savannah.cern.ch/bugs/?90830
#
#

from lib.Exceptions import *

def get_ice_attributes(file):

    target_attributes = ['ice_host_cert','Input','persist_dir','logfile','ice_host_key']

    #Read contents from file
    FILE=open(file,"r")
    lines=FILE.readlines()
    FILE.close()

    row_start=0
    row_end=0

    attributes=[]

    for line in lines:
      if line.find("ICE = ")!=-1:
          row_start=lines.index(line)+1
          break

    lines=lines[row_start:]

    for line in lines:
      if line.find("    ];")!=-1:
          row_end=lines.index(line)

    for line in lines[:row_end]:

        value=[line[:-1].lstrip().split("=")[0].strip(' \t\n\r')]

        z=set(target_attributes)&set(value)

        if(len(z))==1:
          attributes.append(line[:-1].lstrip())

    return attributes



def run(utils):

    bug='90830'

    ice_attributes = [
       'ice_host_cert   =   "${GLITE_HOST_CERT};',
       'Input   =   "${WMS_LOCATION_VAR}/ice/jobdir";',
       'persist_dir   =   "${WMS_LOCATION_VAR}/ice/persist_dir";',
       'logfile   =   "${WMS_LOCATION_LOG}/ice.log";',
       'ice_host_key   =   "${GLITE_HOST_KEY};'
    ]

    utils.log_info("Start regression test for bug %s"%(bug))

    if len(utils.get_Username())==0 or len(utils.get_Password())==0:
        utils.log_info("ERROR: To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")
        raise GeneralError("","To verify this bug you need access to WMS. You have set WMS_USERNAME and WMS_PASSOWRD attributes at configuration file")

    utils.log_info("Get glite_wms.conf file from remote host %s"%(utils.get_WMS()))

    ssh=utils.open_ssh(utils.get_WMS(),utils.WMS_USERNAME,utils.WMS_PASSWORD)

    target='/etc/glite-wms/glite_wms.conf'

    utils.ssh_get_file(ssh,target,"%s/glite_wms.conf_local"%(utils.get_tmp_dir()))

    utils.close_ssh(ssh)

    attributes=get_ice_attributes("%s/glite_wms.conf_local"%(utils.get_tmp_dir()))

    z=set(attributes)^set(ice_attributes)

    if(len(z)>0):
        utils.log_info("ERROR: Problem with the following attributes in the ICE section: %s"%(z))
        raise GeneralError("Check if variables in the ICE section of the wms configuarion file use environment variables","Problem with the following attributes in the ICE section:%s"%(z))

    utils.log_info("Test OK")

    utils.log_info("End of regression test for bug %s"%(bug))
