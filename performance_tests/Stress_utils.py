import getopt
import os
import sys
import time
import re
import commands
import string
import random
import logging

from Exceptions import *
from time import strftime


class Stress_utils:

    """
        Implements Stress_utils object that has all the required attribues and methods to execute
        the WMS stress testing

    """

    def __init__(self,cmd,description):

        self.DESCRIPTION=description
        self.ID=''
        self.CMD=cmd
        self.CONF="stress.conf"
        self.LOG_LEVEL='INFO'
        self.DEFAULTREQ="other.GlueCEStateStatus == \"Production\""
        self.DELEGATION_OPTIONS="-a"
        self.USER_CONF=0
        self.NUM_LOG_LV=10
        self.VERBOSE=0
        self.EXTERNAL_REQUIREMENTS=0
        self.START_TIME=''
        self.WMS=''
        self.LB=''
        self.USERS=0
        self.USERNAMES=''
        self.VOS=''
        self.PASSWORDS=''
        self.MYPROXYSERVER=''
        self.REQUIREMENTS=''
        self.SLEEP_TIME_RANGE=[600,1200]
        self.TARGET_CES=''
        self.AUTOMATIC_DELEGATION=True
        self.ENABLE_RESUBMISSION=True
        self.PROXY_RENEWAL=True
        self.SLEEP_TIME=30
        self.TOTAL_JOBS=100
        self.JOB_TYPE='Collection'
        self.NODES_PER_JOB=20
        self.SUBMISSION_RATE=2
        self.PROXY_FILES=''
        self.TESTLOGFILE=''
        self.MYTMPDIR=''
        self.JDLFILE=''
        self.STATISTICS_FILE=''
        self.EXTERNAL_JDL = False
        self.JDL_FILE=''

    def usage(self,msg):

        """
            Print help message with all supported command line arguments 
        """

        print '\nUsage: '
        print ''
        print '%s [-h] [-v] [-d <level>] [-c <conf>] [-W <wms>] [-L <LB>] [-j <jdl file>] [-r <requirements>]'%(msg)
        print ''
        print " -h                  this help"
        print " -v                  print log messages to stdout"
        print " -d <level >         define log level (1=WARNING, 2=INFO, 3=DEBUG)"
        print " -c <conf>           configuration file"
        print " -W <wms>            WMS host"
        print " -L <LB>             LB host"
        print " -t <job type>       type of submitted jobs (normal,dag,parametric,collection)"
        print " -j <jdl file>       External jdl file"
        print " -r <requirement>    Set default jdl requirement"
        print ""

    #################################################################

    def get_WMS(self):
        return self.WMS

    def get_LB(self):
        return self.LB

    def get_VO(self):
        return self.VO

    def get_tmp_dir(self):
        return self.MYTMPDIR

    def get_jdl_file(self):
        return self.JDLFILE

    ###############################################################################


    def myecho(self,msg,type="default"):

        """
    	    Custom print method with various text colors
        """

        color_codes = { "info": "\033[1;34m" , "waring": "\033[1;33m" , "error": "\033[1;31m", "default":"" }

        if type=="default":
            print msg
            print ""
        else:
            print '\t' + color_codes[type] + msg + "\033[0m"
            print ""
            

    def error(self,msg):

        """
		    Log and print error messages. Error messages are always print to stdout
  	    """
               
        logging.error("%s"%(msg))
        self.myecho("ERROR: %s"%(msg),"error")


    def warn(self,msg):

        """
		    Log warning messages. Warning messages are print to stdout only if verbose = 1
        """

        logging.warning("%s"%(msg),"warning")
        if (self.VERBOSE) and (self.NUM_LOG_LV <= 30):
            self.myecho("WARNING: %s"%(msg))


    def info(self,msg):

        """
		    Log information messages. These messages are print to stdout only if verbose = 2
  	    """

        logging.info("%s"%(msg))
        if (self.VERBOSE) and (self.NUM_LOG_LV <= 20):
            self.myecho("%s"%(msg))


    def dbg(self,msg):

        """
		    Log debug messages. Debug messages are print to stdout only if verbose = 3
  	    """

        logging.debug("%s"%(msg))
        if (self.VERBOSE) and (self.NUM_LOG_LV == 10):
            self.myecho("DEBUG: %s"%(msg))


    def log_error(self,msg):

        """
            Write error messages to dedicated file error.log  which contains all the errors that occured 
            during the test execution
        """

        FILE=open("%s/errors.log"%(self.MYTMPDIR),"a")
        FILE.write("%s\n"%msg)
        FILE.close()


    def log_traceback(self,msg):

        """
            Write traceback messages to dedicated file traceback_error.log  which contains all the traceback 
		    messages from exceptions that occured during the test execution
        """

        FILE=open("%s/traceback_errors.log"%(self.MYTMPDIR),"a")
        FILE.write("%s\n"%msg)
        FILE.close()


    def print_stats(self,message):

        """
    	    Custom print method, used by manager process to print statistical messages to: 
            (a) stdout, (b) statistical file and (c) general log file
        """

        print message
        
        logging.info("%s"%(message))
        
        FILE = open(self.STATISTICS_FILE,"a")
        FILE.write("\n %s"%(message))
        FILE.close()


    # Warning exit: msg is the warning message
    # Exit code: 1
    def exit_warning(self,msg):

        """
            Warning exit during test execution
        """
        
        self.myecho ("")
        self.myecho ("Test: %s"%(self.CMD))
        self.myecho ("WMS: %s"%(self.WMS))
        self.myecho ("Started: %s"%(self.START_TIME))
        self.myecho ("Ended  : %s"%(strftime("%d/%m/%Y %H:%M:%S")))
        self.myecho ("")
        self.myecho ("  *** Warning: %s *** "%(msg))
        self.myecho ("")

        sys.exit(1)


    def exit_interrupt(self,signum,frame):

        """
            User interrupted exit ( Ctrl^C ) during test execution
        """

        self.exit_warning("Interrupted by user")


    def exit_failure(self,error_msg):

        """
            Failure exit during test execution
        """

        self.myecho ("")
        self.myecho ("Test: %s"%(self.CMD))
        self.myecho ("WMS: %s"%(self.WMS))
        self.myecho ("Started: %s"%(self.START_TIME))
        self.myecho ("Ended  : %s"%(strftime("%d/%m/%Y %H:%M:%S")))
        self.myecho ("")
        self.myecho ("    >>> TEST FAILED <<<")
        self.myecho ("")
        self.myecho (" >>> failure reason: %s <<< "%(error_msg))
        self.myecho ("")

        sys.exit(1)


    def exit_success(self):

        """
            Successful exit
        """		

        self.myecho ("")
        self.myecho ("Test: %s"%(self.CMD))
        self.myecho ("WMS: %s"%(self.WMS))
        self.myecho ("Started: %s"%(self.START_TIME))
        self.myecho ("Ended  : %s"%(strftime("%d/%m/%Y %H:%M:%S")))
        self.myecho ("")

        sys.exit(0)


    def set_jdl(self,filename):

        """
            Create the jdl file that will be used  during the stress testing
        """		

        job_type = self.JOB_TYPE.lower()

        if job_type.find("normal")!=-1 :
            self.set_normal_jdl(filename)
        elif job_type.find("dag")!=-1 :
            self.set_dag_jdl(filename)
        elif job_type.find("parametric")!=-1 :
            self.set_parametric_jdl(filename)
        elif job_type.find("collection")!=-1:
            self.set_collection_jdl(filename)
        else:
            self.exit_failure("Unsupported job type: %s"%(self.JOB_TYPE))


    def set_normal_jdl(self,filename):

        """
            Create the jdl file for a normal job type
        """		

        time_range=self.SLEEP_TIME_RANGE.replace("[","")
        time_range=time_range.replace("]","")
        values=time_range.split(",")

        requirements = [self.DEFAULTREQ]

        if len(self.REQUIREMENTS)>0:
            requirements.append(self.REQUIREMENTS)

        if len(self.TARGET_CES)>0:
            requirements.append(self.TARGET_CES)

        self.info("Define a normal jdl")

        FILE = open(filename,"w")

        FILE.write("JobType = \"Normal\";\n")
        FILE.write("Executable = \"/bin/hostname\";\n")
        FILE.write("Arguments = \"%s\";\n"%(int(random.uniform(int(values[0]),int(values[1])))))
        
        FILE.write("Requirements = %s;\n"%(" && ".join(requirements)));

        if self.ENABLE_RESUBMISSION == True:
            FILE.write("RetryCount = 3;\n");
        else:
            FILE.write("RetryCount = 0;\n");

        if self.PROXY_RENEWAL == True:
            FILE.write("MyProxyServer = \"%s\";\n"%(self.MYPROXYSERVER))
        else:
            FILE.write("MyProxyServer = \"\"; \n");

        FILE.close()

        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


    def set_collection_jdl(self,filename):

        """
            Create the jdl file for a collection job type
        """		

        time_range=self.SLEEP_TIME_RANGE.replace("[","")
        time_range=time_range.replace("]","")
        values=time_range.split(",")

        requirements = [self.DEFAULTREQ]

        if len(self.REQUIREMENTS)>0:
            requirements.append(self.REQUIREMENTS)

        if len(self.TARGET_CES)>0:
            requirements.append(self.TARGET_CES)

        self.info("Define a collection jdl")

        FILE = open(filename,"w")

        FILE.write("Type = \"collection\";\n")
        FILE.write("nodes = {\n")

        for i in range(int(self.NODES_PER_JOB)-1):
            FILE.write("[\n")
            FILE.write("NodeName=\"Node_%s_jdl\";\n"%(i+1));
            FILE.write("JobType = \"Normal\";\n")
            FILE.write("Executable = \"/bin/sleep\";\n")
            FILE.write("Arguments = \"%s\";\n"%(int(random.uniform(int(values[0]),int(values[1])))))
            FILE.write("],\n");

        FILE.write("[\n")
        FILE.write("NodeName=\"Node_%s_jdl\";\n"%(self.NODES_PER_JOB));
        FILE.write("JobType = \"Normal\";\n")
        FILE.write("Executable = \"/bin/sleep\";\n")
        FILE.write("Arguments = \"%s\";\n"%(int(random.uniform(int(values[0]),int(values[1])))))
        FILE.write("]\n");
        FILE.write("};\n");

        FILE.write("Requirements = %s;\n"%(" && ".join(requirements)));

        if self.ENABLE_RESUBMISSION == True:
            FILE.write("RetryCount = 3;\n");
        else:
            FILE.write("RetryCount = 0;\n");
            
        if self.PROXY_RENEWAL == True:
            FILE.write("MyProxyServer = \"%s\";\n"%(self.MYPROXYSERVER))
        else:
            FILE.write("MyProxyServer = \"\"; \n");

        FILE.close()

        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


    def set_dag_jdl(self,filename):

        """
            Create the jdl file for a DAG job type
        """		

        time_range = self.SLEEP_TIME_RANGE.replace("[","")
        time_range = time_range.replace("]","")
        values = time_range.split(",")

        node_names = []
        dependencies = []

        requirements = [self.DEFAULTREQ]

        if len(self.REQUIREMENTS)>0:
            requirements.append(self.REQUIREMENTS)

        if len(self.TARGET_CES)>0:
            requirements.append(self.TARGET_CES)

        self.info("Define a DAG jdl")

        FILE = open(filename,"w")

        FILE.write("Type = \"dag\";\n")
        
        FILE.write("nodes = [\n")

        for i in range(int(self.NODES_PER_JOB)):

            node_names.append("node_%s"%(i+1))
            
            FILE.write("node_%s = [\n"%(i+1))
            FILE.write("description = [\n")
            FILE.write("JobType = \"Normal\";\n")
            FILE.write("Executable = \"/bin/sleep\";\n")
            FILE.write("Arguments = \"%s\";\n"%(int(random.uniform(int(values[0]),int(values[1])))))
            FILE.write("];\n");
            FILE.write("];\n");
        
        FILE.write("];\n");

        if int(self.NODES_PER_JOB)%2 == 0:
            limit = int(self.NODES_PER_JOB)
        else:
            limit = int(self.NODES_PER_JOB)-1


        for i in range(0,limit,2):
            dependencies.append("{ %s , %s}"%(node_names[i],node_names[i+1]))

        FILE.write("Dependencies = { %s };\n"%(" , ").join(dependencies));

        FILE.write("Requirements = %s;\n"%(" && ".join(requirements)));

        if self.ENABLE_RESUBMISSION == True:
            FILE.write("RetryCount = 3;\n");
        else:
            FILE.write("RetryCount = 0;\n");

        if self.PROXY_RENEWAL == True:
            FILE.write("MyProxyServer = \"%s\";\n"%(self.MYPROXYSERVER))
        else:
            FILE.write("MyProxyServer = \"\"; \n");

        FILE.close()

        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


    def set_parametric_jdl(self,filename):

        """
            Create the jdl file for a parametric job type
        """		

        time_range = self.SLEEP_TIME_RANGE.replace("[","")
        time_range = time_range.replace("]","")
        values = time_range.split(",")

        requirements = [self.DEFAULTREQ]

        if len(self.REQUIREMENTS)>0:
            requirements.append(self.REQUIREMENTS)

        if len(self.TARGET_CES)>0:
            requirements.append(self.TARGET_CES)

        self.info("Define a parametric jdl")

        FILE = open(filename,"w")

        FILE.write("JobType = \"Parametric\";\n")
        FILE.write("Executable = \"/bin/sh\";\n")
        FILE.write("Arguments = \"script_PARAM_.sh\";\n")
        FILE.write("StdOutput = \"output_PARAM_.txt\";\n")
        FILE.write("StdError = \"error_PARAM_.txt\";\n")

        FILE.write("Parameters = %s;\n"%(self.NODES_PER_JOB))
        FILE.write("ParameterStart = 1;\n")
        FILE.write("ParameterStep = 1;\n")

        FILE.write("OutputSandbox = {\"error_PARAM_.txt\",\"output_PARAM_.txt\"};\n")
        FILE.write("InputSandbox = {\"/tmp/script_PARAM_.sh\"};\n")

        FILE.close()

        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))

        for i in range(int(self.NODES_PER_JOB)):

            FILE=open("/tmp/script%s.sh"%(i+1),"w")

            sleep_time = int(random.uniform(int(values[0]),int(values[1])))

            FILE.write("#!/bin/sh\n")
            FILE.write("echo \"##########################\"\n")
            FILE.write("echo \"This is a script\"\n")
            FILE.write("echo \"Start running at `date +%H:%M:%S`\"\n")
            FILE.write("echo \"Sleep for %s secs\"\n"%(sleep_time))
            FILE.write("sleep %s\n"%(sleep_time))
            FILE.write("echo \"Finish running at `date +%H:%M:%S`\"\n")
            FILE.write("echo \"##########################\"\n")

            FILE.close()


    def set_requirements(self):

        """
			Add to used jdl file requirements from configuration variables: DEFAULTREQ, REQUIREMENTS and TARGET_CES
		"""

        FILE=open(self.JDLFILE)
        lines=FILE.readlines()
        FILE.close()

        requirements=[self.DEFAULTREQ.replace(" ","")]

        if len(self.REQUIREMENTS)>0:
            requirements.append(self.REQUIREMENTS.replace(" ",""))

        if len(self.TARGET_CES)>0:
            requirements.append(self.TARGET_CES.replace(" ",""))

        edit=False

        for line in lines:
            if line.find("Requirements")!=-1 or line.find("requirements")!=-1 :
                edit=True
                break

        if edit:

            self.info("Edit attributed Requirements to jdl. Add requirements: %s"%(requirements))

            for line in lines:

                pattern = re.compile("requirements",re.IGNORECASE)
                result = pattern.sub("Requirements",line)
                
                if result.find("Requirements")!=-1:

                    line_index=lines.index(line)

                    line=line.replace(" ","")
                    line=line.replace("requirements","Requirements")

                    current_requirements=line.split("Requirements=")[1:]
                    
                    for current in current_requirements:
                        current=current.strip(" ;\n\t")
                        current=current.replace(" ","")
                        if current not in requirements :
                            requirements.append(current)

                    lines[line_index]="Requirements = %s;\n"%(" && ".join(requirements))

            FILE=open(self.JDLFILE,"w")
            FILE.writelines(lines)
            FILE.close()

        else:

            self.info("Add attribute Requirements=%s to jdl"%(requirements))

            FILE=open(self.JDLFILE,"a")
            FILE.write("Requirements = %s;\n"%(" && ".join(requirements)))
            FILE.close()

        self.dbg("Saved jdl is:\n%s"%(commands.getoutput("cat %s"%(self.JDLFILE))))


    def get_job_status(self,jobid):

        """
			Return the status for the job with the specified "jobid"
		"""

        status="Unknown"

        self.info ("Check job's status...")

        try:
            OUTPUT=self.run_command_continue_on_error ("glite-wms-job-status --verbosity 0 %s"%(jobid))
            for line in OUTPUT.splitlines():
                if line.split(":",1)[0]=="Current Status":
                    status=line.split(":",1)[1].strip()
                    break

        except RunCommandError, e :
            self.warn("I'm not able to retrieve job %s status. Error is %s"%(jobid,e.message))

        self.info('Job %s status is %s'%(jobid,status))

        return status


    def get_job_status_reason(self,jobid):

        """
			Return the status reason for the job with the specified "jobid"
		"""

        self.info ("Check job's status...")

        reason='Unknown'

        try:
            OUTPUT=self.run_command_continue_on_error ("glite-wms-job-status %s"%(jobid))
            for line in OUTPUT.splitlines():
                if line.find("Status Reason:")!=-1:
                    line=line.split("Status Reason:")
                    reason=line[1].strip(" \n\t")
                    break

        except RunCommandError, e :
            self.warn("I'm not able to retrieve job %s status reason. Error is %s"%(jobid,e.message))

        self.info('Job %s status reason is %s'%(jobid,reason))

        return reason


    def job_is_finished(self,jobid):

        """
			Check if the job with the specified "jobid" is finished
            
            Return values:

			- 0 if job is not finished
			- 1 if job is Done (Success)
			- 2 if Aborted
			- 3 if jobs is Cancelled
			- 4 if Done (exit Code != 0)
			- 5 if jobs is Cleared
			- 6 if job is Done (Failed)

		"""

        status=self.get_job_status(jobid)

        self.info('The status of the job %s is: %s'%(jobid,status))

        if status.find('Aborted') != -1 :
            return 2
        elif status.find('Cancelled') !=-1 :
            return 3
        elif status.find('(Exit Code !=0)') != -1 :
            return 4
        elif status.find('Cleared') != -1 :
            return 5
        elif status.find('Done (Success)') != -1 or status.find('Done(Success)') != -1 :
            return 1
        elif status.find('Done (Failed)') != -1 or status.find('Done(Failed)') != -1 :
            return 6
        else:
            self.info('Job %s is not finished yet'%(jobid))
            return 0


    def get_destination_ce(self,jobid):

        """
			Return the destination ce for the job with the specified "jobid"
		"""

        ce = None

        self.info("Extract the destination CE of the job %s"%(jobid))

        output = self.run_command_continue_on_error ("glite-wms-job-status %s"%(jobid))

        for line in output.split("\n"):
            if line.find("Destination:")!=-1:
                line=line.split("Destination:")
                ce = line[1].strip(" \t\n")
                break

        self.info("Destination CE is %s"%(ce))

        return ce

    
    def get_from_coumpound_job_all_nodes_ids(self,parent_jobid):

        """
			Return all the node ids for a compound job
		"""

        ids=[]

        self.info("Get all nodes ids for coumpound job: %s"%(parent_jobid))

        output=self.run_command_continue_on_error("glite-wms-job-status -v 0 %s"%(parent_jobid)).split("\n")

        for line in output:
            if line.find("Status info for the Job")!=-1 and line.find(parent_jobid)==-1:
                line=line.split("Status info for the Job :")
                ids.append(line[1].strip(" \n\t"))

        self.info("Node ids: %s"%(ids))

        return ids


    def run_command_continue_on_error(self,args,fail=0):

        """
             Execute command 'args', if fail is set method expects a command failure (ret code != 0)
             If command fails (or if fail=1 and it not fails), raise a RunCommandError exception
        """

        self.info("Run command: %s"%(args))

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


    def get_job_output_dir(self,user_index):

        """
            Create jobs output directory for the specified user
        """
       
        self.info("Create jobs output directory")

        directory = "/tmp/%s_%s_job_output/"%(self.ID,user_index)

        if not os.path.exists(directory):
            os.makedirs(directory)

        return directory

    
    def set_delegation(self,config_file):

        """
            Create delegation
        """

        self.info("Set delegation")

        if self.AUTOMATIC_DELEGATION == False:

            DELEGATIONID="deleg-%s"%(os.getpid())

            self.run_command_continue_on_error("glite-wms-job-delegate-proxy -c %s --delegationid %s"%(config_file,DELEGATIONID))

            return "-d %s"%(DELEGATIONID)

        else:
            return "-a"

    
    def set_conf(self,user_index,filename=""):

        """
            Create WMS configuration file
        """

        self.info("Create WMS configuration file")

        if len(filename)==0:
            filename = "/tmp/%s_%s_wms.conf"%(self.ID,user_index)
            
        FILE = open(filename,"w")

        FILE.write ("[\n")
        FILE.write ("  WMProxyEndPoints = {\"https://%s:7443/glite_wms_wmproxy_server\"};\n"%(self.WMS))
        FILE.write ("  LBAddresses= {\"%s\"};\n"%(self.LB))
        FILE.write ("  jdlDefaultAttributes = [\n")
        FILE.write ("    VirtualOrganisation = \"%s\";\n"%(self.VOS[user_index]))
        FILE.write ("    Requirements = %s ;\n"%(self.DEFAULTREQ))
        FILE.write ("    Rank =  -other.GlueCEStateEstimatedResponseTime;\n")
        FILE.write ("    SignificantAttributes = { \"Requirements\",\"Rank\" };\n")
        FILE.write ("  ]\n")
        FILE.write ("]\n")

        FILE.close()

        return filename
        

    def str2bool(self,value):

        """
            Convert a string value to boolean
        """

        return value.lower() in ["yes", "true", "t", "1"]


    def str2list(self,value):

        """
           Convert a string to python list object
        """

        result = []
        
        value=value.strip(" \n\t[]")

        values=value.split(",")

        for val in values:
            result.append(val.strip(" "))

        return result


    def load_configuration(self,conf):

       """
           Read configuration parameters from the test configuration file and set the appropriate variables at Stress_utils
           object
       """

       attributes=['WMS','LB','USERS','VOS','PASSWORDS','MYPROXYSERVER','LOG_LEVEL','REQUIREMENTS']
       attributes.extend(['JDL_FILE','EXTERNAL_JDL','AUTOMATIC_DELEGATION','SLEEP_TIME_RANGE','SLEEP_TIME'])
       attributes.extend(['TARGET_CES','DEFAULTREQ','TOTAL_JOBS','PROXY_RENEWAL','ENABLE_RESUBMISSION'])
       attributes.extend(['JOB_TYPE','NODES_PER_JOB','SUBMISSION_RATE','USERNAMES'])

       FILE = open(conf,"r")
       lines=FILE.readlines()
       FILE.close()

       for line in lines:

           if line.isspace()==False and line.find("#")==-1:
              line=string.strip(line)
              ret=line.split("=",1)

              ret[0]=string.strip(ret[0])
              ret[1]=string.strip(ret[1])
              
              if len(ret[1])>0:

                try:

                    attributes.index(ret[0])

                    if ret[0]=="EXTERNAL_JDL" or ret[0]=="AUTOMATIC_DELEGATION" or ret[0]=="ENABLE_RESUBMISSION" or ret[0]=="PROXY_RENEWAL" :
                       setattr(self,ret[0],self.str2bool(ret[1]))
                    elif ret[0]=="VOS" or ret[0]=="PASSWORDS" or ret[0]=="USERNAMES":
                       setattr(self,ret[0],self.str2list(ret[1]))
                    else:
                       setattr(self,'%s'%(ret[0]),ret[1])

                except ValueError:
                   pass


    def prepare(self,args):

        """
             Prepare test: parse command line arguments, load configuration variables, setup environement and create
             all required files
        """

        try:
            opts,args = getopt.getopt(args,'hvd:c:W:L:t:j:r:')
        except getopt.GetoptError,err:
            print ''
            print str(err)
            self.usage(self.CMD)
            sys.exit(0)

        self.ID=strftime("%Y%m%d%H%M%S")

        if os.path.isfile(self.CONF):
            self.load_configuration(self.CONF)
            
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

            elif option=="-c":
                self.USER_CONF=1
                self.CONF=value
            elif option =="-W":
                self.WMS=value
            elif option =="-L":
                self.LB=value
            elif option =="-t":
                self.JOB_TYPE=value
            elif option=="-j":
                self.EXTERNAL_JDL=True
                self.JDL_FILE=value
            elif option=="-r":
                self.DEFAULTREQ=value
                self.EXTERNAL_REQUIREMENTS=1

        self.START_TIME=strftime("%d/%m/%Y %H:%M:%S")

        if self.USER_CONF==1 and os.path.isfile(self.CONF):
            self.load_configuration(self.CONF)

        if self.LOG_LEVEL=='WARNING':
            self.NUM_LOG_LV=30
        elif self.LOG_LEVEL=='INFO':
            self.NUM_LOG_LV=20
        else:
            self.NUM_LOG_LV=10

        if len(self.WMS)==0 :
            self.exit_failure("Required parameter WMS is not set")

        if len(self.LB)==0 :
             self.exit_failure("Required parameter LB is not set")

        if len(self.USERS)==0 :
             self.exit_failure("Required parameter USERS is not set")

        if len(self.USERNAMES)==0 :
             self.exit_failure("Required parameter USERNAMES is not set")

        if len(self.VOS) != int(self.USERS) :
            self.exit_failure("Required parameter VOS is not set correctly")

        if len(self.PASSWORDS) != int(self.USERS) :
            self.exit_failure("Required parameter PASSWORDS is not set correctly")

        if len(self.USERNAMES) != int(self.USERS) :
            self.exit_failure("Required parameter USERNAMES is not set correctly")
            
        if len(self.JDL_FILE) == 0 and self.EXTERNAL_JDL == True :
            self.exit_failure("Required parameter JDL_FILE is not set")

        #create temporary directory
        self.MYTMPDIR="%s/WMS-Stress-Test_%s"%(os.getcwd(),self.ID)

        try:
            os.mkdir(self.MYTMPDIR,0755)
        except os.error, e:
            self.exit_failure("Fail to create temporary directory")
            return 0
          
        self.TESTLOGFILE='%s/Stress-Test_%s.log'%(self.MYTMPDIR, self.ID)
        
        logging.basicConfig(filename='%s'%(self.TESTLOGFILE),format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S',level=self.NUM_LOG_LV)

        self.info("Start log file for test %s"%(self.ID)) 

        self.myecho ("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        self.myecho ("+ Description: %s "%(self.DESCRIPTION))
        self.myecho ("+++++++++++++++++++++++++++++++++++++++++++++++++++++")

        self.STATISTICS_FILE="%s/statistics.txt"%(self.MYTMPDIR)

        if self.EXTERNAL_JDL == False :
            self.JDLFILE="/tmp/%s_example.jdl"%(self.ID)
        else :
            if os.path.isfile(self.JDL_FILE):
                os.system("cp %s /tmp/%s_%s"%(self.JDL_FILE,self.ID,self.JDL_FILE))
                self.JDLFILE="/tmp/%s_%s"%(self.JDL_FILE)
                self.set_requirements()
                os.system("cp %s %s/example.jdl"%(self.JDLFILE,self.MYTMPDIR))

            else:
                self.exit_failure("Unable to find file: %s"%(self.JDL_FILE))

        if self.EXTERNAL_JDL == False:

            #Set test jdl file
            self.set_jdl(self.JDLFILE)

            #Create copy at debug directory
            os.system("cp %s %s/example.jdl"%(self.JDLFILE,self.MYTMPDIR))
            
        #Create copies of configuration files at debug directory
        for i in range(len(self.VOS)):
            self.set_conf(i,"%s/%s_wms.conf"%(self.MYTMPDIR,i))


