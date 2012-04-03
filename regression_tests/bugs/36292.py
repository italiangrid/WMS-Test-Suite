#
# Bug:36292
# Title: Not all attributes of a SA/SE coul be used in a gangmatching Not implemented
# Link: https://savannah.cern.ch/bugs/?36292
#
#

import logging
import commands

from libutils.Exceptions import *


def run(utils):

    bug='36292'

    logging.info("Start regression test for bug %s"%(bug))

    logging.info("Prepare jdl file")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())

    logging.info("Select SE and get its status")

    closeSEs=utils.run_command_continue_on_error("lcg-infosites --vo %s closeSE"%(utils.VO)).split("\n")

    for line in closeSEs:
        if line.find("Name of the CE:")!=-1 and closeSEs[closeSEs.index(line)+1]!='':
            se=closeSEs[closeSEs.index(line)+1]
            output=commands.getstatusoutput("ldapsearch -x -h %s:2170 -b o=grid | grep GlueSEImplementationVersion"%(se))

            if output[0]==0:
              version=output[1].split(":")[1].strip(" \t\n")
              match_ce=line.split("Name of the CE:")[1].strip(" \t\n")
              logging.info("Selected SE: %s \n Selected CE: %s"%(se,match_ce))
              break

    ce=match_ce.split("/")[0]

    requirements="RegExp(\"%s*\",other.GlueCEUniqueID) && anyMatch(other.storage.CloseSEs,target.GlueSEImplementationVersion == \"%s\")"%(ce,version)

    logging.info("Set requirement expression to jdl file")
    utils.set_requirements(requirements)

    logging.info("Try list match")

    output=utils.run_command_continue_on_error("glite-wms-job-list-match %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    logging.info("Check list match results")

    list_ces=[]

    for line in output.split("\n"):
        if line.find(" - ")!=-1:
            list_ces.append(line.split(" - ")[1].strip(" \t\n"))


    if len(list_ces)!=1:
       logging.error("Test failed, list match returned incorrect number of CEs. Returned: %s , while expected only one"%(len(list_ces)))
       raise GeneralError("","Test failed, list match returned incorrect number of CEs. Returned: %s , while expected only one"%(len(list_ces)))
    elif list_ces[0]!=match_ce:
       logging.error("Test failed, list match returned incorrect CE. Returned: %s , while expected: %s "%(list_ces[0],match_ce))
       raise GeneralError("","Test failed, list match returned incorrect CE. Returned: %s , while expected: %s "%(list_ces[0],match_ce))

     
    logging.info("TEST OK")

    logging.info("End of regression test for bug %s"%(bug))
