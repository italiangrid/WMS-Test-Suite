import os
import sys
import time
import commands
import string
import shlex
import subprocess

import logging

from Exceptions import *
from time import strftime,gmtime

class Test_utils:

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self.ID=''
        self.NUM_STATUS_RETRIEVALS=120
        self.SLEEP_TIME=30
        self.DELEGATION_OPTIONS=''
        self.DEFAULTREQ=''
        self.CONF="wms-command.conf"
        self.CE=''
        self.WMS=''
        self.VO=''
        self.LB=''
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
        self.JOBSTATUS=''
        self.MYPROXYSERVER=''
        self.TESTLOGFILE='' 
        self.logger=''
        self.WMS_USERNAME=''
        self.WMS_PASSWORD=''
        self.YAIM_FILE=''
        self.ROLE=''
        self.open_ssh=0
	self.LFC=''
        self.SE=''
  
    ###########################################################################

    ###########################################################################


    def return_object(self):
       return self;

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

    def get_WMS(self):
        return self.WMS

    def get_LB(self):
        return self.LB

    def get_MYPROXY_SERVER(self):
        return self.MYPROXYSERVER
    
    def get_log_file(self):
        return self.LOGFILE

    def get_job_output_dir(self):
        return self.JOB_OUTPUT_DIR

    def get_PROXY(self):
        return self.PROXY

    
    """
    def get_NOPROXY(self):
        return self.NOPROXY

    def has_external_jdl(self):
        return self.EXTERNAL_JDL

    def get_user_CE(self):
        return self.CE

    def get_current_test(self):
        return self.CURRENTTEST
        
    def is_all_enabled(self):
        return self.RUN_ALL

    """

    def log_info(self,msg,level="INFO"):

        print '*%s* %s'%(level,msg)

        self.external_log(msg) 


    def console_log(self,msg):
 
        self.log_info(msg)

        sys.stderr.write("\n %s \n"%(msg))
 

    def external_log(self,msg):

        self.logger.write("%s : %s\n"%(strftime("%d/%m/%Y - %H:%M:%S", gmtime()),msg))


    def close_logger(self):

        if self.logger!='': 
         self.logger.close()

    # remove a file only if exists
    def remove(self,filename):
        
        self.log_info("Remove file %s..."%(filename),'DEBUG')

        if os.path.isfile(filename):
            os.unlink(filename)


    #
    # Accept only the following attributes (everthing else is ignored):
    #
    # WMS:                    WMS hostname
    # LB:                     LB hostname
    # VO:                     User VO
    # MYPROXYSERVER:          MyProxyServer hostname
    # LOG_LEVEL:              Log level
    # DEFAULTREQ:             Default requirements
    # NUM_STATUS_RETRIEVALS:  Number of retrievals before to stop test (timeout)
    # SLEEP_TIME:             Seconds before the next status check
    # JDLFILE:
    # DELEGATION_OPTIONS
    # WMS_USERNAME
    # WMS_PASSWORD
    # YAIM_FILE
    # PROXY_PASSWORD 
    # ROLE: VOMS ROLE
    # SE
    # LFC  
    # ISB_DEST_HOSTNAME
    # ISB_DEST_USERNAME
    # ISB_DEST_PASSWORD    
    def load_configuration(self,conf):

       attributes=['WMS','JDLFILE','LB','VO','MYPROXYSERVER','PROXY_PASSWORD','WMS_USERNAME','WMS_PASSWORD','YAIM_FILE','LOG_LEVEL','DEFAULTREQ','NUM_STATUS_RETRIEVALS','SLEEP_TIME','DELEGATION_OPTIONS','ROLE','SE','LFC','ISB_DEST_HOSTNAME','ISB_DEST_USERNAME','ISB_DEST_PASSWORD','OSB_DEST_HOSTNAME','OSB_DEST_USERNAME','OSB_DEST_PASSWORD']

       FILE = open(conf,"r")
       lines=FILE.readlines()
       FILE.close()

       for line in lines:

           if line.isspace()==False and line.find("#")==-1:
              line=string.strip(line)
              ret=line.split("=",1)

              try:
                   attributes.index(ret[0])
     
                   if ret[0].find('DEFAULTREQ')==-1: 
                      ret[1]=ret[1].strip(" '\n\t\"")
                   else:
                      ret[1]=ret[1].strip(" '\n\t")
                   
                   setattr(self,'%s'%(ret[0]),ret[1])
                   print '*DEBUG* Set configuration value: %s to value: %s'%(ret[0],ret[1])
              except ValueError:
                   pass


    def prepare_tests(self,title):

        # Test ID
        self.ID=strftime("%Y%m%d%H%M%S")

        #load test configuration parameters from file conf.py
        self.load_configuration("%s/lib/conf.py"%os.getcwd())   
      
        # Check if required arguments are set 
        if len(self.WMS)==0  or len(self.LB)==0 or len(self.VO)==0 :
            raise GeneralError("","Required arguments (WMS,LB,VO) are not set")

        # ... create temporary directory
        if title.find("WMS-command")!=-1:
	     self.MYTMPDIR="%s/WMSCLI-%s_%s"%(os.getcwd(),title,self.ID)
	else:
	     self.MYTMPDIR="%s/WMSService-%s_%s"%(os.getcwd(),title,self.ID)

        try:
             os.mkdir(self.MYTMPDIR,0755)
        except os.error, e:
             raise GeneralError("","Fail to create temporary directory")
             return 0

        # ... define common directory and file names
        self.JOB_OUTPUT_DIR="%s/jobOutput"%(self.MYTMPDIR)

        os.mkdir("%s"%(self.JOB_OUTPUT_DIR))

        self.LOGFILE="%s/log.txt"%(self.MYTMPDIR)
        self.OUTPUTFILE="%s/output.txt"%(self.MYTMPDIR)
        self.JOBIDFILE="%s/job.id"%(self.MYTMPDIR)
        self.PROXY="%s/proxy.file"%(self.MYTMPDIR)
        self.TMPFILE="%s/file.tmp"%(self.MYTMPDIR)
        self.CONFIG_FILE="%s/wms.conf"%(self.MYTMPDIR)

        if title.find("WMS-command")!=-1:
	    self.TESTLOGFILE="WMSCLI-%s_%s.log"%(title,self.ID)
	else:
            self.TESTLOGFILE="WMSService-%s_%s.log"%(title,self.ID)

        self.logger=open(self.TESTLOGFILE,'a')

        self.external_log ("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        self.external_log ("+ Description: %s "%(title))
        self.external_log ("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
   
        if len(self.JDLFILE)==0:
            self.JDLFILE="%s/example.jdl"%(self.MYTMPDIR)

        # Create default jdl and config file
        self.set_jdl(self.JDLFILE)
        self.set_conf(self.CONFIG_FILE)

        return self.JDLFILE      


    ############################################
    # define configuration file and save it in "filename"
    # --> require: WMS
    # --> require: VO
    # --> require: LB
    # --> require: DEFAULTREQ
    def set_conf(self,filename):

        self.log_info('Define the configuration file')
        
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

        self.log_info('The saved configuration file is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')
               
      
    """ 
   

    """ 
 

    ###############################################################################
    ###########################   START JDL METHODS   #############################
    ###############################################################################

    # define a simple jdl and save it in "filename"
    def set_jdl(self,filename):

        self.log_info('Define a simple jdl')

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/hostname\";\n")
        FILE.write("StdOutput  = \"std.out\";\n")
        FILE.write("StdError   = \"std.err\";\n")
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n")
        FILE.write("ShallowRetryCount = 3;\n")

        FILE.close()
       
        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')

   
    # define a 15 minutes long jdl and save it in "filename"
    def set_long_jdl(self,filename):

        self.log_info('Define a 15 minutes long jdl file')

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/sleep\";\n")
        FILE.write("Arguments = \"900\";\n")

        FILE.close()
        
        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')

   
    # define a jdl with ISB and save it in "filename"
    def set_isb_jdl(self,filename):

        self.log_info('Define a jdl with ISB')

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/ls\";\n")
        FILE.write("Arguments = \"-la\";\n")
        FILE.write("StdOutput = \"std.out\";\n")
        FILE.write("StdError = \"std.err\";\n")
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n")
        FILE.write("ShallowRetryCount = 2;\n")
        FILE.write("InputSandbox = \"%s\";\n"%(filename))

        FILE.close()

        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')
    

    # define a dag jdl
    def set_dag_jdl(self,filename):

        self.log_info('Define a DAG jdl')

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
        
        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')


    #define a collection jdl
    def set_collection_jdl(self,filename):

        self.log_info('Define a collection jdl')

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

        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')


    #define a collection jdl
    def set_collection_external_jdls(self,filename):

        self.log_info('Define a collection jdl')

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

        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')


    # define a parametric jdl
    def set_parametric_jdl(self,filename):
        
        self.log_info('Define a parametric jdl')

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
        
        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')

        for idx in range(1, 10, 2):

            FILE=open("%s/input%i.txt"%(self.MYTMPDIR, idx),"w")
            FILE.write("Hello World !!!")
            FILE.close()
            

    # define a jdl with "Prologue" attribute
    def set_prologue_jdl(self,filename):

        self.log_info('Define a jdl with prologue attribute')

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
        
        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')

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

        self.log_info('Define a jdl with epilogue attribute')

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

        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')
        
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

        self.log_info('Define a jdl with prologue and epilogue attributes')

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
        
        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')
        
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

        self.log_info('Define a jdl with file perusal enabled')

        FILE = open(filename,"w")

        FILE.write("Executable = \"sleeper.sh\";\n")
        FILE.write("Arguments = \"out.txt\";\n")
        FILE.write("StdOutput = \"std.out\";\n")
        FILE.write("StdError = \"std.err\";\n")
        FILE.write("InputSandbox = \"%s/sleeper.sh\";\n"%(self.MYTMPDIR))
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\",\"out.txt\"};\n")
        FILE.write("PerusalFileEnable = true;\n")

        FILE.close()
        
        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')


    # define a jdl which trigger one shallow resubmission
    def set_shallow_jdl(self,filename):

        self.log_info('Define a jdl which trigger one shallow resubmission')

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/hostname\";\n")
        FILE.write("StdOutput  = \"std.out\";\n")
        FILE.write("StdError   = \"std.err\";\n")
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n")
        FILE.write("ShallowRetryCount = 2; \n")
        FILE.write("Prologue = \"/bin/false\";\n")

        FILE.close()
        
        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')


    # define a jdl which trigger one deep resubmission and save it in filename
    def set_deep_jdl(self,filename):

        self.log_info('Define a jdl which trigger one deep resubmission')

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/hostname\";\n")
        FILE.write("StdOutput  = \"std.out\";\n")
        FILE.write("StdError   = \"std.err\";\n")
        FILE.write("OutputSandbox = {\"std.out\",\"std.err\"};\n")
        FILE.write("RetryCount = 2; \n")
        FILE.write("Epilogue = \"/bin/false\";\n")
        FILE.write("ShallowRetryCount = 0; \n")
        
        FILE.close()
        
        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')


    # define a jdl for parallel a job
    def set_mpi_jdl(self,filename):

        self.log_info('Define a jdl for mpi job and extract required files from openmpi.tar.gz')

        self.run_command("tar xf testsuites/WMS-service/openmpi.tar.gz -C %s"%(self.MYTMPDIR))

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
        
        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')


    #define a jdl which triggers reschedule
    def set_feedback_jdl(self,filename):

        self.log_info('Define a jdl which triggers reschedule')

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/sleep\";\n")
        FILE.write("Arguments = \"3600\";\n")
        FILE.write("Retrycount = 0;\n")
        FILE.write("Shallowretrycount = 0;\n")
        FILE.write("StdError = \"stderr.log\";\n")
        FILE.write("StdOutput = \"stdout.log\";\n")
        FILE.write("OutputSandbox = {\"stderr.log\", \"stdout.log\"};\n")
        FILE.write("EnableWMSFeedback = true;\n")

        FILE.close()

        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')


    #define a jdl for gangmathing
    def set_gang_jdl(self,filename):

        self.log_info('Define a jdl with data requirements')

        FILE = open(filename,"w")

        FILE.write("Executable = \"/bin/ls\";\n")
        FILE.write("StdError = \"stderr.log\";\n")
        FILE.write("StdOutput = \"stdout.log\";\n")
        FILE.write("OutputSandbox = {\"stderr.log\", \"stdout.log\"};\n")
        FILE.write("SErequirements = anyMatch(other.storage.CloseSEs, target.GlueSAStateAvailableSpace > 20);\n")
        FILE.write("CErequirements = other.GlueCEStateStatus == \"Production\" && other.GlueCEInfoTotalCPUs >= 2;\n")

        FILE.close()

        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')


    #define a jdl with data requirements
    def set_data_req_jdl(self,filename,VO,LFC,DIR):

        self.log_info('Define a jdl for gangmatching')

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

        self.log_info('The saved jdl is:\n%s'%(commands.getoutput("cat %s"%(filename))),'DEBUG')


    # define a script which write 100 messages, one every 15sec
    def create_sleeper(self):

        self.log_info('Define the sleeper script, which write 100 messages one every 15sec')

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
        
        self.log_info('The saved script is:\n%s'%(commands.getoutput("cat %s/sleeper.sh"%(self.MYTMPDIR))),'DEBUG')


    # add the given couple (att, value) to the jdl (string value)
    def add_jdl_attribute(self, att, value=''):
   
        self.log_info('Add the attribute %s=\"%s\" to jdl'%(att,value))
        
        FILE=open(self.JDLFILE,"a")
        
        FILE.write("%s=\"%s\";\n"%(att,value))

        FILE.close()
        
        self.log_info('The new saved jdl is:\n%s'%(commands.getoutput("cat %s"%(self.JDLFILE))),'DEBUG')


    # add the given couple (att, value) to the jdl (not string value)
    def add_jdl_general_attribute(self, att, value):

        self.log_info('Add the attribute %s=%s to jdl'%(att,value))

        FILE=open(self.JDLFILE,"a")

        FILE.write("%s=%s;\n"%(att,value))

        FILE.close()

        self.log_info('The new saved jdl is:\n%s'%(commands.getoutput("cat %s"%(self.JDLFILE))),'DEBUG')


    # change value of the given attribute to the jdl (string value)
    def change_jdl_attribute(self, att, value):

        self.log_info('Change the value of the attribute %s to %s. '%(att,value))

        FILE=open(self.JDLFILE,"r")
        lines=FILE.readlines()
        FILE.close()

        for line in lines:
            if line.find(att)!=-1:
                lines[lines.index(line)]="%s=%s;\n"%(att,value)

        FILE=open(self.JDLFILE,"w")
        FILE.writelines(lines)
        FILE.close()

        self.log_info('The new saved jdl is:\n%s'%(commands.getoutput("cat %s"%(self.JDLFILE))),'DEBUG')


    # add given requirements to jdl
    def set_requirements(self, requirements):
        
        self.log_info('Add the attribute Requirements=%s to jdl'%(requirements))
        
        FILE=open(self.JDLFILE,"a")
        
        FILE.write("Requirements=%s;\n"%(requirements))
        
        FILE.close()
        
        self.log_info('The new saved jdl is:\n%s'%(commands.getoutput("cat %s"%(self.JDLFILE))),'DEBUG')


    # force the destination ce for parallel jobs
    def set_mpi_destination_ce(self,filename, destination_ce):
        
        self.set_requirements("Member (\"OPENMPI\",other.GlueHostApplicationSoftwareRunTimeEnvironment) && RegExp(\"%s\",other.GlueCEUniqueID);"%(destination_ce))

    # force the destination ce
    def set_destination_ce(self,filename, destination_ce):
        
        self.set_requirements("RegExp(\"%s\",other.GlueCEUniqueID)"%(destination_ce))


    #######################################################################################
    #######################################################################################

    ################################### JOB HANDLING ######################################

    # submit a job and return JOBID
    # Raise RunCommandError exception if submission fails
    def submit_job(self,jdl_file,delegation='',config=''):

        self.log_info('Submit a job')

        if len(delegation)==0:
            delegation=self.DELEGATION_OPTIONS   
             
        if len(config)==0:
            config=self.CONFIG_FILE   

        JOBID=self.run_command("glite-wms-job-submit %s --config %s --nomsg %s"%(delegation,config,jdl_file),0)
       
        self.log_info('Job submitted successfuly. Returned JOBID: %s'%(JOBID),'DEBUG')

        return JOBID


    def try_failure_submission(self,jdl_file,delegation='',config=''):

        self.log_info('Try a failure submission')

        if len(delegation)==0:
            delegation=self.DELEGATION_OPTIONS   
             
        if len(config)==0:
            config=self.CONFIG_FILE   

        com="glite-wms-job-submit %s --config %s --nomsg %s"%(delegation,config,jdl_file)

        args = shlex.split(com.encode('ascii'))

	p = subprocess.Popen( args , shell=False , stderr=subprocess.STDOUT , stdout=subprocess.PIPE )
	fPtr=p.stdout

        retVal=p.wait()

        output=fPtr.readlines()

	if retVal == 0:
           self.log_info('Submission not failed as expected. Submission output: %s'%(args,output))
           raise RunCommandError('Try failure submission','Submission not failed as expected. Submission output: %s'%(output))
                          
        self.log_info('Command successfully failed. Command output:\n%s'%(output),'DEBUG')
       
        return output



    # Wait until job "jobid" is done or raise TimeOutError exception if time is out 
    def wait_until_job_finishes(self,jobid):

        self.log_info('Wait until job %s finishes ...'%(jobid))

        self.log_info('Iterating %s times and each time wait for %s secs'%(self.NUM_STATUS_RETRIEVALS,self.SLEEP_TIME))

        counter=0
        
        while self.job_is_finished(jobid) == 0 :

            if counter >= int(self.NUM_STATUS_RETRIEVALS) :
                self.log_info("Timeout reached while waiting the job %s to finish"%(jobid))  
                raise TimeOutError("","Timeout reached while waiting the job %s to finish"%(jobid))
               
            self.log_info('*INFO* Job\'s %s status is %s ... sleeping %s seconds ( %s/%s )'%(jobid,self.JOBSTATUS,self.SLEEP_TIME,counter,self.NUM_STATUS_RETRIEVALS))
            time.sleep(int(self.SLEEP_TIME))
            counter=counter+1


    # Check if job described in JOBIDFILE is finished
    # returns 0 if job is not finished
    # returns 1 if job is DoneOK
    # returns 2 if Aborted
    # returns 3 if jobs is Cancelled
    # returns 4 if Done (exit Code != 0)
    # returns 5 if jobs is Cleared
    # returns 6 if Done (Failed)
    def job_is_finished(self,jobid):

        self.job_status(jobid)
        
        self.log_info('The status of the job %s is: %s'%(jobid,self.JOBSTATUS))

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
        elif self.JOBSTATUS.find('Done (Failed)') != -1 :
            return 6
        else:
            self.log_info('Job %s is not finished yet'%(jobid))
            return 0


    # Extract the "status" of the job "jobid"
    # --> set JOBSTATUS
    def job_status(self,jobid):

        self.JOBSTATUS="Unknown"

        self.log_info('Check job\'s status...')

        #try:
        OUTPUT=self.run_command("glite-wms-job-status --verbosity 0 %s"%(jobid))
        for line in OUTPUT.splitlines():
                if line.split(":",1)[0]=="Current Status":
                    self.JOBSTATUS=line.split(":",1)[1].strip()
                    break
      
        #except RunCommandError, e :
        #    print '*WARN* I\'m not able to retrieve job %s status. Error is %s'%(jobid,e.message)
        
        self.log_info('Job %s status is %s'%(jobid,self.JOBSTATUS))

        return 0


    def get_job_status(self,jobid):

          self.job_status(jobid)

          return self.JOBSTATUS



    # Wait until job is transfered to CE or raise TimeOutError exception if time is out
    def wait_until_job_transfered(self,jobid):

        self.log_info("Wait until job %s transfered to CE ..."%(jobid))

        self.log_info("Iterating %s times and each time wait for %s secs"%(self.NUM_STATUS_RETRIEVALS,self.SLEEP_TIME))

        counter=0

        while self.job_is_transfered(jobid) == 0 :

            if counter >= int(self.NUM_STATUS_RETRIEVALS) :
                self.error("Timeout reached while waiting the job %s to transfered to CE"%(jobid))
                raise TimeOutError("","Timeout reached while waiting the job %s to transfered to CE"%(jobid))

            self.log_info("Job's %s status is %s ... sleeping %s seconds ( %s/%s )"%(jobid,self.JOBSTATUS,self.SLEEP_TIME,counter,self.NUM_STATUS_RETRIEVALS))
            time.sleep(int(self.SLEEP_TIME))
            counter=counter+1
 

    # Check if job described in JOBIDFILE is transfered
    # returns 0 if job is not transfered
    # returns 1 if job is transfered
    def job_is_transfered(self,jobid):

        status=self.get_job_status(jobid)

        self.log_info('The status of the job %s is: %s'%(jobid,status))

        if status.find('Submitted') != -1 :
            self.log_info('Job %s is not transfered yet'%(jobid))
            return 0
        elif status.find('Ready') !=-1 :
            self.log_info('Job %s is not transfered yet'%(jobid))
            return 0
        elif status.find('Waiting') !=-1 :
            self.log_info('Job %s is not transfered yet'%(jobid))
            return 0
        else:
            self.log_info('Job %s is transfered'%(jobid))
            return 1


    def create_delegation(self,config_file,delegId):
        '''
                |  Description: |   Delegate user's proxy credentials,to be used later for job submissions. | \n
                |  Arguments:   |   config_file     |     the configuration file                             |
                |               |   delegId       |     the delegation id string                       | \n
                |  Returns:     |   nothing                                                                 |
        '''

        com="glite-wms-job-delegate-proxy -c %s -d %s"%(config_file,delegId)

        self.log_info('Execute command %s'%(com))

        OUTPUT=commands.getstatusoutput(com)

        if OUTPUT[0]!=0 :
            self.log_info("Delegation failed. Failure message: %s"%(OUTPUT[1]))
            raise RunCommandError("","Delegation failed. Failure message: %s"%(OUTPUT[1]))
            
        self.log_info('Command output:\n%s'%(OUTPUT[1]),'DEBUG')


    def get_ces_from_list_match(self,data):

        match_ces=[]

        for lines in data.splitlines():
            if lines.find(" - ") == 0:
                match_ces.append(lines[3:])
                
        return match_ces

       
    def get_job_output(self,jobid,output_dir): 
     
        com="glite-wms-job-output --dir %s --noint --nosubdir %s"%(output_dir,jobid)

        self.log_info('Execute command %s'%(com))

        OUTPUT=commands.getstatusoutput(com)

        if OUTPUT[0]!=0 :
            self.log_info("Command %s failed. Failure message: %s"%(com,OUTPUT[1]))
            raise RunCommandError("","Command %s failed. Failure message: %s"%(com,OUTPUT[1]))
            
        self.log_info('Command output:\n%s'%(OUTPUT[1]),'DEBUG')
        

    #Return the "status reason" of the job "jobid"
    def get_job_status_reason(self,jobid):

        self.log_info ("Check job's status...")

        reason='Unknown'

        OUTPUT=commands.getstatusoutput("glite-wms-job-status %s"%(jobid))

        if OUTPUT[0]!=0:
            self.log_info("Unable to retrieve job's %s status reason. Error message: %s"%(OUTPUT[1]))
            raise RunCommandError("","Unable to retrieve job's %s status reason. Error message: %s"%(OUTPUT[1]))
        
        for line in OUTPUT[1].splitlines():
                if line.split(":",1)[0]=="Status Reason":
                    reason=line.split(":",1)[1].strip()
                    break
        
        self.log_info('Job %s status reason is %s'%(jobid,reason))

        return reason


    # ... create proxy file with validity "valid_period" (default 24:00)
    def set_proxy(self,proxy,valid_period="24:00"):
     
	self.log_info("Initializing proxy file with voms %s, valid for %s"%(self.VO,valid_period))
        
	OUTPUT=commands.getstatusoutput("echo %s | voms-proxy-init -voms %s -verify -valid %s -bits 1024 -pwstdin -out %s "%(self.PROXY_PASSWORD,self.VO,valid_period,proxy))
      
        if OUTPUT[0] == 0 :
            self.log_info("voms-proxy-init output: %s"%(OUTPUT[1]),'DEBUG')
            os.putenv("X509_USER_PROXY",proxy)
            self.log_info("Set environment variable X509_USER_PROXY to %s"%(proxy))
        else:
            self.log_info("Failed to create a valid user proxy")
            self.log_info("voms-proxy-init output : %s"%(OUTPUT[1]),'DEBUG')
            raise GeneralError("Create proxy file","Failed to create a valid user proxy")


    # ... create proxy file with validity "valid_period" (default 24:00)
    def set_proxy_with_role(self,proxy,valid_period="24:00"):
     
        self.log_info("Initializing proxy file with voms %s, role %s, valid for %s"%(self.VO,self.ROLE,valid_period))

        OUTPUT=commands.getstatusoutput("echo %s | voms-proxy-init -voms %s:/%s/Role=%s -verify -valid %s -bits 1024 -pwstdin -out %s "%(self.PROXY_PASSWORD,self.VO,self.VO,self.ROLE,valid_period,proxy))

        if OUTPUT[0] == 0 :
            self.log_info("voms-proxy-init output: %s"%(OUTPUT[1]),'DEBUG')
            os.putenv("X509_USER_PROXY",proxy)
            self.log_info("Set environment variable X509_USER_PROXY to %s"%(proxy))
        else:
            self.log_info("Failed to create a valid user proxy")
            self.log_info("voms-proxy-init output : %s"%(OUTPUT[1]),'DEBUG')
            raise GeneralError("Create proxy file","Failed to create a valid user proxy")


    # ... delegate proxy and (re-)define DELEGATION_OPTIONS
    # --> set: DELEGATION_OPTIONS
    def define_delegation(self):

        self.DELEGATION_OPTIONS="-d del_%s"%(self.ID)
        self.log_info ("Delegating proxy ...")
        self.run_command("glite-wms-job-delegate-proxy %s -c %s"%(self.DELEGATION_OPTIONS,self.CONFIG_FILE))


  

    # Extract the destination CE of the job given as input 
    # return CENAME
    def get_CE(self,jobid):

        CENAME="Destination not available"

        self.log_info("Extract the destination CE of the job %s"%(jobid))

        OUTPUT=self.run_command("glite-wms-job-status %s"%(jobid))

        for line in OUTPUT.split("\n"):
            if line.find("Current Status:")!=-1:
                  STATUS=line.split("Current Status:")[1].strip(" \n\t")    
                  break

        while STATUS.find("Submitted") != -1 or STATUS.find("Waiting") != -1 :
            time.sleep(3)
            OUTPUT=self.run_command("glite-wms-job-status %s"%(jobid))
   
            for line in OUTPUT.split("\n"):
               if line.find("Current Status:")!=-1:
                  STATUS=line.split("Current Status:")[1].strip(" \n\t")    
                  break


        for line in OUTPUT.split("\n"):
               if line.find("Destination:")!=-1:
                    CENAME=line.split("Destination:")[1].strip(" \t\n")
                    break

        self.log_info("Destination CE is %s"%(CENAME))

        return CENAME


    # Extract the destination CE of the DAG job given as input 
    def get_dag_CE(self,jobid):

        CENAME="Destination not available"

        # Waiting until job is matched
        while True:
      
	  output=self.run_command("glite-wms-job-status %s"%(jobid)) 

	  if output.count("Destination")<=1: 
             time.sleep(30)  
          else:
             break
          
        for line in output.split("\n"):
           if line.find("Destination")!=-1 and line.find("dagman")==-1:
              CENAME=line.split("Destination:")[1].strip(" \t\n")
              break   


        self.log_info ("CE id is: %s"%(CENAME))

        return CENAME


    def get_cream_jobid(self,jobid):

       self.log_info("Get CREAM jobid")

       cream_jobid=""

       output=self.run_command("glite-wms-job-logging-info -v 2 --event Transfer %s"%(jobid)).split("\n")

       for line in output:
           if line.find("Dest jobid")!=-1 and line.find("https://")!=-1:
               cream_jobid=line.split("=")[1].strip(" \n\t")

       return cream_jobid

    #
    def get_cream_jdl(self,cream_jobid):

       self.log_info("Get CREAM jdl")

       jdl=""

       output=self.run_command("glite-ce-job-status -L 2  %s"%(cream_jobid)).split("\n")

       for line in output:
           if line.find("JDL")!=-1 :
               jdl=line.strip(" \n\t")

       return jdl


    #######################################################################################
    #######################################################################################

    ################################### RUN COMMANDS ######################################


    # Run command "args", if "fail" is set we expect a command failure (ret code != 0)
    # If command fails (or if "fail"=1 and it not fails), exit with failure 
    # returns command's output
    def run_command(self,args,fail=0):

        self.log_info('Run command: %s'%(args))

        OUTPUT=commands.getstatusoutput(args)

        
        if fail==0 and OUTPUT[0]!=0 :
            self.log_info('Command %s failed. Failure message: %s'%(args,OUTPUT[1]))
            raise RunCommandError('','Command %s failed. Failure message: %s'%(args,OUTPUT[1]))
        elif fail==1 and OUTPUT[0]==0:
            self.log_info('Command %s not failed as expected. Command output: %s'%(args,OUTPUT[1]))
            raise RunCommandError('','Command %s not failed as expected. Command output: %s'%(args,OUTPUT[1]))
                        
        self.log_info('Command output:\n%s'%(OUTPUT[1]),'DEBUG')
        
        if fail==0:
            self.log_info('Command success')
        else:
            self.log_info('Command successfully failed')

 
        return OUTPUT[1]
        


    def execute_list_match(self,delegation,config_file,jdl_file):
        '''
        '''

        args="/usr/bin/glite-wms-job-list-match %s --noint --config %s %s"%(delegation,config_file,jdl_file)

        self.log_info('Execute list match %s'%(args))

        OUTPUT=commands.getstatusoutput(args)

        if OUTPUT[0]!=0 :
            self.log_info("Command %s failed. Failure message: %s"%(args,OUTPUT[1]))
            raise RunCommandError("","Command %s failed. Failure message: %s"%(args,OUTPUT[1]))
            
        self.log_info('Command output:\n%s'%(OUTPUT[1]),'DEBUG')

        return OUTPUT[1]



    """ 
  
    

    ############### JOB UTILS ####################################

  
    #
 

    
  

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

    """
   


  

