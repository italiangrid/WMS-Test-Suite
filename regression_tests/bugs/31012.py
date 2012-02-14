#
# Bug: 31012
# Title: WMS Client does not print properly WMProxy server version
# Link: https://savannah.cern.ch/bugs/?31012
#
#

import logging

from libutils.Exceptions import *



def run(utils):

    bug='31012'

    ver_lines=[]

    wmproxy_version=''
    get_version=''

    logging.info("Start regression test for bug %s"%(bug))
      
    logging.info("Get WMProxy server version")

    OUTPUT=utils.run_command_continue_on_error("glite-wms-job-submit %s --config %s --debug --version"%(utils.get_delegation_options(),utils.get_config_file()))

    for line in OUTPUT.split("\n"):
        if line.find("Version")!=-1:
            ver_lines.append(line)

    for line in ver_lines:
        if line.find("WMProxy Version:")!=-1:
             wmproxy_version=line.split("WMProxy Version:")[1]
        elif line.find("Version successfully retrieved :")!=-1:
             get_version=line.split("Version successfully retrieved :")[1]

    if len(get_version)>0:

       if wmproxy_version != get_version:
           logging.error("Test failed: the getVersion result and the WMProxy Version mismatch")
           raise GeneralError("","Test failed: the getVersion result and the WMProxy Version mismatch")
    else:
       logging.error("Error !!! Unable to find getVersion result")
       raise GeneralError("","Error !!! Unable to find getVersion result")

    logging.info("End of regression test for bug %s"%(bug))