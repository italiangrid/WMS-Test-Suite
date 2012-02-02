#! /usr/bin/python

import sys
import signal
import os
import commands
import traceback

from Exceptions import *

import Test_utils

COMMAND="glite-wms-job-list-match"

### REMEMBER to reset jdl at the begining of every test


def test1(utils, title):

    # test if command exists
    utils.show_progress(title)

    try:
        utils.info(title)
        utils.run_command_continue_on_error("which %s"%(COMMAND))

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    utils.info("TEST PASS.")
    return 0


def test2(utils, title):

    # Test a simple matching
    utils.show_progress(title)

    try:

        utils.set_jdl(utils.JDLFILE)
        utils.info(title)
        output=utils.run_command_continue_on_error("%s %s --rank --noint --config %s %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
        utils.info ("Check if some CEs match")
        if output.find("No Computing Element matching your job requirements has been found!") != -1:
            utils.error("TEST FAILS: no one CE matches!")
            return 1 # test fails
        else:
            utils.info("TEST PASS.")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0


def test3(utils, title):


    # Test delegation proxy option --delegationid
    utils.show_progress(title)

    try:
        utils.set_jdl(utils.JDLFILE)
        utils.info(title)
        # Create delegate proxy
        Delegation="DelegationTest"
        utils.info("Set Delegation Id to %s"%(Delegation))
        utils.run_command_continue_on_error("glite-wms-job-delegate-proxy -c %s -d %s"%(utils.get_config_file(),Delegation))
        output=utils.run_command_continue_on_error ("%s --rank --noint --delegationid %s --config %s %s"%(COMMAND,Delegation,utils.get_config_file(),utils.get_jdl_file()))
        utils.info ("Check if some CEs match")
        if output.find("No Computing Element matching your job requirements has been found!") != -1:
            utils.error("TEST FAILS: no one CE matches!")
            return 1 # test fails    
        else:
            utils.info("TEST PASS.")             

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0


def test4(utils, title):

    # Test a restricted matching. Success if the select CE does not match.
    utils.show_progress(title)

    try:
        utils.set_jdl(utils.JDLFILE)
        utils.info(title)
        utils.dbg("Look for a matching CE")
        output=utils.run_command_continue_on_error("%s %s --config %s --noint %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
        for lines in output.splitlines():
            if lines.find(" - ") == 0:
                match=lines[4:]
                break
        utils.dbg("CE %s matches"%(match))
        utils.set_requirements ("!regexp(\"%s\", other.GlueCEUniqueID)"%(match))
        output=utils.run_command_continue_on_error("%s %s --config %s --noint %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
        utils.info ("Look for the selected CE in the command output")
#        If only one CE matches the test returns a false error message !
#        if output.find("No Computing Element matching your job requirements has been found!") != -1:
#            utils.error("TEST FAILS: no one CE matches!")
#            return 1 # test fails 
        if output.find(match) != -1:
            utils.error("TEST FAILS: found the excluded CE")        
            return 1 # test fails 
        else:
            utils.info("TEST PASS.")  
            

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0
   

def test5(utils, title):

    # Test a failure matching (requirements = false). Success if no matching is found.
    utils.show_progress(title)

    try:
        utils.set_jdl(utils.JDLFILE)
        utils.info(title)
        utils.set_requirements ("false")
        output=utils.run_command_continue_on_error("%s %s --config %s --noint %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))
        utils.info ("Check if no one CEs match")
        if output.find("No Computing Element matching your job requirements has been found!") == -1:
            utils.error("TEST FAILS: some CEs match!")
            return 1 # test fails         
        else:
            utils.info("TEST PASS.")        

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0


def test6(utils, title):

    # Test a matching with attribute EnableWMSFeedback true. Success if match only CREAM CEs
    utils.show_progress(title)

    try:
        utils.set_jdl(utils.JDLFILE)
        matched_ces=[]
        cream_counter=0

        utils.info(title)
        utils.info("Set EnableWMSFeedback=true; in jdl file")

        utils.add_jdl_general_attribute("EnableWMSFeedback","true")

        output=utils.run_command_continue_on_error("%s %s --config %s --noint %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file())).split("\n")

        utils.info ("Check the matching CEs")

        for line in output:

            if line.find(" - ")!=-1:
                   ce=line.split(" - ")[1].strip("\n")
                   
                   if ce.find("/cream-")!=-1:
                       cream_counter=cream_counter+1
                 
                   matched_ces.append(ce)

        if len(matched_ces)!=cream_counter:
             utils.error("TEST FAILS: Matching CEs are not only CREAM CEs")
             return 1
        else:
             utils.info("Check OK, matched only CREAM CEs")
             utils.info("TEST PASS.")
        

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0


### Test not completely implemented An as hoc JDL is needed for
### data matchmaking test
def test7(utils, title):
    
    # Test matching with data requirements
    utils.show_progress(title)

    try:

        utils.info(title)

        utils.info("Find an lfc for the %s VO"%(utils.VO))

        output=utils.run_command_continue_on_error("lcg-infosites -v 1 --vo %s lfc"%(utils.VO)).split("\n")

        if len(output)==0:
            utils.error("Unable to find an lfc for the %s VO"%(utils.VO))
            return 1

        lfc=output[0]

        utils.info("Find an SE for the %s VO"%(utils.VO))

        SEs=utils.run_command_continue_on_error("lcg-infosites -v 1 --vo %s se"%(utils.VO)).split("\n")

        if len(SEs)==0:
            utils.error("Unable to find an se for the %s VO"%(utils.VO))
            return 1

        utils.info("Set the lfc host")

        os.environ['LFC_HOST']=lfc

        dir="/grid/%s/%s"%(utils.VO,utils.ID)

        utils.info("Create the directory %s"%(dir))

        utils.run_command_continue_on_error("lfc-mkdir %s"%(dir))

        utils.info("Create the files file1.txt and file2.txt")

        usedSE=[]

        for se in SEs:

          res=commands.getstatusoutput("lcg-cr --vo %s -d %s -l lfn:%s/file1.txt file://%s/file1.txt"%(utils.VO,se,dir,os.getcwd()))

          if res[0]==0:
            res=commands.getstatusoutput("lcg-cr --vo %s -d %s -l lfn:%s/file2.txt file://%s/file2.txt"%(utils.VO,se,dir,os.getcwd()))
            usedSE.append(se)
            break

        utils.set_data_req_jdl(utils.JDLFILE,utils.VO,lfc,dir)

        output=utils.run_command_continue_on_error("%s %s --config %s %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file())).split("\n")

        matched_ces=[]

        for line in output:

            if line.find(" - ")!=-1:
                 ce=line.split(" - ")[1].strip("\n")
                 matched_ces.append(ce)

        if len(matched_ces)==0:
            utils.error("Unable to find any CEs mathing the job requirements")
            return 1

        utils.info ("Check if the matched CEs are close to the SE %s"%(usedSE[0]))

        output=utils.run_command_continue_on_error("lcg-infosites --vo %s closeSE"%(utils.VO)).split("\n")

        for target in matched_ces:

           utils.info("Check for CE %s"%(target))

           for line in output:

             if line.find(target)!=-1:
                 inx=output.index(line)
                 qix=output[inx+1:]
                 break

           ses=[]

           for line in qix:

              if len(line)==0:
                 break

              ses.append(line.strip(' \t\n'))


           if len(set(ses)&set(usedSE))!=1:
              utils.error("Matched CE %s is not close to the SE %s"%(target,usedSE[0]))
              return 1

        utils.info("TEST PASS.")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0

    
def test8(utils, title):

    #Gangmathing Test
    utils.show_progress(title)

    try:

        utils.set_gang_jdl(utils.JDLFILE)
        utils.set_requirements("CErequirements && SErequirements");
        utils.info(title)

        output=utils.run_command_continue_on_error("%s %s --config %s %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file())).split("\n")

        utils.info ("Check if some CEs really meet the constraints")

        matched_ces=[]

        for line in output:

            if line.find(" - ")!=-1:
                 ce=line.split(" - ")[1].strip("\n")
                 matched_ces.append(ce)

        for ce in matched_ces:

            result=utils.run_command_continue_on_error("ldapsearch -x -h %s:2170 -b \"Mds-Vo-name=resource,o=grid\"  GlueSALocalID=%s"%(ce.split(":")[0],utils.VO)).split("\n")

            utils.info("Check the GlueSAStateAvailableSpace attribute for CE %s"%(ce))

            value=0
        
            for line in result:
                if line.find("GlueSAStateAvailableSpace")!=-1:
                   value=line.split(":")[1].strip(" \n\t")

            if int(value)<20:
                utils.error("GlueSAStateAvailableSpace for matched CE %s is %s while expected at least 20"%(ce,value));
                return 1


            utils.info("Check the GlueCEStateStatus and GlueCEInfoTotalCPUs attributes for CE %s"%(ce))

            result=utils.run_command_continue_on_error("ldapsearch -x -h %s:2170 -b GlueCEUniqueID=%s,Mds-Vo-name=resource,o=grid"%(ce.split(":")[0],ce)).split("\n")

            value=0
            status=""

            for line in result:

                if line.find("GlueCEInfoTotalCPUs")!=-1:
                   value=line.split(":")[1].strip(" \n\t")

                if line.find("GlueCEStateStatus")!=-1:
                   status=line.split(":")[1].strip(" \n\t")

            if int(value)<2:
               utils.error("GlueCEInfoTotalCPUs for matched CE %s is %s while expected at least 2"%(ce,value));
               return 1

            if status!='Production':
               utils.error("GlueCEStateStatus for matched CE %s is %s while expected 'Production'"%(ce,status));
               return 1

            utils.info("Everything ok with mathced CE: %s"%(ce))


        utils.info ("Now try listmatch with only CE Requirements")

        utils.set_gang_jdl(utils.JDLFILE)
        utils.set_requirements("CErequirements");

        output=utils.run_command_continue_on_error("%s %s --config %s %s"%(COMMAND,utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file())).split("\n")

        matched2_ces=[]

        for line in output:

            if line.find(" - ")!=-1:
                 ce=line.split(" - ")[1].strip("\n")
                 matched2_ces.append(ce)

    
        utils.info ("Check the number of the matched CEs")

        if len(matched_ces)>len(matched2_ces):
            utils.error("TEST FAILS: Gangmatch listmatch return more CEs than the simple list-match")
            return 1 # test fails
        
        utils.info("TEST PASS.")

    except (RunCommandError,GeneralError,TimeOutError) , e :
        utils.log_error("%s"%(utils.get_current_test()))
        utils.log_error("Command: %s"%(e.expression))
        utils.log_error("Message: %s"%(e.message))
        utils.log_traceback("%s"%(utils.get_current_test()))
        utils.log_traceback(traceback.format_exc())
        return 1

    return 0




def main():

    fails=[]
    
    tests=["Test 1: check if %s command exists"%(COMMAND)]
    tests.append("Test 2: test a simple matching")
    tests.append("Test 3: check --delegationid option")
    tests.append("Test 4: exclude a CE from the match")
    tests.append("Test 5: try a failure matching (Requirements == false)")
    tests.append("Test 6: try a matching with EnableWMSFeedback attribute true")
    tests.append("Test 7: try a matching with data requirements")
    tests.append("Test 8: try a gang-matching")

    utils = Test_utils.Test_utils(sys.argv[0],"WMS Job ListMatch Testing")

    utils.prepare(sys.argv[1:],tests)

    utils.info("WMS Job ListMatch Testing")

    signal.signal(signal.SIGINT,utils.exit_interrupt)

    all_tests=utils.is_all_enabled()

    if all_tests==1 or utils.check_test_enabled(1)==1 :
        if test1(utils, tests[0]):
            fails.append(tests[0])
                
    if all_tests==1 or utils.check_test_enabled(2)==1 :
        if test2(utils, tests[1]):
            fails.append(tests[1])
                
    if all_tests==1 or utils.check_test_enabled(3)==1 :
        if test3(utils, tests[2]):
            fails.append(tests[2])
                
    if all_tests==1 or utils.check_test_enabled(4)==1 :
        if test4(utils, tests[3]):
            fails.append(tests[3])   

    if all_tests==1 or utils.check_test_enabled(5)==1 :
        if test5(utils, tests[4]):
            fails.append(tests[4])

    if all_tests==1 or utils.check_test_enabled(6)==1 :
        if test6(utils,tests[5]):
            fails.append(tests[5])

    if all_tests==1 or utils.check_test_enabled(7)==1 :
        if test7(utils,tests[6]):
            fails.append(tests[6])

    if all_tests==1 or utils.check_test_enabled(8)==1 :
        if test8(utils,tests[7]):
            fails.append(tests[7])



    if len(fails) > 0 :
      utils.exit_failure("%s test(s) fail(s): %s"%(len(fails), fails))
    else:
      utils.exit_success()


if __name__ == "__main__":
    main()
