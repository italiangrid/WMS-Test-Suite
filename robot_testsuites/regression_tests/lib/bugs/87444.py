#
# Bug: 87444
# Title: glite-wms-job-list-match --help show an un-implemented (and useless) option --default-jdl
# Link: https://savannah.cern.ch/bugs/?87444
#
#

import commands

from lib.Exceptions import *

def run(utils):

    bug='87444'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Check if useless option --default-jdl has been removed from glite-wms-job-list-match help message")

    output=commands.getstatusoutput("glite-wms-job-list-match --help")

    if output[1].find("--default-jdl")==-1:
         utils.log_info("Test OK")
    else:
         utils.log_info("ERROR: Found useless option --default-jdl")
         raise GeneralError("Check glite-wms-job-list-match help message","Found useless option --default-jdl")

    utils.log_info("End of regression test for bug %s"%(bug))
