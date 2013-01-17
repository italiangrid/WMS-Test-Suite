#
# Bug:74832
# Title: Files specified with absolute paths shouldn't be used with InputSandboxBaseURI
# Link: https://savannah.cern.ch/bugs/?74832
#
#

import logging

from libutils.Exceptions import *


def bug_74832_jdl(utils,jdlfile):

     utils.remove(jdlfile)

     FILE = open(jdlfile,"w")

     FILE.write("Executable = \"/bin/ls\";\n")
     FILE.write("Arguments = \"-la\";\n")
     FILE.write("StdOutput = \"output.out\";\n")
     FILE.write("StdError = \"error.err\";\n")
     FILE.write("RetryCount = 0;\n")
     FILE.write("ShallowRetryCount = 1;\n")
     FILE.write("OutputSandbox={\"output.out\", \"error.err\", \"fstab\", \"grid-mapfile\", \"groupmapfile\", \"passwd\"};\n")
     FILE.write("InputSandbox = { \"/etc/fstab\", \"grid-mapfile\", \"groupmapfile\", \"gsiftp://%s/etc/passwd\"};\n"%(utils.OTHER_HOST))
     FILE.write("InputSandboxBaseURI=\"gsiftp://%s/etc/grid-security/\";\n"%(utils.OTHER_HOST))

     FILE.close()


def run(utils):

    bug='74832'

    logging.info("Start regression test for bug %s"%(bug))

    logging.warning("To verify this bug you have to set the OTHER_HOST attribute for ISB destination at configuration file")

    if utils.OTHER_HOST=='':
       logging.warn("Please set the required variable OTHER_HOST (for ISB destination) in test's configuration file")
       raise GeneralError("Missing required configuration attribute","Please set the required variable OTHER_HOST (for ISB destination) in test's configuration file")


    logging.info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    bug_74832_jdl(utils,utils.get_jdl_file())

    logging.info("Submit the job")

    output=utils.run_command_continue_on_error("glite-wms-job-submit %s --debug --config %s %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Check at debug information if file /etc/fstab has been correctly staged from UI node via gsiftp")
  
    if output.find("Source: /etc/fstab")==-1:
         logging.error("File /etc/fstab hasn't been correctly staged from UI node via gsiftp")
         raise GeneralError("Check for file /etc/fstab","Error !!! File /etc/fstab hasn't been correctly staged from UI node via gsiftp")
    else:
          logging.info("File /etc/fstab has been correctly staged from UI node via gsiftp as expected")


    for line in output.split("\n"):
        if line.find("The JobId is:")!=-1:
            JOBID=line.split("The JobId is:")[1].strip(" \n\t")


    logging.info("Wait until job finishes")

    utils.wait_until_job_finishes(JOBID)

    logging.info("End of regression test for bug %s"%(bug))
