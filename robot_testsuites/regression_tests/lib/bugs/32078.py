#
# Bug:32078
# Title: Problem with GangMatching statement involving GlueSEStatus
# Link: https://savannah.cern.ch/bugs/?32078
#
#

import commands

from lib.Exceptions import *


def run(utils):

    bug='32078'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Prepare jdl file")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_utils_jdl()
    utils.set_jdl(utils.get_jdl_file())

    utils.log_info("Select SE and get its status")

    closeSEs=utils.run_command("lcg-infosites --vo %s closeSE"%(utils.VO)).split("\n")

    for line in closeSEs:
        if line.find("Name of the CE:")!=-1 and closeSEs[closeSEs.index(line)+1]!='':
            se=closeSEs[closeSEs.index(line)+1]
            output=commands.getstatusoutput("ldapsearch -x -h %s:2170 -b o=grid | grep GlueSEStatus"%(se))

            if output[0]==0:
              status=output[1].split(":")[1].strip(" \t\n")
              match_ce=line.split("Name of the CE:")[1].strip(" \t\n")
              utils.log_info("Selected SE: %s \n Selected CE: %s"%(se,match_ce))
              break

    ce=match_ce.split("/")[0]

    requirements="RegExp(\"%s*\",other.GlueCEUniqueID) && anyMatch(other.storage.CloseSEs,target.GlueSEStatus == \"%s\")"%(ce,status)

    utils.log_info("Set requirement expression to jdl file")
    utils.set_requirements(requirements)

    utils.log_info("Try list match")

    output=utils.run_command("glite-wms-job-list-match %s --config %s %s"%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Check list match results")

    list_ces=[]

    for line in output.split("\n"):
        if line.find(" - ")!=-1:
            list_ces.append(line.split(" - ")[1].strip(" \t\n"))


    if len(list_ces)!=1:
       utils.log_info("ERROR: Test failed, list match returned incorrect number of CEs. Returned: %s , while expected only one"%(len(list_ces)))
       raise GeneralError("","Test failed, list match returned incorrect number of CEs. Returned: %s , while expected only one"%(len(list_ces)))
    elif list_ces[0]!=match_ce:
       utils.log_info("ERROR: Test failed, list match returned incorrect CE. Returned: %s , while expected: %s "%(list_ces[0],match_ce))
       raise GeneralError("","Test failed, list match returned incorrect CE. Returned: %s , while expected: %s "%(list_ces[0],match_ce))

     
    utils.log_info("TEST OK")

    utils.log_info("End of regression test for bug %s"%(bug))
