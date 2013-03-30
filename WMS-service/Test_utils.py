import getopt
import os
import sys
import time
import commands
import getpass
import string

import logging

from Exceptions import *
from time import strftime


class Test_utils:

    def __init__(self,cmd,description):

        self.DESCRIPTION=description
        self.ID=''
        self.CMD=cmd
        self.NUM_STATUS_RETRIEVALS=120
        self.SLEEP_TIME=30
        self.DELEGATION_OPTIONS="-a"
        self.DEFAULTREQ="other.GlueCEStateStatus == \"Production\""
        self.CONF="wms-command.conf"
        self.LOG=0
        self.NOPROXY=1
        self.CE=''
        self.WMS=''
        self.VO=''
        self.LB=''
        self.TESTLOGFILE=''
        self.START_TIME=''
        self.MYTMPDIR=''
        self.JOB_OUTPUT_DIR=''
        self.LOGFILE=''
        self.OUTPUTFILE=''
        self.JOBIDFILE=''
        self.PROXY=''
        self.TMPFILE=''
        self.JDLFILE=''
        self.CONFIG_FILE=''
        self.PASS=''
        self.JOBIDFILE=''
        self.JOBSTATUS=''
        self.EXTERNAL_JDL=0
        self.EXTERNAL_JDL_FILE=''
        self.LOG_LEVEL='DEBUG'
        self.USER_CONF=0
        self.NUM_LOG_LV=10
        self.VERBOSE=0
        self.MYPROXYSERVER=''
        self.CURRENTTEST=''
        self.SUBTESTS=''
        self.ENABLEDTESTS=[]
        self.RUN_ALL=1
        self.WMS_USERNAME=''
        self.WMS_PASSWORD=''
        self.YAIM_FILE=''
        self.ROLE=''
        self.LFC=''
        self.SE=''
        self.ISB_DEST_HOSTNAME=''
        self.ISB_DEST_USERNAME=''
        self.ISB_DEST_PASSWORD=''
        self.OSB_DEST_HOSTNAME=''
        self.OSB_DEST_USERNAME=''
        self.OSB_DEST_PASSWORD=''
        self.EXTERNAL_REQUIREMENTS=0


    def usage(self,msg):

        print '\nUsage: '
        print ''
        print '%s [-h] [-l] [-v] [-d <level>] [-c <conf>] [-i] [-W <wms>] [-L <lb>] [-C <ce>] [-V <vo>] [-j <jdl file>] -s -t <tests> -r <requirements>'%(msg)
        print ''
        print " -h               this help"
        print " -l               save output in a file"
        print " -v               print log messages to stdout"
        print " -d <level >      define log level (1=WARNING, 2=INFO, 3=DEBUG)"
        print " -i               interactive mode (it asks for proxy pwd)"
        print " -c <conf>        configuration file overwrites command line options"
        print " -W <wms>         WMS host (Required)"
        print " -L <lb>          LB host (Required)"
        print " -C <ce>          CE host"
        print " -V <vo>          User VO (Required)"
        print " -j <jdl file>    External jdl file"
        print " -s                  List all available tests"
        print " -t <test numbers>   Run specific test cases. Syntax number1,numberK,numberM or number1-numberN or mixed "
        print " -r <requirement>  Set default jdl requirement"
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

    def get_jobid_file(self):
        return self.JOBIDFILE

    def get_job_status(self):
        return self.JOBSTATUS

    def get_WMS(self):
        return self.WMS

    def get_LB(self):
        return self.LB

    def get_MYPROXY_SERVER(self):
        return self.MYPROXYSERVER
    
    def get_log_file(self):
        return self.LOGFILE

    def get_NOPROXY(self):
        return self.NOPROXY

    def get_PROXY(self):
        return self.PROXY

    def get_job_output_dir(self):
        return self.JOB_OUTPUT_DIR

    def has_external_jdl(self):
        return self.EXTERNAL_JDL

    def get_user_CE(self):
        return self.CE

    def get_current_test(self):
        return self.CURRENTTEST
        
    def is_all_enabled(self):
        return self.RUN_ALL


    # Extract the destination CE of the job given as input ($1 must be a valid JOBID)
    # return CENAME
    def get_CE(self,jobid):

        CENAME="Destination not available"

        self.info("Extract the destination CE of the job %s"%(jobid))

	    # Waiting until job is matched

        self.remove("%s/status.output"%(self.MYTMPDIR))

        self.run_command_continue_on_error ("glite-wms-job-status %s >> %s/status.output"%(jobid,self.MYTMPDIR))

        STATUS = self.run_command_continue_on_error("grep -m 1 \'Current Status\' %s/status.output | awk -F: \'{print $2}\'"%(self.MYTMPDIR))

        STATUS = string.strip(STATUS)

        while STATUS.find("Submitted") != -1 or STATUS.find("Waiting") != -1 :
            time.sleep(3)
            self.remove("%s/status.output"%(self.MYTMPDIR))
            self.run_command_continue_on_error ("glite-wms-job-status %s >> %s/status.output"%(jobid,self.MYTMPDIR))
            STATUS = self.run_command_continue_on_error("grep -m 1 \'Current Status\' %s/status.output | awk -F: \'{print $2}\'"%(self.MYTMPDIR))
            STATUS = string.strip(STATUS)


        OUTPUT=commands.getstatusoutput("grep -m 1 Destination %s/status.output | sed -e \"s/Destination://\""%(self.MYTMPDIR))

        if OUTPUT[0] != 0 :
           self.error("Job %s doesn't match"%(jobid))
           self.remove("%s/status.output"%(self.MYTMPDIR))
           raise GeneralError("grep -m 1 Destination %s/status.output | sed -e \"s/Destination://\""%(self.MYTMPDIR),"Job %s doesn't match"%(jobid))

        self.remove("%s/status.output"%(self.MYTMPDIR))

        CENAME=string.strip(OUTPUT[1])

        self.info("Destination CE is %s"%(CENAME))

        return CENAME

    # Extract the destination CE of the job given as input ($1 must be a valid JOBID)
    # return CENAME
    def get_dag_CE(self,jobid):

        CENAME="Destination not available"

        # Waiting until job is matched

        self.remove("%s/status.output"%(self.MYTMPDIR))

        self.run_command ("glite-wms-job-status %s >> %s/status.output"%(jobid,self.MYTMPDIR))

        STATUS = self.run_command("grep -m 1 \'Current Status\' %s/status.output | awk -F: \'{print $2}\'"%(self.MYTMPDIR))

        STATUS = string.strip(STATUS)

        self.dbg("Wait 30 secs ...")
        time.sleep(30)

        while STATUS.find("Submitted") != -1 or STATUS.find("Waiting") != -1 :
            time.sleep(3)
            self.remove("%s/status.output"%(self.MYTMPDIR))
            self.run_command ("glite-wms-job-status %s >> %s/status.output"%(jobid,self.MYTMPDIR))
            STATUS = self.run_command("grep -m 1 \'Current Status\' %s/status.output | awk -F: \'{print $2}\'"%(self.MYTMPDIR))
            STATUS = string.strip(STATUS)

        OUTPUT=commands.getstatusoutput("grep Destination %s/status.output | sed -e \"s/Destination://\" | awk \'{if(NR==2) print $1}\'"%(self.MYTMPDIR))

        if OUTPUT[0] != 0 :
           self.remove("%s/status.output"%(self.MYTMPDIR))
           self.exit_failure("Job %s doesn't match"%(jobid))

        self.remove("%s/status.output"%(self.MYTMPDIR))

        CENAME=string.strip(OUTPUT[1])

        self.info ("CE id is: %s"%(CENAME))

        return CENAME


    def get_from_coumpound_job_all_nodes_ids(self,parent_jobid):

        ids=[]

        self.info("Get all nodes ids for coumpound job: %s"%(parent_jobid))

        output=self.run_command_continue_on_error("glite-wms-job-status -v 0 %s"%(parent_jobid)).split("\n")

        for line in output:
            if line.find("Status info for the Job")!=-1 and line.find(parent_jobid)==-1:
                line=line.split("Status info for the Job :")
                ids.append(line[1].strip(" \n\t"))

        self.info("Node ids: %s"%(ids))

        return ids


    def myecho(self,msg):

        print "===> %s"%(msg)

    # Error Message (they are _always_ print to stdout)
    def error(self,msg):
        
        logging.error("%s"%(msg))
        self.myecho("ERROR: %s"%(msg))

    # Warning messages, verbose = 1
    def warn(self,msg):
        
        logging.warning("%s"%(msg))       
        if (self.VERBOSE) and (self.NUM_LOG_LV <= 30):
            self.myecho("WARNING: %s"%(msg))

    # Verbose messages, verbose = 2
    def info(self,msg):
        
        logging.info("%s"%(msg))
        if (self.VERBOSE) and (self.NUM_LOG_LV <= 20):
            self.myecho("%s"%(msg))

    # Debug messages, verbose = 3
    def dbg(self,msg):
        
        logging.debug("%s"%(msg))       
        if (self.VERBOSE) and (self.NUM_LOG_LV == 10):
            self.myecho("DEBUG: %s"%(msg))

    def show_progress(self,title):

        self.CURRENTTEST=title
        print ""
        os.system("echo -e \"\\e[1;34m %s \\e[0m\""%(title))
        print ""

    def show_critical(self,title):
        print ""
        os.system("echo -e \"\\e[1;31m %s \\e[0m\""%(title))
        print ""

    # remove a file only if exists
    def remove(self,filename):
        
        self.dbg("Remove file %s..."%(filename))

        if os.path.isfile(filename):
            os.unlink(filename)

    # ... cleanup temporary files
    def cleanup(self):

      self.info ("Cleaning up %s ..."%(self.MYTMPDIR))

      self.remove (self.OUTPUTFILE)

      self.remove (self.LOGFILE)

      self.remove (self.JOBIDFILE)

      self.remove (self.JDLFILE)

      self.remove (self.CONFIG_FILE)
      self.remove (self.TMPFILE)

      self.remove ("%s/std.out"%(self.JOB_OUTPUT_DIR))
      self.remove ("%s/std.err"%(self.JOB_OUTPUT_DIR))
      self.remove ("%s/out.txt"%(self.JOB_OUTPUT_DIR))

      self.dbg ("Remove %s directory ..."%(self.JOB_OUTPUT_DIR))

      if os.path.isdir(self.JOB_OUTPUT_DIR):
          os.system("rm -rf %s"%(self.JOB_OUTPUT_DIR))

      if os.path.isfile(self.PROXY):
          commands.getoutput("voms-proxy-destroy -file %s"%(self.PROXY))

      self.dbg("Remove %s directory ..."%(self.MYTMPDIR))

      if os.path.isdir(self.MYTMPDIR) :
          os.system("rm -rf %s"%(self.MYTMPDIR))


    # FAILURE exit: error_msg is the last failure reason
    # Exit code: 2 
    def exit_failure(self,error_msg):

        #No cleanup for debug
        self.myecho ("")
        self.myecho ("Test: %s"%(self.CMD))
        self.myecho ("WMS: %s"%(self.WMS))       
        self.myecho ("Started: %s"%(self.START_TIME))
        self.myecho ("Ended  : %s"%(strftime("%H:%M:%S")))
        self.myecho ("")
        self.myecho ("    >>> TEST FAILED <<<")
        self.myecho ("")
        self.myecho (" >>> failure reason: %s <<< "%(error_msg))
        self.myecho ("")
        self.myecho ("Test log file is %s"%(self.TESTLOGFILE))
        self.myecho ("Error messages have been written in %s/errors.log"%(self.MYTMPDIR))
        self.myecho ("")
        self.myecho (" Test directory %s has not been cleaned for debug purpose"%(self.MYTMPDIR))

        sys.exit(2)

    # GOOD exit
    # Exit code: 0
    def exit_success(self):

        self.cleanup()

        self.myecho ("")
        self.myecho ("Test: %s"%(self.CMD))
        self.myecho ("WMS: %s"%(self.WMS))
        self.myecho ("Started: %s"%(self.START_TIME))
        self.myecho ("Ended  : %s"%(strftime("%H:%M:%S")))
        self.myecho ("")
        self.myecho ("    === test PASSED === ")

        if self.LOG == 1 :
            self.myecho ("")
            self.myecho ("Test log file is %s"%(self.TESTLOGFILE))

        sys.exit(0)

    # Warning exit: msg is the warning message
    # Exit code: 1 
    def exit_warning(self,msg):

        self.cleanup()

        self.myecho ("")
        self.myecho ("Test: %s"%(self.CMD))
        self.myecho ("WMS: %s"%(self.WMS))
        self.myecho ("Started: %s"%(self.START_TIME))
        self.myecho ("Ended  : %s"%(strftime("%H:%M:%S")))
        self.myecho ("")
        self.myecho ("  *** Warning: %s *** "%(msg))
        self.myecho ("")

        if self.LOG == 1 :
            self.myecho ("")
            self.myecho ("Test log file is %s"%(self.TESTLOGFILE))

        sys.exit(1)

    # ... exit on Ctrl^C
    def exit_interrupt(self,signum,frame):

       self.exit_warning("Interrupted by user")

    # ... exit on timeout: try cancel job and exit
    def exit_timeout(self,jobid):

       self.info ("Try to remove job...")
       self.run_command("glite-wms-job-cancel --noint %s"%(jobid))
       time.sleep(60)
       self.job_status(jobid)

       if self.JOBSTATUS == "Cancelled" :
           self.info("Job has been succesfully cancelled")
       else:
           self.warn("WARNING: Job has NOT been cancelled")

       self.exit_warning("Timeout reached")

    #
    # Accept only the following attributes (everthing else is ignored):
    #
    # WMS:                    WMS hostname
    # WMS_USERNAME:           WMS account username 
    # WMS_PASSWORD:           WMS account password
    # YAIM_FILE:              Path of yaim configuration file for WMS
    # LB:                     LB hostname
    # VO:                     User VO
    # MYPROXYSERVER:          MyProxyServer hostname
    # LOG_LEVEL:              Log level
    # DEFAULTREQ:             Default requirements
    # NUM_STATUS_RETRIEVALS:  Number of retrievals before to stop test (timeout)
    # SLEEP_TIME:             Seconds before the next status check
    # ROLE:                   voms role
    # LF:                     LFC hostname
    # SE:                     SE hostname
    #
    def load_configuration(self,conf):

       attributes=['WMS','WMS_USERNAME','WMS_PASSWORD','YAIM_FILE','LB','VO','MYPROXYSERVER','LOG_LEVEL','DEFAULTREQ','NUM_STATUS_RETRIEVALS','SLEEP_TIME']

       attributes.append("ROLE")
       attributes.append("LFC")
       attributes.append("SE")
       attributes.append('ISB_DEST_HOSTNAME')
       attributes.append('ISB_DEST_USERNAME')
       attributes.append('ISB_DEST_PASSWORD')

       attributes.append('OSB_DEST_HOSTNAME')
       attributes.append('OSB_DEST_USERNAME')
       attributes.append('OSB_DEST_PASSWORD')

       FILE = open(conf,"r")
       lines=FILE.readlines()
       FILE.close()

       for line in lines:

           if line.isspace()==False and line.find("#")==-1:
              line=string.strip(line)
              ret=line.split("=",1)

              try:
                   attributes.index(ret[0])
                   setattr(self,'%s'%(ret[0]),ret[1])
              except ValueError:
                   pass


    ########################## JDL #######################################

    # define a simple jdl and save it in "filename"
    def set_jdl(self,filename):

        self.info("Define a simple jdl")

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/hostname\";\n")
        FILE.write("StdOutput  = \"std.out\";\n")
        FILE.write("StdError   = \"std.err\";\n")
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n")
        FILE.write("ShallowRetryCount = 3;\n")

        FILE.close()
       
        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


    # define a 15 minutes long jdl and save it in "filename"
    def set_long_jdl(self,filename):

        self.info("Define a 15 minutes long jdl file")

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/sleep\";\n")
        FILE.write("Arguments = \"900\";\n")

        FILE.close()
        
        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))

    # define a jdl with ISB and save it in "filename"
    def set_isb_jdl(self,filename):

        self.info("Define a jdl with ISB")

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/ls\";\n")
        FILE.write("Arguments = \"-la\";\n")
        FILE.write("StdOutput = \"std.out\";\n")
        FILE.write("StdError = \"std.err\";\n")
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n")
        FILE.write("ShallowRetryCount = 2;\n")
        FILE.write("InputSandbox = \"%s\";\n"%(filename))

        FILE.close()

        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))
    
    # define a dag jdl
    def set_dag_jdl(self,filename):

        self.info("Define a DAG jdl")

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
        FILE.write("dependencies = { { nodeA, nodeB },{  nodeA, nodeC } };\n");
        
        FILE.close()
        
        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))

    #define a collection jdl
    def set_collection_jdl(self,filename):

        self.info("Define a collection jdl")

        FILE = open(filename,"w")

        FILE.write("Type = \"collection\";\n")
        FILE.write("nodes = {\n")
        FILE.write("[\n")
        FILE.write("NodeName=\"Node_1_jdl\";\n");
        FILE.write("JobType = \"Normal\";\n")
        FILE.write("Executable = \"/bin/hostname\";\n")
        FILE.write("StdOutput  = \"std.out\";\n");
        FILE.write("StdError   = \"std.err\";\n");
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
        FILE.write("],\n");
        FILE.write("[\n")
        FILE.write("NodeName=\"Node_2_jdl\";\n");
        FILE.write("JobType = \"Normal\";\n")
        FILE.write("Executable = \"/bin/hostname\";\n")
        FILE.write("StdOutput  = \"std.out\";\n");
        FILE.write("StdError   = \"std.err\";\n");
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
        FILE.write("],\n");
        FILE.write("[\n")
        FILE.write("NodeName=\"Node_3_jdl\";\n");
        FILE.write("JobType = \"Normal\";\n")
        FILE.write("Executable = \"/bin/hostname\";\n")
        FILE.write("StdOutput  = \"std.out\";\n");
        FILE.write("StdError   = \"std.err\";\n");
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
        FILE.write("]\n");
        FILE.write("};\n");

        FILE.close()

        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


    #define a collection jdl
    def set_collection_external_jdls(self,filename):

        self.info("Define a collection jdl")

        self.set_isb_jdl("%s/node.jdl"%(self.get_tmp_dir()))

        FILE = open(filename,"w")

        FILE.write("Type = \"collection\";\n")
        FILE.write("nodes = {\n")
        FILE.write("[\n")

        FILE.write("NodeName=\"Node_1_jdl\";\n");
        FILE.write("JobType = \"Normal\";\n")
        FILE.write("Executable = \"/bin/hostname\";\n")
        FILE.write("StdOutput  = \"std.out\";\n");
        FILE.write("StdError   = \"std.err\";\n");
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n");
        FILE.write("],\n");

        FILE.write("[\n")
        FILE.write("NodeName=\"Node_2_jdl\";\n");
        FILE.write("file = \"%s/node.jdl\";\n"%(self.get_tmp_dir()))
        FILE.write("],\n");

        FILE.write("[\n")
        FILE.write("NodeName=\"Node_3_jdl\";\n");
        FILE.write("file = \"%s/node.jdl\";\n"%(self.get_tmp_dir()));
        FILE.write("],\n");

        FILE.write("[\n")
        FILE.write("NodeName=\"Node_4_jdl\";\n");
        FILE.write("file = \"%s/node.jdl\";\n"%(self.get_tmp_dir()))
        FILE.write("]\n");

        FILE.write("};\n");
        
        FILE.close()

        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


    # define a parametric jdl
    def set_parametric_jdl(self,filename):
        
        self.info("Define a parametric jdl")

        FILE = open(filename,"w")

        FILE.write("JobType = \"Parametric\";\n")
        FILE.write("Executable = \"/bin/cat\";\n")
        FILE.write("Arguments = \"input_PARAM_.txt\";\n")
        FILE.write("StdInput = \"input_PARAM_.txt\";\n")
        FILE.write("StdOutput = \"output_PARAM_.txt\";\n")
        FILE.write("StdError = \"error_PARAM_.txt\";\n")

        FILE.write("Parameters=10;\n")
        FILE.write("ParameterStart=1;\n")
        FILE.write("ParameterStep=2;\n")

        FILE.write("OutputSandbox = {\"error_PARAM_.txt\",\"output_PARAM_.txt\"};\n")
        FILE.write("InputSandbox = {\"%s/input_PARAM_.txt\"};\n"%(self.MYTMPDIR))
        
        FILE.close()
        
        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))

        for idx in range(1, 10, 2):

            FILE=open("%s/input%i.txt"%(self.MYTMPDIR, idx),"w")
            FILE.write("Hello World !!!")
            FILE.close()
            
    # define a jdl with "Prologue" attribute
    def set_prologue_jdl(self,filename):

        self.info("Define a jdl with prologue attribute")

        FILE = open(filename,"w")

        FILE.write("Executable = \"exe.sh\";\n")
        FILE.write("Arguments = \"Executable Arguments\";\n")
        FILE.write("StdOutput = \"std.out\";\n")
        FILE.write("Prologue = \"prologue.sh\";\n")
        FILE.write("PrologueArguments = \"Prologue Arguments\";\n")
        FILE.write("Environment={\"VAR=TestVariable\"};\n")
        FILE.write("InputSandbox = {\"%s/exe.sh\", \"%s/prologue.sh\"};\n"%(self.MYTMPDIR,self.MYTMPDIR))
        FILE.write("OutputSandbox = {\"std.out\", \"prologue.out\"};\n")

        FILE.close()
        
        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))

        FILE = open("%s/prologue.sh"%(self.MYTMPDIR),"w")

        FILE.write("#!/bin/sh\n")
        FILE.write("echo \"##########################\" >> prologue.out\n")
        FILE.write("echo \"This is the prologue script\" >> prologue.out\n")
        FILE.write("echo \"Start running at `date +%H:%M:%S`\" >> prologue.out\n")
        FILE.write("echo \"My aurguments are: $@\" >> prologue.out\n")
        FILE.write("echo \"Check the value of the environment variable: $VAR\" >> prologue.out\n")
        FILE.write("echo \"Now we 'touch' the file 'prologue'\" >> prologue.out\n")
        FILE.write("touch prologue\n")
        FILE.write("echo \"Finish running at `date +%H:%M:%S`\" >> prologue.out\n")
        FILE.write("echo \"##########################\" >> prologue.out\n")

        FILE.close()

        FILE = open("%s/exe.sh"%(self.MYTMPDIR),"w")

        FILE.write("#!/bin/sh\n")
        FILE.write("echo \"##########################\"\n")
        FILE.write("echo \"This is the executable\"\n")
        FILE.write("echo \"Start running at `date +%H:%M:%S`\"\n")
        FILE.write("echo \"Mine aurguments are: $@\"\n")
        FILE.write("echo \"Check the presence of the file 'prologue'\"\n")
        FILE.write("ls -l prologue\n")
        FILE.write("echo \"Check the value of the environment variable: $VAR\"\n")
        FILE.write("echo \"Now we 'touch' the file 'executable'\"\n")
        FILE.write("touch executable\n")
        FILE.write("echo \"Finish running at `date +%H:%M:%S`\"\n")
        FILE.write("echo \"##########################\"\n")

        FILE.close()

    # define a jdl with "Epilogue" attribute
    def set_epilogue_jdl(self,filename):

        self.info("Define a jdl with epilogue attribute")

        FILE = open(filename,"w")

        FILE.write("Executable = \"exe.sh\";\n")
        FILE.write("Arguments = \"Executable Arguments\";\n")
        FILE.write("StdOutput = \"std.out\";\n")
        FILE.write("Epilogue = \"epilogue.sh\";\n")
        FILE.write("EpilogueArguments = \"Epilogue Arguments\";\n")
        FILE.write("Environment={\"VAR=TestVariable\"};\n")
        FILE.write("InputSandbox = {\"%s/exe.sh\", \"%s/epilogue.sh\"};\n"%(self.MYTMPDIR,self.MYTMPDIR))
        FILE.write("OutputSandbox = {\"std.out\", \"epilogue.out\"};\n")

        FILE.close()

        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))
        
        FILE = open("%s/exe.sh"%(self.MYTMPDIR),"w")

        FILE.write("#!/bin/sh\n")
        FILE.write("echo \"##########################\"\n")
        FILE.write("echo \"This is the executable\"\n")
        FILE.write("echo \"Start running at `date +%H:%M:%S`\"\n")
        FILE.write("echo \"Mine aurguments are: $@\"\n")
        FILE.write("echo \"Check the value of the environment variable: $VAR\"\n")
        FILE.write("echo \"Now we 'touch' the file 'executable'\"\n")
        FILE.write("touch executable\n")
        FILE.write("echo \"Finish running at `date +%H:%M:%S`\"\n")
        FILE.write("echo \"##########################\"\n")

        FILE.close()

        FILE = open("%s/epilogue.sh"%(self.MYTMPDIR),"w")

        FILE.write("#!/bin/sh\n")

        FILE.write("echo \"##########################\"  >> epilogue.out\n")
        FILE.write("echo \"This is the epilogue\"  >> epilogue.out\n")
        FILE.write("echo \"Start running at `date +%H:%M:%S`\" >> epilogue.out\n")
        FILE.write("echo \"Mine aurguments are: $@\" >> epilogue.out\n")
        FILE.write("echo \"Check the value of the environment variable: $VAR\" >> epilogue.out\n")
        FILE.write("echo \"Check the presence of the file 'executable'\" >> epilogue.out\n")
        FILE.write("ls -l executable >> epilogue.out\n")
        FILE.write("echo \"Finish running at `date +%H:%M:%S`\" >> epilogue.out\n")
        FILE.write("echo \"All the jokes are done!\" >> epilogue.out\n")
        FILE.write("echo \"##########################\"  >> epilogue.out\n")

        FILE.close()


    # define a jdl with "Prologue" and "Epilogue"
    def set_prologue_epilogue_jdl(self,filename):

        self.info("Define a jdl with prologue and epilogue attributes")

        FILE = open(filename,"w")

        FILE.write("Executable = \"exe.sh\";\n")
        FILE.write("Arguments = \"Executable Arguments\";\n")
        FILE.write("StdOutput = \"std.out\";\n")
        FILE.write("Prologue = \"prologue.sh\";\n")
        FILE.write("PrologueArguments = \"Prologue Arguments\";\n")
        FILE.write("Epilogue = \"epilogue.sh\";\n")
        FILE.write("EpilogueArguments = \"Epilogue Arguments\";\n")
        FILE.write("Environment={\"VAR=TestVariable\"};\n")
        FILE.write("InputSandbox = {\"%s/exe.sh\", \"%s/epilogue.sh\",\"%s/prologue.sh\"};\n"%(self.MYTMPDIR,self.MYTMPDIR,self.MYTMPDIR))
        FILE.write("OutputSandbox = {\"std.out\", \"prologue.out\", \"epilogue.out\"};\n")
        
        FILE.close()
        
        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))
        
        FILE = open("%s/prologue.sh"%(self.MYTMPDIR),"w")

        FILE.write("#!/bin/sh\n")
        FILE.write("echo \"##########################\" >> prologue.out\n")
        FILE.write("echo \"This is the prologue script\" >> prologue.out\n")
        FILE.write("echo \"Start running at `date +%H:%M:%S`\" >> prologue.out\n")
        FILE.write("echo \"My aurguments are: $@\" >> prologue.out\n")
        FILE.write("echo \"Check the value of the environment variable: $VAR\" >> prologue.out\n")
        FILE.write("echo \"Now we 'touch' the file 'prologue'\" >> prologue.out\n")
        FILE.write("touch prologue\n")
        FILE.write("echo \"Finish running at `date +%H:%M:%S`\" >> prologue.out\n")
        FILE.write("echo \"##########################\" >> prologue.out\n") 
        
        FILE.close()

        FILE = open("%s/exe.sh"%(self.MYTMPDIR),"w")

        FILE.write("#!/bin/sh\n")
        FILE.write("echo \"##########################\"\n")
        FILE.write("echo \"This is the executable\"\n")
        FILE.write("echo \"Start running at `date +%H:%M:%S`\"\n")
        FILE.write("echo \"Mine aurguments are: $@\"\n")
        FILE.write("echo \"Check the presence of the file 'prologue'\"\n")
        FILE.write("ls -l prologue\n")
        FILE.write("echo \"Check the value of the environment variable: $VAR\"\n")
        FILE.write("echo \"Now we 'touch' the file 'executable'\"\n")
        FILE.write("touch executable\n")
        FILE.write("echo \"Finish running at `date +%H:%M:%S`\"\n")
        FILE.write("echo \"##########################\"\n")

        FILE.close()

        FILE = open("%s/epilogue.sh"%(self.MYTMPDIR),"w")

        FILE.write("#!/bin/sh\n")
        
        FILE.write("echo \"##########################\"  >> epilogue.out\n")
        FILE.write("echo \"This is the epilogue\"  >> epilogue.out\n")
        FILE.write("echo \"Start running at `date +%H:%M:%S`\" >> epilogue.out\n")
        FILE.write("echo \"Mine aurguments are: $@\" >> epilogue.out\n")
        FILE.write("echo \"Check the value of the environment variable: $VAR\" >> epilogue.out\n")
        FILE.write("echo \"Check the presence of the files 'prologue' and 'executable'\" >> epilogue.out\n")
        FILE.write("ls -l prologue >> epilogue.out\n")
        FILE.write("ls -l executable >> epilogue.out\n")
        FILE.write("echo \"Finish running at `date +%H:%M:%S`\" >> epilogue.out\n")
        FILE.write("echo \"All the jokes are done!\" >> epilogue.out\n")
        FILE.write("echo \"##########################\"  >> epilogue.out\n")

        FILE.close()

    # define a perusal jdl
    def set_perusal_jdl(self,filename):

        self.create_sleeper()

        self.info("Define a jdl with file perusal enabled")

        FILE = open(filename,"w")

        FILE.write("Executable = \"sleeper.sh\";\n")
        FILE.write("Arguments = \"out.txt\";\n")
        FILE.write("StdOutput = \"std.out\";\n")
        FILE.write("StdError = \"std.err\";\n")
        FILE.write("InputSandbox = \"%s/sleeper.sh\";\n"%(self.MYTMPDIR))
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\",\"out.txt\"};\n")
        FILE.write("PerusalFileEnable = true;\n")

        FILE.close()
        
        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))

    # define a jdl which trigger one shallow resubmission
    def set_shallow_jdl(self,filename):

        self.info("Define a jdl which trigger one shallow resubmission")

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/hostname\";\n")
        FILE.write("StdOutput  = \"std.out\";\n")
        FILE.write("StdError   = \"std.err\";\n")
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n")
        FILE.write("ShallowRetryCount = 2; \n")
        FILE.write("Prologue = \"/bin/false\";\n")

        FILE.close()
        
        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


    # define a jdl which trigger one deep resubmission and save it in filename
    def set_deep_jdl(self,filename):

        self.info("Define a jdl which trigger one deep resubmission")

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/hostname\";\n")
        FILE.write("StdOutput  = \"std.out\";\n")
        FILE.write("StdError   = \"std.err\";\n")
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n")
        FILE.write("RetryCount = 2; \n")
        FILE.write("Epilogue = \"/bin/false\";\n")
        FILE.write("ShallowRetryCount = 0; \n")
        

        FILE.close()
        
        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))

    # define a jdl for parallel a job
    def set_mpi_jdl(self,filename):

        self.info("Define a jdl for mpi job and extract required files from openmpi.tar.gz")

        self.run_command("tar xf openmpi.tar.gz -C %s"%(self.MYTMPDIR))

        FILE = open(filename,"w")

        FILE.write("CpuNumber=1;\n")
        FILE.write("Executable = \"openmpi-wrapper.sh\";\n")
        FILE.write("Arguments=\"hello\";\n")
        FILE.write("StdOutput  = \"hello.out\";\n")
        FILE.write("StdError   = \"hello.err\";\n")
        FILE.write("OutputSandbox = {\"hello.out\",\"hello.err\"};\n")
        FILE.write("InputSandbox = {\"%s/openmpi-wrapper.sh\",\"%s/hello.c\",\"%s/Makefile\"};\n"%(self.MYTMPDIR,self.MYTMPDIR,self.MYTMPDIR))
        FILE.write("Requirements = Member (\"OPENMPI\",other.GlueHostApplicationSoftwareRunTimeEnvironment);\n")

        FILE.close()
        
        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


    #define a jdl which triggers reschedule
    def set_feedback_jdl(self,filename):

        self.info("Define a jdl which triggers reschedule")

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/sleep\";\n")
        FILE.write("Arguments = \"3\";\n")
        FILE.write("Retrycount = 0;\n")
        FILE.write("Shallowretrycount = 0;\n")
        FILE.write("StdError = \"stderr.log\";\n")
        FILE.write("StdOutput = \"stdout.log\";\n")
        FILE.write("OutputSandbox = {\"stderr.log\", \"stdout.log\"};\n")
        FILE.write("EnableWMSFeedback = true;\n")

        FILE.close()

        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))

    #define a jdl for gangmathing
    def set_gang_jdl(self,filename):

        self.info("Define a jdl with data requirements")

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/ls\";\n")
        FILE.write("StdError = \"stderr.log\";\n")
        FILE.write("StdOutput = \"stdout.log\";\n")
        FILE.write("OutputSandbox = {\"stderr.log\", \"stdout.log\"};\n")
        FILE.write("SErequirements = anyMatch(other.storage.CloseSEs, target.GlueSAStateAvailableSpace > 20);\n")
        FILE.write("CErequirements = other.GlueCEStateStatus == \"Production\" && other.GlueCEInfoTotalCPUs >= 2;\n")

        FILE.close()

        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


    #define a jdl with data requirements
    def set_data_req_jdl(self,filename,VO,LFC,DIR):

        self.info("Define a jdl for gangmatching")

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/cat\";\n")
        FILE.write("StdError = \"std.err\";\n")
        FILE.write("StdOutput = \"std.out\";\n")
        FILE.write("FuzzyRank = true;\n")
        FILE.write("OutputSandbox = {\"std.err\", \"std.out\"};\n")
        FILE.write("Requirements = true;\n")
        FILE.write("DataAccessProtocol = \"gsiftp\";\n")
        FILE.write("RetryCount = 1;\n")
        FILE.write("ShallowRetryCount = 2;\n")
        FILE.write("VirtualOrganisation = \"%s\";\n"%(VO))
        FILE.write("DataRequirements = {\n")
        FILE.write("[\n")
        FILE.write("DataCatalogType = \"DLI\";\n")
        FILE.write("DataCatalog = \"http://%s:8085\";\n"%(LFC))
        FILE.write("InputData = {\"lfn:%s/file1.txt\",\"lfn:%s/file2.txt\"};\n"%(DIR,DIR))
        FILE.write("]\n")
        FILE.write("};\n")

        FILE.close()

        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


    # define a script which write 100 messages, one every 15sec
    def create_sleeper(self):

        self.info("Define the sleeper script, which write 100 messages one every 15sec")

        FILE = open("%s/sleeper.sh"%(self.MYTMPDIR),"w")

        FILE.write("#!/bin/sh\n")

        FILE.write("echo \"This is sleeper\"\n")
        FILE.write("echo \"This is sleeper\" > $1\n")

        FILE.write("for((i=1;i<=100;i++))\n")
        FILE.write("do \n")
        FILE.write("    echo \"message $i\" >> $1 \n")
        FILE.write("    sleep 15 \n")
        FILE.write("done \n")

        FILE.write("echo \"Stop sleeping!\" >> $1 \n")
        FILE.write("echo \"Stop sleeping!\" \n")

        FILE.close()
        
        self.dbg("The saved script is:\n%s"%(commands.getoutput("cat %s/sleeper.sh"%(self.MYTMPDIR))))

    # add the given couple (att, value) to the jdl (string value)
    def add_jdl_attribute(self, att, value):
   
        self.info("Add the attribute %s=\"%s\" to jdl"%(att,value))
        
        FILE=open(self.JDLFILE,"a")
        
        FILE.write("%s=\"%s\";\n"%(att,value))

        FILE.close()
        
        self.dbg("The new saved jdl is:\n%s"%(commands.getoutput("cat %s"%(self.JDLFILE))))


    # add the given couple (att, value) to the jdl (not string value)
    def add_jdl_general_attribute(self, att, value):

        self.info("Add the attribute %s=%s to jdl"%(att,value))

        FILE=open(self.JDLFILE,"a")

        FILE.write("%s=%s;\n"%(att,value))

        FILE.close()

        self.dbg("The new saved jdl is:\n%s"%(commands.getoutput("cat %s"%(self.JDLFILE))))


    # change value of the given attribute to the jdl (string value)
    def change_jdl_attribute(self, att, value):

        self.info("Change the value of the attribute %s to %s. "%(att,value))

        FILE=open(self.JDLFILE,"r")
        lines=FILE.readlines()
        FILE.close()

        for line in lines:
            if line.find(att)!=-1:
                lines[lines.index(line)]="%s=%s;\n"%(att,value)

        FILE=open(self.JDLFILE,"w")
        FILE.writelines(lines)
        FILE.close()

        self.dbg("The new saved jdl is:\n%s"%(commands.getoutput("cat %s"%(self.JDLFILE))))

    # add given requirements to jdl
    def set_requirements(self, requirements):
        
        self.info("Add the attribute Requirements=%s to jdl"%(requirements))
        
        FILE=open(self.JDLFILE,"a")
        
        FILE.write("Requirements=%s;\n"%(requirements))
        
        FILE.close()
        
        self.dbg("The new saved jdl is:\n%s"%(commands.getoutput("cat %s"%(self.JDLFILE))))

    # force the destination ce for parallel jobs
    def set_mpi_destination_ce(self,filename, destination_ce):
        
        self.set_requirements("Member (\"OPENMPI\",other.GlueHostApplicationSoftwareRunTimeEnvironment) && RegExp(\"%s\",other.GlueCEUniqueID);"%(destination_ce))

    # force the destination ce
    def set_destination_ce(self,filename, destination_ce):
        
        self.set_requirements("RegExp(\"%s\",other.GlueCEUniqueID)"%(destination_ce))


    ############################################
    # define configuration file and save it in "filename"
    # --> require: WMS
    # --> require: VO
    # --> require: LB
    # --> require: DEFAULTREQ
    def set_conf(self,filename):

        self.info("Define the configuration file")

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

        self.dbg("The saved configuration file is:\n%s"%(commands.getoutput("cat %s"%(filename))))

    # ... get user passwd
    # --> set PASS
    def set_pwd(self):

       print ("")
       self.PASS=getpass.getpass("Enter the user proxy password:")


    # ... create proxy file with validity "valid_period" (default 24:00)
    def set_proxy(self,proxy,valid_period="24:00",role=""):

        if self.ROLE=='':
            self.info("Initializing proxy file with voms %s, valid for %s"%(self.VO,valid_period))
            OUTPUT=commands.getstatusoutput("echo %s | voms-proxy-init -voms %s -verify -valid %s -bits 1024 -pwstdin -out %s "%(self.PASS,self.VO,valid_period,proxy))
        else:
            self.info("Initializing proxy file with voms %s, role %s, valid for %s"%(self.VO,self.ROLE,valid_period))
            OUTPUT=commands.getstatusoutput("echo %s | voms-proxy-init -voms %s:/%s/Role=%s -verify -valid %s -bits 1024 -pwstdin -out %s "%(self.PASS,self.VO,self.VO,self.ROLE,valid_period,proxy))

        if OUTPUT[0] == 0 :
            self.dbg("voms-proxy-init output: %s"%(OUTPUT[1]))
            os.putenv("X509_USER_PROXY",proxy)
            self.info("Set environment variable X509_USER_PROXY to %s"%(proxy))
        else:
            logging.critical("Failed to create a valid user proxy")
            self.error("voms-proxy-init output : %s"%(OUTPUT[1]))
            self.exit_failure("Failed to create a valid user proxy")

    
    # Run command "args", if "fail" is set we expect a command failure (ret code != 0)
    # If command fails (or if "fail"=1 and it not fails), exit with failure 
    # returns command's output
    def run_command(self,args,fail=0):

        self.info ("Run command: %s"%(args))

        OUTPUT=commands.getstatusoutput(args)

        if fail==0 and OUTPUT[0]!=0 :
            logging.critical('Command %s failed.', args)
            self.error('Command %s failed. Failure message: %s'%(args,OUTPUT[1]))
            self.exit_failure ("%s failed"%(args))
        elif fail==1 and OUTPUT[0]==0:
            logging.critical('Command %s not failed as expected.',args)
            self.error('Command %s not failed as expected. Command output: %s'%(args,OUTPUT[1]))
            self.exit_failure ("%s not failed as expected."%(args))
            
        self.dbg("Command output:\n%s"%(OUTPUT[1]))
        
        if fail==0:
            self.info(" -> Command success")
        else:
            self.info(" -> Command successfully failed")  

        return OUTPUT[1]

    # Run command "args", if "fail" is set we expect a command failure (ret code != 0)
    # If command fails (or if "fail"=1 and it not fails), raise a RunCommandError exception
    # returns command's output
    def run_command_continue_on_error(self,args,fail=0):
 
        self.info ("Run command: %s"%(args))

        OUTPUT=commands.getstatusoutput(args)

        if fail==0 and OUTPUT[0]!=0 :
            logging.critical("Command %s failed !!!!",args)
            self.error('Command %s failed. Failure message: %s'%(args,OUTPUT[1]))
            raise RunCommandError(args,OUTPUT[1])
            return 1
        elif fail==1 and OUTPUT[0]==0:
            logging.critical("Command %s not failed as expected!!!!",args)
            self.error('Command %s not failed as expected. Command output: %s'%(args,OUTPUT[1]))
            raise RunCommandError(args,OUTPUT[1])
            return 1            

        self.dbg("Command output:\n%s"%(OUTPUT[1]))

        if fail==0:
            self.info(" -> Command success")
        else:
            self.info(" -> Command successfully failed")  

        return OUTPUT[1]



    # Wait until job "jobid" is done or raise TimeOutError exception if time is out 
    def wait_until_job_finishes(self,jobid):

        self.info("Wait until job %s finishes ..."%(jobid))

        self.info("Iterating %s times and each time wait for %s secs"%(self.NUM_STATUS_RETRIEVALS,self.SLEEP_TIME))

        counter=0

        while self.job_is_finished(jobid) == 0 :

            if counter >= int(self.NUM_STATUS_RETRIEVALS) :
                self.error("Timeout reached while waiting the job %s to finish"%(jobid))
                raise TimeOutError("","Timeout reached while waiting the job %s to finish"%(jobid))
               
            self.info("Job's %s status is %s ... sleeping %s seconds ( %s/%s )"%(jobid,self.JOBSTATUS,self.SLEEP_TIME,counter,self.NUM_STATUS_RETRIEVALS))
            time.sleep(int(self.SLEEP_TIME))
            counter=counter+1


    # Wait until job is transfered to CE or raise TimeOutError exception if time is out
    def wait_until_job_transfered(self,jobid):

        self.info("Wait until job %s transfered to CE ..."%(jobid))

        self.info("Iterating %s times and each time wait for %s secs"%(self.NUM_STATUS_RETRIEVALS,self.SLEEP_TIME))

        counter=0

        while self.job_is_transfered(jobid) == 0 :

            if counter >= int(self.NUM_STATUS_RETRIEVALS) :
                self.error("Timeout reached while waiting the job %s to transfered to CE"%(jobid))
                raise TimeOutError("","Timeout reached while waiting the job %s to transfered to CE"%(jobid))

            self.info("Job's %s status is %s ... sleeping %s seconds ( %s/%s )"%(jobid,self.JOBSTATUS,self.SLEEP_TIME,counter,self.NUM_STATUS_RETRIEVALS))
            time.sleep(int(self.SLEEP_TIME))
            counter=counter+1


    # ... delegate proxy and (re-)define DELEGATION_OPTIONS
    # --> set: DELEGATION_OPTIONS
    def define_delegation(self):

        self.DELEGATION_OPTIONS="-d del_%s"%(self.ID)
        self.info ("Delegating proxy ...")
        self.run_command("glite-wms-job-delegate-proxy %s -c %s"%(self.DELEGATION_OPTIONS,self.CONFIG_FILE))


    ############### JOB UTILS ####################################

    # submit a job and return JOBID
    # Raise RunCommandError exception if submission fails
    def submit_job(self):

        self.info("Submit a job")

        JOBID=self.run_command_continue_on_error ("glite-wms-job-submit %s --config %s --nomsg --output %s %s"%(self.DELEGATION_OPTIONS,self.CONFIG_FILE,self.JOBIDFILE,self.JDLFILE))

        self.info("Job submitted successfuly. Returned JOBID: %s"%(JOBID))

        # wait until job arrives to wm, needs because there is a bug in the wmproxy.
        time.sleep(5)

        return JOBID


    #
    def get_cream_jobid(self,jobid):

       self.info("Get CREAM jobid")

       cream_jobid=""

       output=self.run_command_continue_on_error("glite-wms-job-logging-info -v 2 --event Transfer %s"%(jobid)).split("\n")

       for line in output:
           if line.find("Dest jobid")!=-1 and line.find("https://")!=-1:
               cream_jobid=line.split("=")[1].strip(" \n\t")

       return cream_jobid

    #
    def get_cream_jdl(self,cream_jobid):

       self.info("Get CREAM jdl")

       jdl=""

       output=self.run_command_continue_on_error("glite-ce-job-status -L 2  %s"%(cream_jobid)).split("\n")

       for line in output:
           if line.find("JDL")!=-1 :
               jdl=line.strip(" \n\t")

       return jdl

    # Extract the "status" of the job "jobid"
    # --> set JOBSTATUS
    def job_status(self,jobid):

        self.JOBSTATUS="Unknown"

        self.info ("Check job's status...")

        try:
            OUTPUT=self.run_command_continue_on_error ("glite-wms-job-status --verbosity 0 %s"%(jobid))
            for line in OUTPUT.splitlines():
                if line.split(":",1)[0]=="Current Status":
                    self.JOBSTATUS=line.split(":",1)[1].strip()
                    break
          
        except RunCommandError, e :
            self.warn("I'm not able to retrieve job %s status. Error is %s"%(jobid,e.message))
        
        self.info('Job %s status is %s'%(jobid,self.JOBSTATUS))

        return 0

    # Return the "status reason" of the job "jobid"
    def get_job_status_reason(self,jobid):

        self.info ("Check job's status...")

        reason='Unknown'

        try:
            OUTPUT=self.run_command_continue_on_error ("glite-wms-job-status %s"%(jobid))
            for line in OUTPUT.splitlines():
                if line.split(":",1)[0]=="Status Reason":
                    reason=line.split(":",1)[1].strip()
                    break

        except RunCommandError, e :
            self.warn("I'm not able to retrieve job %s status reason. Error is %s"%(jobid,e.message))

        self.info('Job %s status reason is %s'%(jobid,reason))

        return reason

    # Check if job described in JOBIDFILE is finished
    # returns 0 if job is not finished
    # returns 1 if job is DoneOK
    # returns 2 if Aborted
    # returns 3 if jobs is Cancelled
    # returns 4 if Done (exit Code != 0)
    # returns 5 if jobs is Cleared
    def job_is_finished(self,jobid):

        self.job_status(jobid)
        
        self.info('The status of the job %s is: %s'%(jobid,self.JOBSTATUS))

        if self.JOBSTATUS.find('Aborted') != -1 :
            return 2
        elif self.JOBSTATUS.find('Cancelled') !=-1 :
            return 3
        elif self.JOBSTATUS.find('(Exit Code !=0)') != -1 :
            return 4
        elif self.JOBSTATUS.find('Cleared') != -1 :
            return 5
        elif self.JOBSTATUS.find('Done (Success)') != -1 or self.JOBSTATUS.find('Done(Success)') != -1 :
            return 1
        elif self.JOBSTATUS.find('Done (Failed)') != -1 or self.JOBSTATUS.find('Done(Failed)') != -1 :
            return 6
        else:
            self.info('Job %s is not finished yet'%(jobid))
            return 0


    # Check if job described in JOBIDFILE is transfered
    # returns 0 if job is not transfered
    # returns 1 if job is transfered
    def job_is_transfered(self,jobid):

        self.job_status(jobid)

        self.info('The status of the job %s is: %s'%(jobid,self.JOBSTATUS))

        if self.JOBSTATUS.find('Submitted') != -1 :
            self.info('Job %s is not transfered yet'%(jobid))
            return 0
        elif self.JOBSTATUS.find('Ready') !=-1 :
            self.info('Job %s is not transfered yet'%(jobid))
            return 0
        elif self.JOBSTATUS.find('Waiting') !=-1 :
            self.info('Job %s is not transfered yet'%(jobid))
            return 0
        else:
            self.info('Job %s is transfered'%(jobid))
            return 1


    # store jobIDs from the file "filename" into a list
    def load_job_ids(self,filename):

        jobids=[]

        FILE = open(filename,"r")

        lines = FILE.readlines()

        for line in lines :
            if line.find("http")==1: # it is a valid jobid
                jobids.append(string.strip(line))

        FILE.close()

        return jobids


    def log_error(self,msg):
        
        FILE=open("%s/errors.log"%(self.MYTMPDIR),"a")
        
        FILE.write("%s\n"%msg)
        
        FILE.close()

    def log_traceback(self,msg):

        FILE=open("%s/traceback_errors.log"%(self.MYTMPDIR),"a")

        FILE.write("%s\n"%msg)

        FILE.close()

    def show_tests(self,tests):

        print ""
        print "Available %s tests"%(len(tests))
        print ""

        for test in tests:
            print test
       
        print ""


    def parse_test_numbers(self):

        final=[]

        if self.SUBTESTS!='' :

            tests=self.SUBTESTS.split(',')

            for test in tests:

                if test.find('-')!=-1:
    
                    test=test.split('-')

                    for x in range(int(test[0]),int(test[1])+1):
                        final.append(x)

                else:
                    final.append(int(test))

        final.sort()

        self.ENABLEDTESTS=final


    def check_test_enabled(self,test):

        for x in self.ENABLEDTESTS:
            if x==test:
                return 1

        return 0


    def get_target_ces(self):

        CES=[]
        NAMES=[]

        FILE = open(self.CONF,"r")
        lines=FILE.readlines()
        FILE.close()

        for line in lines:

           if line.find("=>")!=-1 and line.find("#")==-1:

              line=string.strip(line)
              ret=line.split("=>",1)

              NAMES.append(ret[0].strip(" \n\t"))
              CES.append(ret[1].strip(" \n\t"))

        if len(CES)>0:
            self.EXTERNAL_REQUIREMENTS=1

        return NAMES,CES


    ###########################################################################

    def prepare(self,args,tests):

        try:
            opts,args = getopt.getopt(args,'hlvd:ic:nW:V:L:C:j:st:r:')
        except getopt.GetoptError,err:
            print ''
            print str(err)
            self.usage(self.CMD)
            sys.exit(0)

        # Test ID
        self.ID=strftime("%Y%m%d%H%M%S")

        # source default configuration file: wms_command.conf if exists 
        if os.path.isfile(self.CONF):
            self.load_configuration(self.CONF)   
        
        # Read command line options (they overwrite values found in default configuration file) 
        for option,value in opts:

            if option=="-h":
                self.usage(self.CMD)
                sys.exit(0)
            elif option=="-v":
                self.VERBOSE=1
            elif option=="-d":
                if value=="1":
                    self.LOG_LEVEL='WARNING'
                elif value=="2":
                    self.LOG_LEVEL='INFO'
                else:
                    self.LOG_LEVEL='DEBUG'
            elif option=="-l":
                self.LOG=1
            elif option=="-i":
                self.NOPROXY=0
            elif option=="-n":
                self.NAGIOS=1
            elif option=="-W":
                self.WMS=value
            elif option=="-c":
                self.USER_CONF=1
                self.CONF=value
            elif option=="-C":
                self.CE=value
            elif option=="-L":
                self.LB=value
            elif option=="-V":
                self.VO=value
            elif option=="-j":
                self.EXTERNAL_JDL=1
                self.EXTERNAL_JDL_FILE=value
            elif option=="-s":
                self.show_tests(tests)
                sys.exit(0)
            elif option=="-t":
                self.RUN_ALL=0
                self.SUBTESTS=value
                self.parse_test_numbers()
            elif option=="-r":
                self.DEFAULTREQ=value
                self.EXTERNAL_REQUIREMENTS=1

        self.START_TIME=strftime("%H:%M:%S")     

        # source users specific configuration values (they overwrite command line option values)
        if self.USER_CONF==1 and os.path.isfile(self.CONF):
            self.load_configuration(self.CONF)

     
        if self.LOG_LEVEL=='WARNING':
            self.NUM_LOG_LV=30
        elif self.LOG_LEVEL=='INFO':
            self.NUM_LOG_LV=20
        else:
            self.NUM_LOG_LV=10

        # Check if required arguments are set 
        if len(self.WMS)==0  or len(self.LB)==0 or len(self.VO)==0 :
            self.exit_failure("Required argument is not set")

        # ... create temporary directory
        self.MYTMPDIR="%s/WMSService-Test_%s"%(os.getcwd(),self.ID)

        try:
            os.mkdir(self.MYTMPDIR,0755)
        except os.error, e:
            self.exit_failure("Fail to create temporary directory")
            return 0
          
        # ... create log file
        if self.LOG == 1 :
            self.TESTLOGFILE='WMSService-TS_%s.log'%(self.ID)
        else: # write the logfile in the working directory just for debug
            self.TESTLOGFILE='%s/WMSService-TS_%s.log'%(self.MYTMPDIR, self.ID)
        
    
        logging.basicConfig(filename='%s'%(self.TESTLOGFILE),format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S',level=self.NUM_LOG_LV)

        self.info("Start log file for test %s"%(self.ID)) 

        self.myecho ("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        self.myecho ("+ TestSuite of the WMS Service                       ")
        self.myecho ("+ Description: %s "%(self.DESCRIPTION))
        self.myecho ("+++++++++++++++++++++++++++++++++++++++++++++++++++++")

        # ... define common directory and file names
        self.JOB_OUTPUT_DIR="%s/jobOutput"%(self.MYTMPDIR)

        os.mkdir("%s"%(self.JOB_OUTPUT_DIR))

        self.LOGFILE="%s/log.txt"%(self.MYTMPDIR)
        self.OUTPUTFILE="%s/output.txt"%(self.MYTMPDIR)
        self.JOBIDFILE="%s/job.id"%(self.MYTMPDIR)
        self.PROXY="%s/proxy.file"%(self.MYTMPDIR)
        self.TMPFILE="%s/file.tmp"%(self.MYTMPDIR)
        self.CONFIG_FILE="%s/wms.conf"%(self.MYTMPDIR)

        if self.EXTERNAL_JDL == 0:
            self.JDLFILE="%s/example.jdl"%(self.MYTMPDIR)
        else :
            os.system("cp %s %s/%s"%(self.EXTERNAL_JDL_FILE,self.MYTMPDIR,self.EXTERNAL_JDL_FILE))
            self.JDLFILE="%s/%s"%(self.MYTMPDIR,self.EXTERNAL_JDL_FILE)


        # Create default jdl and config file
        if self.EXTERNAL_JDL == 0:
            self.set_jdl(self.JDLFILE)

        self.set_conf(self.CONFIG_FILE)

        # Create proxy if required

        if self.NOPROXY != 1:
            self.set_pwd()
            self.set_proxy(self.PROXY)
        else:
            voms_info=commands.getstatusoutput("voms-proxy-info -timeleft")

            if voms_info[1].isdigit() == False :
                self.set_proxy(self.PROXY) # try to create a proxy without pwd
                voms_info=commands.getstatusoutput("voms-proxy-info -timeleft")
                if voms_info[1].isdigit() == False :
                    self.exit_failure("I don't find neither create any valid proxy")


