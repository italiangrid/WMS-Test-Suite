#
# Bug: 31012
# Title: WMS Client does not print properly WMProxy server version
# Link: https://savannah.cern.ch/bugs/?31012
#
#


from lib.Exceptions import *


def run(utils):

    bug='31012'

    ver_lines=[]

    wmproxy_version=''
    get_version=''

    utils.log_info("Start regression test for bug %s"%(bug))
      
    utils.log_info("Get WMProxy server version")

    OUTPUT=utils.run_command("glite-wms-job-submit %s --config %s --debug --version"%(utils.get_delegation_options(),utils.get_config_file()))

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
           utils.log_info("ERROR: Test failed - the getVersion result and the WMProxy Version mismatch")
           raise GeneralError("","Test failed: the getVersion result and the WMProxy Version mismatch")
    else:
       utils.log_info("ERROR: Unable to find getVersion result")
       raise GeneralError("","Error !!! Unable to find getVersion result")

    utils.log_info("End of regression test for bug %s"%(bug))
