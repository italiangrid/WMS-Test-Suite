#
# Bug: 85799
# Title: pkg-config info for wmproxy-api-cpp should be enriched
# Link: https://savannah.cern.ch/bugs/?85799
#
#

from lib.Exceptions import *


def run(utils):

    bug='85799'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Get wmproxy-api-cpp.pc file")

    result=utils.run_command("rpm -ql glite-wms-wmproxy-api-cpp")

    config_file=''

    for line in result.split("\n"):

        if line.find("wmproxy-api-cpp.pc")!=-1:
            config_file=line
            break

    if len(config_file)==0:
        utils.log_info("ERROR: Unable to find wmproxy-api-cpp.pc file")
        raise GeneralError("Get wmproxy-api-cpp.pc file","Unable to find wmproxy-api-cpp.pc file")
    
    FILE=open(config_file)
    file_data=' '.join(FILE.readlines())
    FILE.close()

    error=[]

    utils.log_info("Check if wmproxy-api-cpp.pc contants all the required information")

    attributes=['Requires: emi-gridsite-openssl' , 'Libs: -L${libdir} -lglite_wms_wmproxy_api_cpp' ,'Cflags: -I${includedir}']
    
    for attribute in attributes:

        utils.log_info("Check for: %s"%(attribute))

        if file_data.find(attribute)==-1:
            utils.log_info("ERROR: Unable to find: %s"%(attribute))
            error.append(attribute)


    if len(error)==0:
        utils.log_info("Test OK")
    else:
      utils.log_info("ERROR: Unable to find all the required info. Missing: %s"%(' '.join(error)))
      raise GeneralError("Check if wmproxy-api-cpp.pc contants all the required information","Unable to find all the required info. Missing: %s"%(' '.join(error)))

    
    utils.log_info("End of regression test for bug %s"%(bug))

