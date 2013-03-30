import os.path
import getopt
import os
import sys
import time
import commands
import getpass
import string
import sqlite
import paramiko
import socket

import logging
import traceback

from Exceptions import *
from time import strftime


class Regression_utils:

    def __init__(self,cmd):

        self.CMD=cmd
        self.NUM_STATUS_RETRIEVALS=120
        self.SLEEP_TIME=30
        self.DELEGATION_OPTIONS="-a"
        self.DEFAULTREQ="other.GlueCEStateStatus == \"Production\""
        self.ID=''
        self.CONF="wms.conf"
        self.VERBOSE=0
        self.LOG=0
        self.WMS=''
        self.VO=''
        self.LB=''
        self.TESTLOGFILE=''
        self.START_TIME=''
        self.MYTMPDIR=''
        self.JOB_OUTPUT_DIR=''
        self.LOGFILE=''
        self.OUTPUTFILE=''
        self.PROXY=''
        self.TMPFILE=''
        self.JDLFILE=''
        self.CONFIG_FILE=''
        self.JOBSTATUS=''
        self.LOG_LEVEL=''
        self.MYPROXYSERVER=''
        self.INPUT_TEST_FILE=''
        self.ALL=0
        self.CURRENTTEST=''
        self.fails=[]
        self.WMS_USERNAME=''
        self.WMS_PASSWORD=''
        self.PROXY_PASSWORD=''
        self.YAIM_FILE=''
        self.ROLE=''
        self.USERNAME=''
        self.PASSWORD=''
        self.OTHER_HOST=''

    def usage(self,msg):

        print '\nUsage: '
        print ''
        print '%s -a | -b <#bug> | -i <file> [-s] [-h] [-l] [-d <level>] [-c <conf>]'%(msg)
        print ''
        print " -b <#bug>        execute the regression test for given #bug"
        print " -a               execute all available regression tests"
        print " -i <file>        execute only the regression tests that are listed to file"
        print " -h               this help"
        print " -s               show all the available tests"
        print " -l               save output in a file"
        print " -d <level >      print verbose messages (level = (1|2|3)"
        print " -c <conf>        configuration file"
        print ""



    def get_delegation_options(self):
        return self.DELEGATION_OPTIONS

    def get_config_file(self):
        return self.CONFIG_FILE

    def get_output_file(self):
        return self.OUTPUTFILE

    def get_tmp_file(self):
        return self.TMPFILE

    def get_tmp_dir(self):
        return self.MYTMPDIR

    def get_jdl_file(self):
        return self.JDLFILE

    def get_job_status(self):
        return self.JOBSTATUS

    def get_WMS(self):
        return self.WMS

    def get_MYPROXY_SERVER(self):
        return self.MYPROXYSERVER
    
    def get_log_file(self):
        return self.LOGFILE

    def get_job_output_dir(self):
        return self.JOB_OUTPUT_DIR

    def get_current_test(self):
        return self.CURRENTTEST

    def get_fails_number(self):
        return len(self.fails)

    def get_fails_test(self):
        return self.fails
        
    def get_jdl_name(self):
        return self.JDLFILE

    
    # Extract the destination CE of the job given as input ($1 must be a valid JOBID)
    # return CENAME
    def get_CE(self,jobid):

        CENAME="Destination not available"

        logging.info("Extract the destination CE of the job %s",jobid)

	# Waiting until job is matched

        self.remove("%s/status.output"%(self.MYTMPDIR))

        self.run_command_continue_on_error ("glite-wms-job-status %s >> %s/status.output"%(jobid,self.MYTMPDIR))

        STATUS=self.run_command_continue_on_error("grep -m 1 \'Current Status\' %s/status.output | awk -F: \'{print $2}\'"%(self.MYTMPDIR))

        STATUS = string.strip(STATUS)

        while STATUS.find("Submitted") != -1 or STATUS.find("Waiting") != -1 :
            time.sleep(3)
            self.remove("%s/status.output"%(self.MYTMPDIR))
            self.run_command_continue_on_error ("glite-wms-job-status %s >> %s/status.output"%(jobid,self.MYTMPDIR))
            STATUS=self.run_command_continue_on_error("grep -m 1 \'Current Status\' %s/status.output | awk -F: \'{print $2}\'"%(self.MYTMPDIR))
            STATUS = string.strip(STATUS)


        OUTPUT=commands.getstatusoutput("grep -m 1 Destination %s/status.output | sed -e \"s/Destination://\""%(self.MYTMPDIR))

        if OUTPUT[0] != 0 :
           logging.debug("Job %s doesn't match"%(jobid))
           self.remove("%s/status.output"%(self.MYTMPDIR))
           raise GeneralError("grep -m 1 Destination %s/status.output | sed -e \"s/Destination://\""%(self.MYTMPDIR),"Job %s doesn't match"%(jobid))

        self.remove("%s/status.output"%(self.MYTMPDIR))

        CENAME=string.strip(OUTPUT[1])

        logging.info("Destination CE is %s",CENAME)

        return CENAME


    # Return the logged "Status Reason"
    # Trow RunCommandError exception if status command fails
    def get_StatusReason(self,jobid):
        
        logging.info("Extract the status reason for the job %s",jobid)  
        
        OUTPUT=self.run_command_continue_on_error("glite-wms-job-status %s"%(jobid))
            
        for line in OUTPUT.splitlines():
            if line.split(":")[0].strip()=="Status Reason":
                reason=line.split(":")[1].strip()
                break
        
        logging.debug("Status reason is: %s"%(reason))
        
        return reason
        
    # Return a vector with "Logged Reason(s)"
    # Trow RunCommandError exception if status command fails 
    def getLoggedReason(self, jobid):
        
        reason=[]
        
        logging.info("Extract the logged reason for the job %s",jobid)   
        
        OUTPUT=self.run_command_continue_on_error("glite-wms-job-status %s"%(jobid))
        
        if OUTPUT.find("Logged Reason(s):") == -1:
        
            logging.info("We not found any 'Logged reasons'")
        
        else:
        
            for line in OUTPUT[OUTPUT.find("Logged Reason(s):")+18:].splitlines():
                if line.find(" - ") != -1:
                    reason.append(line[line.find(" - ")+3:])
                else:
                    break
            
            
            #reason=OUTPUT[OUTPUT.find("Logged Reason(s):")+17: OUTPUT.find("Status Reason:")].split("\n    -")
        
            logging.debug("Logged reasons are: %s"%(reason))
        
        return reason
        

    ########################## JDL #######################################

    def use_external_jdl(self,filename):
        # copy external jdl so we can manipulate it

        logging.info("Use the jdl file %s"%(filename))
        
        FILE=open("data/%s"%(filename), "r")
        
        jdl=FILE.read()

        FILE.close()
        
        FILE=open(self.JDLFILE, "w")
        
        if jdl[0]=="[": # remove [ ] if present
            FILE.write(jdl[1:-2])
            logging.debug("Used jdl is: %s"%(jdl[1:-2]))
        else:
            FILE.write(jdl)
            logging.debug("Used jdl is: %s"%(jdl))
            
        FILE.close()
        


    def use_utils_jdl(self):

        logging.info("Update jdl file path to use jdls from utils")

        self.JDLFILE="%s/example.jdl"%(self.MYTMPDIR)


    # add the given couple (att, value) to the jdl (string value)
    def add_jdl_attribute(self, jdl, att, value):

        logging.info("Add the attribute %s=\"%s\" to jdl",att,value)

        FILE=open(jdl,"a")

        FILE.write("%s=\"%s\";\n"%(att,value))

        FILE.close()


    # add the given couple (att, value) to the jdl (not string value)
    def add_jdl_general_attribute(self, jdl, att, value):

        logging.info("Add the attribute %s=%s to jdl",att,value)

        FILE=open(jdl,"a")

        FILE.write("%s=%s;\n"%(att,value))

        FILE.close()


    def change_jdl_attribute(self,jdl,attribute,value):

        logging.info("Set new value (%s) at attribute %s"%(value,attribute))

        FILE=open(jdl,"r")
        lines=FILE.readlines()
        FILE.close()

        for line in lines:
            if line.find(attribute)!=-1:
                lines[lines.index(line)]="%s=%s;\n"%(attribute,value)
                break

        FILE=open(jdl,"w")

        for line in lines:
            FILE.write(line)

        FILE.close()

    # define a simple jdl and save it in filename
    def set_jdl(self,filename):

       self.remove(filename)

       logging.info("Define a simple jdl and save it in %s",filename)

       FILE = open(filename,"w")

       FILE.write("Executable = \"/bin/hostname\";\n")
       FILE.write("StdOutput  = \"std.out\";\n")
       FILE.write("StdError   = \"std.err\";\n")
       FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n")
       FILE.write("ShallowRetryCount = 3;\n")

       FILE.close()

    
    # define a 15 minutes long jdl and save it in $1
    def set_long_jdl(self,filename):

        logging.info("Try to create a 15 minutes long jdl file")

        self.remove(filename)

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/sleep\";\n")
        FILE.write("Arguments = \"900\";\n")
        FILE.write("MyProxyServer = \"%s\";\n"%(self.get_MYPROXY_SERVER()))

        FILE.close()

        logging.info("New long jdl file created successfully ")


    # define a jdl with ISB and save it in $1
    def set_isb_jdl(self,filename):

          self.remove(filename)

          logging.info("Define a jdl with ISB and save it in %s",filename)

          FILE = open(filename,"w")

          FILE.write("Executable = \"/bin/ls\";\n")
          FILE.write("Arguments = \"-la\";\n")
          FILE.write("StdOutput = \"std.out\";\n")
          FILE.write("StdError = \"std.err\";\n")
          FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n")
          FILE.write("InputSandbox = \"%s\";\n"%(filename))

          FILE.close()

    
    def set_dag_jdl(self,filename):

        self.remove(filename)

        logging.info("Define a DAG jdl and save it in %s",filename)

        FILE = open(filename,"w")

    
        FILE.write("Type = \"dag\";\n")
        FILE.write("nodes = [\n")
        FILE.write("nodeA = [\n")
        FILE.write("description = [\n")
        FILE.write("JobType = \"Normal\";\n")
        FILE.write("Executable = \"/bin/date\";\n")
        FILE.write("StdOutput  = \"std.out\";\n");
        FILE.write("StdError   = \"std.err\";\n");
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
        FILE.write("];\n");
        FILE.write("];\n");
        FILE.write("nodeB = [\n");
        FILE.write("description = [\n");
        FILE.write("JobType = \"Normal\";\n");
        FILE.write("Executable = \"/bin/date\";\n");
        FILE.write("StdOutput  = \"std.out\";\n");
        FILE.write("StdError   = \"std.err\";\n");
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
        FILE.write("];\n");
        FILE.write("];\n");
        FILE.write("nodeC = [\n");
        FILE.write("description = [\n");
        FILE.write("JobType = \"Normal\";\n");
        FILE.write("Executable = \"/bin/date\";\n");
        FILE.write("StdOutput  = \"std.out\";\n");
        FILE.write("StdError   = \"std.err\";\n");
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
        FILE.write("];\n");
        FILE.write("];\n");
        FILE.write("];\n");
        FILE.write("dependencies = { { nodeA, nodeB },{  nodeB, nodeC } };\n");
        


        FILE.close()


    # define a jdl which trigger one shallow resubmission and save it in filename
    def set_shallow_jdl(self,filename):

        self.remove(filename)

        logging.info("Define a jdl which trigger one shallow resubmission and save it in %s",filename)

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/hostname\";\n")
        FILE.write("StdOutput  = \"std.out\";\n")
        FILE.write("StdError   = \"std.err\";\n")
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n")
        FILE.write("ShallowRetryCount = 2; \n")
        FILE.write("Prologue = \"/bin/false\";\n")

        FILE.close()



    # define a jdl which trigger one deep resubmission and save it in filename
    def set_deep_jdl(self,filename):

        self.remove(filename)

        logging.info("Define a jdl which trigger one deep resubmission and save it in %s",filename)

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/hostname\";\n")
        FILE.write("StdOutput  = \"std.out\";\n")
        FILE.write("StdError   = \"std.err\";\n")
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n")
        FILE.write("RetryCount = 2; \n")
        FILE.write("Epilogue = \"/bin/false\";\n")

        FILE.close()

    # add given requirements  to jdl
    # require: JDLFILE
    def set_requirements(self,requirements):

        logging.info("Add the attribute Requirements=%s to jdl"%(requirements))

        FILE=open(self.JDLFILE,"a")

        FILE.write("Requirements=%s;\n"%(requirements))

        FILE.close()

        logging.debug("The new saved jdl is:\n%s"%(commands.getoutput("cat %s"%(self.JDLFILE))))


    def set_destination_ce(self,filename,destination_ce):

         logging.info("Set Requirements expression for the destination CE at the jdl file.")
         logging.info("Requirements=RegExp(\"%s\",other.GlueCEUniqueID);",destination_ce)

         FILE=open(filename,"a")

         FILE.write("Requirements=RegExp(\"%s\",other.GlueCEUniqueID);\n"%(destination_ce))

         FILE.close()


    
    ############################################3
    # define configuration file and save it in $1
    # --> require: WMS
    # --> require: VO
    # --> require: LB
    # --> require: DEFAULTREQ
    def set_conf(self,filename):

       self.remove(filename)

       FILE = open(filename,"w")

       FILE.write ("[\n")
       FILE.write ("  WMProxyEndPoints = {\"https://%s:7443/glite_wms_wmproxy_server\"};\n"%(self.WMS))
       FILE.write ("  LBAddresses= {\"%s\"};\n"%(self.LB))
       FILE.write ("  jdlDefaultAttributes = [\n")
       FILE.write ("    VirtualOrganisation = \"%s\";\n"%(self.VO))
       FILE.write ("    Requirements = %s ;\n"%(self.DEFAULTREQ))
       FILE.write ("    Rank =  -other.GlueCEStateEstimatedResponseTime;\n")
       FILE.write ("    SignificantAttributes = { \"Requirements\",\"Rank\" };\n")
       FILE.write ("  ]\n")
       FILE.write ("]\n")

       FILE.close()


    def run_command_continue_on_error(self,args):
 
       logging.info ("[ %s ] %s"%(strftime("%H:%M:%S"),args))

       OUTPUT=commands.getstatusoutput(args)

       if OUTPUT[0]!=0 :
          logging.error('Command %s failed. Failure message: %s',args,OUTPUT[1])
          ret=1
          raise RunCommandError(args,OUTPUT[1])
          return ret

       logging.info('Command %s executed successfully',args)
       logging.debug("Command output: %s",OUTPUT[1])

       return OUTPUT[1]


    def run_command_fail_continue_on_error(self,args):

       logging.info ("[ %s ] %s"%(strftime("%H:%M:%S"),args))

       OUTPUT=commands.getstatusoutput(args)

       if OUTPUT[0]==0 :
          logging.error('Command %s not failed as expected'%(args))
          ret=1
          raise RunCommandError(args,"Command %s not failed as expected"%(args))
          return ret

       logging.info('Command %s failed as expected',args)
       logging.debug("Command output: %s",OUTPUT[1])

       return OUTPUT[1]

    
    # .... wait until job $1 is done or time is out
    # Need these two variables: $SLEEP_TIME $NUM_STATUS_RETRIEVALS
    def wait_until_job_finishes(self,jobid):


        logging.info("Wait until job %s finishes ...",jobid)

        logging.info("Iterating %s times and each time wait for %s secs",self.NUM_STATUS_RETRIEVALS,self.SLEEP_TIME)

        counter=0

        while self.job_is_finished(jobid) == 0 :

            if counter >= int(self.NUM_STATUS_RETRIEVALS) :
                logging.error("Timeout reached while waiting the job %s to finish",jobid)
                raise TimeOutError("","Timeout reached while waiting the job %s to finish"%(jobid))
               

            logging.info("Job's %s status is %s ... sleeping %s seconds ( %s/%s )",jobid,self.JOBSTATUS,self.SLEEP_TIME,counter,self.NUM_STATUS_RETRIEVALS)
            time.sleep(int(self.SLEEP_TIME))
            counter=counter+1


    def wait_until_job_finishes_no_timeout_error(self,jobid):

        logging.info("Wait until job %s finishes ...",jobid)

        logging.info("Iterating %s times and each time wait for %s secs",self.NUM_STATUS_RETRIEVALS,self.SLEEP_TIME)

        counter=0

        while self.job_is_finished(jobid) == 0 :

            if counter >= int(self.NUM_STATUS_RETRIEVALS) :
                logging.error("Timeout reached while waiting the job %s to finish",jobid)
                self.run_command_continue_on_error("glite-wms-job-cancel -c %s --noint %s"%(self.get_config_file(),jobid))

            logging.info("Job's %s status is %s ... sleeping %s seconds ( %s/%s )",jobid,self.JOBSTATUS,self.SLEEP_TIME,counter,self.NUM_STATUS_RETRIEVALS)
            time.sleep(int(self.SLEEP_TIME))
            counter=counter+1


    # Extract the "status" of the job given as input ($1 must be a valid JOBID)
    # --> set JOBSTATUS
    def job_status(self,jobid):

       self.JOBSTATUS="Unknown"

       self.remove(self.TMPFILE)

       self.run_command_continue_on_error ("glite-wms-job-status %s >> %s"%(jobid,self.TMPFILE))

       OUTPUT=commands.getstatusoutput("cat %s"%(self.TMPFILE))

       logging.debug("%s",OUTPUT[1])

       self.JOBSTATUS=self.run_command_continue_on_error("grep -m 1 \'Current Status\' %s | awk -F: \'{print $2}\'"%(self.TMPFILE))

       self.JOBSTATUS = string.strip(self.JOBSTATUS)

       logging.info('Job %s status is %s',jobid,self.JOBSTATUS)  

       self.remove(self.TMPFILE)

       return 0


    # Check if job described in JOBIDFILE is finished
    # returns 0 if job is not finished
    # returns 1 if job is DoneOK, 2 if Aborted
    # returns 3 if jobs is Cancelled and 4 if Done (Exit code != 0)
    # returns 5 if jobs is Cleared
    # returns 6 if job is Done (Failed)
    def job_is_finished(self,jobid):

       logging.info('Check if job %s is finished',jobid)

       self.job_status(jobid)

       # ... exit if it is Aborted
       if self.JOBSTATUS.find('Aborted') != -1 :
          logging.info("Job %s was Aborted !",jobid)
          return 2


       # ... or Cancelled
       if self.JOBSTATUS.find('Cancelled') !=-1 :
          logging.info("Job %s has been cancelled !",jobid)
          return 3


       # ... or Failed
       if self.JOBSTATUS.find('(Exit Code !=0)') != -1 :
          logging.info("Job %s finished with exit code != 0 !",jobid)
          return 4


       # ... or Cleared
       if self.JOBSTATUS.find('Cleared') != -1 :
          logging.info("Job %s has been cleared !",jobid)
          return 5


       # ... go to the next step if it is a success
       if self.JOBSTATUS.find('Done (Success)') != -1 :
         logging.info("Job %s finished !",jobid)
         return 1


       if self.JOBSTATUS.find('Done (Failed)') != -1 :
         logging.info("Job %s finished !",jobid)
         return 6


       logging.info('Job %s is not finished yet',jobid)

       return 0


    ###############################################################

    def prepare(self,args):

        try:
            opts,args = getopt.getopt(args,'ab:i:hld:c:s')
        except getopt.GetoptError,err:
            print ''
            print str(err)
            self.usage(self.CMD)
            sys.exit(1)

        # Test ID
        self.ID=strftime("%Y%m%d%H%M%S")

        # ... define default values for optional parameters

        for option,value in opts:

            if option=="-a":
                self.ALL=1
            elif option=="-b":
                self.CURRENTTEST=value
            elif option=="-i":
                self.INPUT_TEST_FILE=value
            elif option=="-h":
                self.usage(self.CMD)
                sys.exit(0)
            elif option=="-d":
                if value=="1":
                    self.LOG_LEVEL='WARNING'
                elif value=="2":
                    self.LOG_LEVEL='INFO'
                else:
                    self.LOG_LEVEL='DEBUG'
            elif option=="-l":
                self.LOG=1
            elif option=="-c":
                self.CONF=value
            elif option=="-s":
                self.show_test()
                sys.exit(0)
        

        if self.ALL==0 and len(self.INPUT_TEST_FILE)==0 and len(self.CURRENTTEST)==0:
            self.usage(self.CMD)
            sys.exit(1)


        if self.ALL==0 and os.path.isfile(self.INPUT_TEST_FILE)==False and len(self.CURRENTTEST)==0:
            print ""
            print "+-----------------------------------------------------------------------+"
            print "Unable to continue , can not find the input file: %s"%(self.INPUT_TEST_FILE)
            print "+-----------------------------------------------------------------------+"
            print ""
            sys.exit(1)

        self.START_TIME=strftime("%H:%M:%S")

        # source configuration values
        if os.path.isfile(self.CONF):
            self.load_configuration(self.CONF)

        if self.LOG_LEVEL=='WARNING':
            self.NUM_LOG_LV=30
        elif self.LOG_LEVEL=='INFO':
            self.NUM_LOG_LV=20
        else:
            self.NUM_LOG_LV=10

        # ... create temporary directory
        self.MYTMPDIR="%s/regression-tests_%s"%(os.getcwd(),self.ID)
        try:
            os.mkdir(self.MYTMPDIR,0755)
        except os.error, e:
            self.exit_failure("Fail to create temporary directory")
            return 1

        # ... create log file
        if self.LOG == 1 :
            self.TESTLOGFILE='RegressionTest_%s.log'%(self.ID)
        else: # write the logfile in the working directory just for debug
            self.TESTLOGFILE='%s/RegressionTest_%s.log'%(self.MYTMPDIR, self.ID)

        logging.basicConfig(filename='%s'%(self.TESTLOGFILE),format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S',level=self.NUM_LOG_LV)


        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "+ Regression TestSuite ....                         +"
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"

        # ... define common directory and file names
        self.JOB_OUTPUT_DIR="%s/jobOutput"%(self.MYTMPDIR)

        os.mkdir("%s"%(self.JOB_OUTPUT_DIR))

        self.LOGFILE="%s/log.txt"%(self.MYTMPDIR)
        self.OUTPUTFILE="%s/output.txt"%(self.MYTMPDIR)
        self.PROXY="%s/proxy.file"%(self.MYTMPDIR)
        self.TMPFILE="%s/file.tmp"%(self.MYTMPDIR)
        self.CONFIG_FILE="%s/wms.conf"%(self.MYTMPDIR)
        self.JDLFILE="%s/example.jdl"%(self.MYTMPDIR)

        # Create default jdl and config file
        self.set_jdl(self.JDLFILE)
        self.set_conf(self.CONFIG_FILE)

    

    def load_configuration(self,conf):

       FILE = open(conf,"r")
       lines=FILE.readlines()
       FILE.close()

       for line in lines:

           if line.isspace()==False and line.find("#")==-1:
              line=string.strip(line)
              ret=line.split("=")
              setattr(self,'%s'%(ret[0]),ret[1])


    def show_progress(self,title):

        self.CURRENTTEST=title
        print ""
        os.system("echo -e \"\\e[1;34m %s \\e[0m\""%(title))
        print ""


    def show_critical(self,title):
    
        print ""
        os.system("echo -e \"\\e[1;31m %s \\e[0m\""%(title))
        print ""

    def log_error(self,msg):

        FILE=open("%s/errors.log"%(self.MYTMPDIR),"a")

        FILE.write("%s\n"%msg)

        FILE.close()

    def log_traceback(self,msg):

        FILE=open("%s/traceback_errors.log"%(self.MYTMPDIR),"a")

        FILE.write("%s\n"%msg)

        FILE.close()


    # remove a file only if exists
    def remove(self,filename):

      logging.debug("Remove file %s..."%(filename))

      if os.path.isfile(filename):
        os.unlink(filename)



    # ... cleanup temporary files
    def cleanup(self):

      logging.info ("Cleaning up %s ..."%(self.MYTMPDIR))

      self.remove (self.OUTPUTFILE)

      self.remove (self.LOGFILE)
      
      self.remove (self.CONFIG_FILE)
      self.remove (self.TMPFILE)

      self.remove ("%s/std.out"%(self.JOB_OUTPUT_DIR))
      self.remove ("%s/std.err"%(self.JOB_OUTPUT_DIR))
      self.remove ("%s/out.txt"%(self.JOB_OUTPUT_DIR))

      logging.debug ("Remove %s directory ..."%(self.JOB_OUTPUT_DIR))

      if os.path.isdir(self.JOB_OUTPUT_DIR):
          os.system("rm -rf %s"%(self.JOB_OUTPUT_DIR))

      if os.path.isfile(self.PROXY):
          commands.getoutput("voms-proxy-destroy -file %s"%(self.PROXY))

      logging.debug("Remove %s directory ..."%(self.MYTMPDIR))

      if os.path.isdir(self.MYTMPDIR) :
          os.system("rm -rf %s"%(self.MYTMPDIR))


    # FAILURE exit: arg is the failure reason
    def exit_failure(self,error_msg):

        # No cleanup for debug
       
        logging.info("Started: %s"%(self.START_TIME))
        logging.info("Ended  : %s"%(strftime("%H:%M:%S")))
        logging.error("    >>> TEST FAILED <<<")
        logging.error(" >>> failure reason: %s <<< "%(error_msg))

        logging.warning(" Test directory %s"%(self.MYTMPDIR))
        logging.warning(" has not been cleaned for debug purpose")

        self.show_critical("TestSuite failed: %s"%(error_msg))
        sys.exit(2)


    # GOOD exit
    # Exit code: 0
    def exit_success(self):

        self.cleanup()

        logging.info("Started: %s"%(self.START_TIME))
        logging.info("Ended  : %s"%(strftime("%H:%M:%S")))
        logging.info("    === test PASSED === ")

        self.show_progress("All tests PASSED")
        sys.exit(0)

    # Warning exit: arg is the warning message
    # Exit code: 1 (as required by NAGIOS)
    def exit_warning(self,msg):

        self.cleanup()

        logging.info("Started: %s"%(self.START_TIME))
        logging.info("Ended  : %s"%(strftime("%H:%M:%S")))
        logging.warning("  *** Warning: %s *** "%(msg))

        self.show_critical("WARNING: %s"%(msg))
        sys.exit(1)

    # ... exit on Ctrl^C
    def exit_interrupt(self,signum,frame):

       self.exit_warning("Interrupted by user")

    # ... exit on timeout: try cancel job and exit
    def exit_timeout(self,jobid):

       logging.info ("Try to remove job...")
       self.run_command("glite-wms-job-cancel --noint %s"%(jobid))
       time.sleep(60)
       self.job_status(jobid)

       if self.JOBSTATUS == "Cancelled" :
           logging.info("Job has been succesfully cancelled")
       else:
           logging.warning("Job has NOT been cancelled")

       self.exit_warning("Timeout reached")



    def load_tests(self):

        if self.ALL==1:
            tests=self.load_tests_from_database()
        elif self.CURRENTTEST != "":
            tests=["%s"%(self.CURRENTTEST)]
        else:
            tests=self.load_tests_from_file(self.INPUT_TEST_FILE)

        return tests

    def load_tests_from_file(self,filename):

        tests=[]

        FILE = open(filename,"r")
        lines=FILE.readlines()
        FILE.close()

        for line in lines:

           if line.isspace()==False and line.find("#")==-1 :
              line=string.strip(line)
              tests.append(line)
             
        return tests


    def load_tests_from_database(self):

        tests=[]
        
        con = sqlite.connect('testdata/tests.db')

        cur=con.cursor()

        cur.execute("select bug_number from tests")

        for bug in cur:
            tests.append(bug[0])

        con.close()

        return tests


    def show_test(self):
        
        print "These are all the available tests"
        
        con = sqlite.connect('testdata/tests.db')
        cur=con.cursor()
        cur.execute("select bug_number, summary from tests order by bug_number")

        for bug in cur:
            print "Test for bug %i: %s"%(bug[0], bug[1])
            
        con.close()
        
        return 0


    def execute_test(self,target):

        try:

            module_name="bugs/%s"%(target)
         
            logging.info("Try to import module for bug %s"%(target))

            __import__(module_name)

            bug_module = sys.modules[module_name]

            logging.info("Start test of bug")

            bug_module.run(self)
            
        except (RunCommandError,GeneralError,TimeOutError) , e :
            self.show_critical("\tTest for bug %s fails"%(target))
            logging.error("Test for bug %s fails"%(target))
            self.fails.append(target)
            self.log_error("%s"%(self.get_current_test()))
            self.log_error("Command: %s"%(e.expression))
            self.log_error("Message: %s"%(e.message))
            self.log_error("")
            self.log_traceback("%s"%(self.get_current_test()))
            self.log_traceback(traceback.format_exc())
        except ImportError, e:
            self.show_critical("Unable to find the required module for bug %s . Test is skipped"%(target))
            self.log_error("Unable to find the required module for bug %s . Test is skipped"%(target))
        except RetryError, e:
            self.show_critical("\tWARNING Test for bug %s should be repeat"%(target))
            self.log_error("%s"%(self.get_current_test()))
            self.log_error("Command: %s"%(e.expression))
            self.log_error("Message: %s"%(e.message))
            self.log_error("")
            self.log_traceback("%s"%(self.get_current_test()))
            self.log_traceback(traceback.format_exc())


    ############################ SSH methods ###################################


    def get_Username(self):
        return self.WMS_USERNAME


    def get_Password(self):
        return self.WMS_PASSWORD


    def open_ssh(self,host,user,passwd):

        try:

            logging.info("Create ssh connection for host %s",host)

            ssh = paramiko.SSHClient()

            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(host,username=user,password=passwd)


        except (socket.error,paramiko.BadHostKeyException,paramiko.AuthenticationException,paramiko.SSHException) , e:
           logging.error("Error description => %s",e)
           raise GeneralError("method open_ssh","Error description => %s"%(e))

        return ssh


    def close_ssh(self,ssh):

        logging.info("Close ssh connection")

        ssh.close()


    def execute_remote_cmd(self,ssh,cmd):

       logging.info("Execute remote command %s",cmd)

       stdin,stdout,stderr=ssh.exec_command(cmd)

       errors=stderr.readlines()
       output_lines=stdout.readlines()

       output=' '.join(output_lines)

       if len(errors)!=0 :

          #Warning during glite-wms-wmproxy restart
          if errors[0].find("warn")==-1 :
            logging.error("Error while executing remote command => %s",cmd)
            logging.error("Error Description: %s",errors)
            raise GeneralError("Method execute_remote_cmd","Error while executing remote command => %s"%(cmd))
       else:
         logging.info('Command %s executed successfully',cmd)
         logging.debug("Command output: %s",output)

       return output


    def execute_remote_cmd_fail(self,ssh,cmd):

       logging.info("Execute remote command %s",cmd)

       stdin,stdout,stderr=ssh.exec_command(cmd)

       errors=stderr.readlines()
       output_lines=stdout.readlines()

       output=' '.join(output_lines)
       err_msg=' '.join(errors)

       if len(errors)!=0 :

          #Warning during glite-wms-wmproxy restart
          if errors[0].find("warn")==-1 :
            logging.info('Command %s failed as expected',cmd)
            logging.debug("Command error message: %s",err_msg)
       else:
          logging.error("Command %s not failed as expected",cmd)
          logging.error("Command output: %s",output)
          raise GeneralError("Method execute_remote_cmd_fail","Error remote command %s not failed as expected"%(cmd))

       return err_msg


    def ssh_put_file(self,ssh,src,dst):

        logging.info("Send file: %s at remote host"%(file))

        try:

            ftp = ssh.open_sftp()

            ftp.put(src,dst)

            ftp.close()

        except Exception, e:
           logging.error("Error while transfer file %s at remote host",src)
           logging.error("Error Description: %s",e)
           raise GeneralError("Method ssh_put_file","Error while transfer file %s at remote host"%(src))


    def ssh_get_file(self,ssh,src,dst):

        logging.info("Get file: %s from remote host"%(file))

        try:

            ftp = ssh.open_sftp()

            ftp.get(src,dst)

            ftp.close()

        except Exception, e:
           logging.error("Error while transfer file %s from remote host",src)
           logging.error("Error Description: %s",e)
           raise GeneralError("Method ssh_get_file","Error while transfer file %s from remote host"%(src))


    #When olds="*" then the method find the current value of the attribute
    def change_remote_file(self,ssh,file,attributes,olds,news):

        logging.info("Change attributes at remote file %s"%(file))

        self.remove("%s/local_copy"%(self.get_tmp_dir()))

        try:

            self.execute_remote_cmd(ssh, "cp -f %s %s.bak"%(file,file))

            ftp = ssh.open_sftp()

            logging.info("Get file %s"%(file))
            
            #Get required file from remote host
            ftp.get(file,"%s/local_copy"%(self.get_tmp_dir()))

            logging.info("Read file %s"%(file))

            #Read contents from file
            FILE=open("%s/local_copy"%(self.get_tmp_dir()),"r")
            lines=FILE.readlines()
            FILE.close()

            counter=0
            find=0

            for attribute in attributes:

                old=olds[counter]
                new=news[counter]
                find=0

                #find the current value of attribute
                if old=="*":
                    
                  for line in lines:
                     if line.find(attribute)!=-1:
                        old=line.split("=")[1][:-2].strip()
                        
    
                logging.info("For attribute %s change the value from %s to %s"%(attribute,old,new))

                for line in lines:

                    if line.find("=")!= -1:

                       attr=line.split("=")

                       if attr[0].strip()==attribute  and attr[1].find(old)!=-1 :
                            logging.info("Attribute %s found."%(attribute))
                            lines[lines.index(line)]=line.replace(old,new)
                            find=1

                if find==0:
                    logging.error("Unable to find attribute %s"%(attribute))
                    raise GeneralError("Method change_remote_file","Unable to find attribute %s"%(attribute))
                
                counter=counter+1

            #write changes to local copy of file
            logging.info("Save changes to %s/local_copy"%(self.get_tmp_dir()))
            FILE=open("%s/local_copy"%(self.get_tmp_dir()),"w")
            FILE.writelines(lines)
            FILE.close()

            #Save file again to remote host
            logging.info("Upload new version of file %s to remote host"%(file))
            ftp.put("%s/local_copy"%(self.get_tmp_dir()),file)

            ftp.close()
            

        except Exception, e:
            logging.error("Error while edit file %s at remote host",file)
            logging.error("Error Description: %s",e)
            raise GeneralError("Method change_remote_file","Error while edit file %s at remote host"%(file))


    def add_attribute_to_remote_file(self,ssh,file,section,attributes,values):

        logging.info("Add attributes at remote file %s"%(file))

        self.remove("%s/local_copy"%(self.get_tmp_dir()))

        try:

            self.execute_remote_cmd(ssh, "cp -f %s %s.bak"%(file,file))

            ftp = ssh.open_sftp()

            logging.info("Get file %s"%(file))

            #Get required file from remote host
            ftp.get(file,"%s/local_copy"%(self.get_tmp_dir()))

            logging.info("Read file %s"%(file))

            #Read contents from file
            FILE=open("%s/local_copy"%(self.get_tmp_dir()),"r")
            lines=FILE.readlines()
            FILE.close()

            new_lines=[]

            row=0
            counter=0

            for line in lines:
                if line.find("%s"%(section))!=-1:
                    row=lines.index(line)+1

            new_lines=lines[:row]

            for attribute in attributes:

               add=1
               
               logging.info("Check if attribute %s already exists."%(attribute))
               
               #Check if already exists
               for li in lines:
                 if li.find("%s"%(attribute))!=-1:
                     logging.info("Attribute %s already exists. Go to next"%(attribute))
                     add=0
                     break

               if add==1:
                  logging.info("Add new attribute %s with value %s"%(attribute,values[counter]))
                  new_lines.append("    %s = %s;\n"%(attribute,values[counter]))

               counter=counter+1

            new_lines[len(new_lines):]=lines[row:]
            
            #write changes to local copy of file
            logging.info("Save changes to %s/local_copy_new"%(self.get_tmp_dir()))
            FILE=open("%s/local_copy_new"%(self.get_tmp_dir()),"w")
            FILE.writelines(new_lines)
            FILE.close()
            
            #Save new file to remote host
            logging.info("Upload new version of file %s to remote host"%(file))
            ftp.put("%s/local_copy_new"%(self.get_tmp_dir()),file)

            ftp.close()


        except Exception, e:
            logging.error("Error while edit file %s at remote host",file)
            logging.error("Error Description: %s",e)
            raise GeneralError("Method change_remote_file","Error while edit file %s at remote host"%(file))



    #When olds="*" then the method find the current value of the attribute
    def change_attribute_at_remote_file_section(self,ssh,file,attribute,section,new):

        logging.info("Change attribute at remote file %s for section %s"%(file,section))

        self.remove("%s/local_copy"%(self.get_tmp_dir()))

        try:

            self.execute_remote_cmd(ssh, "cp -f %s %s.bak"%(file,file))

            ftp = ssh.open_sftp()

            logging.info("Get file %s"%(file))

            #Get required file from remote host
            ftp.get(file,"%s/local_copy"%(self.get_tmp_dir()))

            logging.info("Read file %s"%(file))

            #Read contents from file
            FILE=open("%s/local_copy"%(self.get_tmp_dir()),"r")
            lines=FILE.readlines()
            config=''.join(lines)
            FILE.close()

            logging.info("Search section %s"%(section))

            sects=config.split("%s =  ["%(section));

            find=0

            if len(sects)!=2:
                 logging.error("Unable to find section %s"%(section))
                 raise GeneralError("Method change_attribute_at_remote_file","Unable to find section %s"%(section))
            else:

                start_index=lines.index("%s =  [\n"%(section))

                sect_lines=sects[1].split("\n")

                for line in sect_lines:

                    if line.find("%s"%(attribute))!=-1:
                        attr=line.split("=")
                        inx=sect_lines.index(line)
                        line=line.replace(attr[1][:-1].strip(),new)
                        lines[start_index+inx]="%s\n"%(line)
                        find=1
                        break
              
                if find==0:
                    logging.error("Unable to find attribute %s"%(attribute))
                    raise GeneralError("Method change_remote_file","Unable to find attribute %s"%(attribute))

                #write changes to local copy of file
                logging.info("Save changes to %s/local_copy"%(self.get_tmp_dir()))
                FILE=open("%s/local_copy"%(self.get_tmp_dir()),"w")
                FILE.writelines(lines)
                FILE.close()

                #Save file again to remote host
                logging.info("Upload new version of file %s to remote host"%(file))
                ftp.put("%s/local_copy"%(self.get_tmp_dir()),file)

                ftp.close()


        except Exception, e:
            logging.error("Error while edit file %s at remote host",file)
            logging.error("Error Description: %s",e)
            raise GeneralError("Method change_remote_file","Error while edit file %s at remote host"%(file))
