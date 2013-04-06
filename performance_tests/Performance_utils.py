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


class Performance_utils:

    """
        Implements Performance_utils object that has all the required attribues and methods to execute
        the performance testing

    """

    def __init__(self,cmd,description):

        self.DESCRIPTION=description
        self.ID=''
        self.CMD=cmd
        self.CONF="performance.conf"
        self.LOG_LEVEL='INFO'
        self.DEFAULTREQ="other.GlueCEStateStatus == \"Production\""
        self.DELEGATION_OPTIONS="-a"
        self.USER_CONF=0
        self.NUM_LOG_LV=10
        self.VERBOSE=0
        self.EXTERNAL_REQUIREMENTS=0
        self.WMS=''
        self.VO=''
        self.LB=''
        self.MYPROXYSERVER=''
        self.START_TIME=''
        self.REQUIREMENTS=''
        self.NUM_STATUS_RETRIEVALS=-1
        self.SLEEP_TIME=30
        self.PASSWORD=''
        self.JDL_FILE=''
        self.EXTERNAL_JDL=False
        self.AUTOMATIC_DELEGATION=True
        self.SLEEP_TIME_RANGE=[600,1200]
        self.TOTAL_NUMBER_OF_NODES=500
        self.TARGET_CES=''
        self.PROXY=''
        self.TESTLOGFILE=''
        self.MYTMPDIR=''
        self.JDLFILE=''
        self.CONFIG_FILE=''
        self.STATISTICS_FILE=''

        
    def usage(self,msg):

        """
            Print help message with all supported command line arguments 
        """

        print '\nUsage: '
        print ''
        print '%s [-h] [-v] [-d <level>] [-c <conf>] [-W <wms>] [-L <LB>] [-V <VO] [-n <node numbers>] [-j <jdl file>] [-r <requirements>]'%(msg)
        print ''
        print " -h                  this help"
        print " -v                  print log messages to stdout"
        print " -d <level >         define log level (1=WARNING, 2=INFO, 3=DEBUG)"
        print " -c <conf>           configuration file"
        print " -W <wms>            WMS host"
        print " -L <LB>             LB host"
        print " -V <VO>             User VO"
        print " -n <node numbers>   Number of nodes in the compound job"
        print " -j <jdl file>       External jdl file"
        print " -r <requirement>    Set default jdl requirement"
        print ""

    ##########################################

	
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

    def get_config_file(self):
        return self.CONFIG_FILE

    def get_delegation_options(self):
        return self.DELEGATION_OPTIONS

    
	####################################################################

    def myecho(self,msg):

        """
    	    Custom print method
        """
        print "===> %s"%(msg)


    def error(self,msg):

        """
		    Log and print error messages. Error messages are always print to stdout
  	    """

        logging.error("%s"%(msg))
        self.myecho("ERROR: %s"%(msg))


    def warn(self,msg):

        """
		    Log warning messages. Warning messages are print to stdout only if verbose = 1
  	    """

        logging.warning("%s"%(msg))
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


    def print_statistics(self,msg):

        """
    	    Custom print method which print statistical messages to (a) stdout and (b) statistical file 
        """

        print msg
        os.system("echo %s >> %s "%(msg,self.STATISTICS_FILE))


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
            create the jdl file that will be used  during the performance testing
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

        for i in range(int(self.TOTAL_NUMBER_OF_NODES)-1):
            FILE.write("[\n")
            FILE.write("NodeName=\"Node_%s_jdl\";\n"%(i+1));
            FILE.write("JobType = \"Normal\";\n")
            FILE.write("Executable = \"/bin/sleep\";\n")
            FILE.write("Arguments = \"%s\";\n"%(int(random.uniform(int(values[0]),int(values[1])))))
            FILE.write("],\n");

        FILE.write("[\n")
        FILE.write("NodeName=\"Node_%s_jdl\";\n"%(self.TOTAL_NUMBER_OF_NODES));
        FILE.write("JobType = \"Normal\";\n")
        FILE.write("Executable = \"/bin/sleep\";\n")
        FILE.write("Arguments = \"%s\";\n"%(int(random.uniform(int(values[0]),int(values[1])))))
        FILE.write("]\n");
        FILE.write("};\n");

        FILE.write("Requirements = %s;\n"%(" && ".join(requirements)));

        FILE.close()

        self.dbg("The saved jdl is:\n%s"%(commands.getoutput("cat %s"%(filename))))


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
                        current=current.strip(" \n\t")
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
			Return the status of the job "jobid"
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
                if line.split(":",1)[0]=="Status Reason":
                    reason=line.split(":",1)[1].strip()
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


    def wait_until_job_finishes(self,jobid):

        """
            Wait until the specified job is finished or raise TimeOutError exception if time is out
        """

        self.info("Wait until job %s finishes ..."%(jobid))

        if int(self.NUM_STATUS_RETRIEVALS)==-1:
            self.info("Iteraring until job finished. Timeout disabled")
            print ""
            os.system("echo -e \"\\e[1;31m Iteraring until job finished. Timeout disabled \\e[0m\"")
            print ""
        else:
            self.info("Iterating %s times and each time wait for %s secs"%(self.NUM_STATUS_RETRIEVALS,self.SLEEP_TIME))
            print ""
            os.system("echo -e \"\\e[1;31m Iterating %s times and each time wait for %s secs \\e[0m\""%(self.NUM_STATUS_RETRIEVALS,self.SLEEP_TIME))
            print ""
            
        counter=0

        while self.job_is_finished(jobid) == 0 :

            if int(self.NUM_STATUS_RETRIEVALS)!=-1 and counter >= int(self.NUM_STATUS_RETRIEVALS) :
                self.error("Timeout reached while waiting the job %s to finish"%(jobid))
                raise TimeOutError("","Timeout reached while waiting the job %s to finish"%(jobid))

            status=self.get_job_status(jobid)

            self.info("Job's %s status is %s ... sleeping %s seconds ( %s/%s )"%(jobid,status,self.SLEEP_TIME,counter,self.NUM_STATUS_RETRIEVALS))
            print ""
            os.system("echo -e \"\\e[1;34m Job's %s status is %s ... sleeping %s seconds ( %s/%s ) \\e[0m\""%(jobid,status,self.SLEEP_TIME,counter,self.NUM_STATUS_RETRIEVALS))
            print ""
            time.sleep(int(self.SLEEP_TIME))
            counter=counter+1


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


   
    def set_proxy(self,proxy,valid_period="24:00"):

        """
            Create a proxy file with validity "valid_period" (default 24:00)
        """

        self.info("Initializing proxy file with voms %s, valid for %s"%(self.VO,valid_period))
        OUTPUT=commands.getstatusoutput("echo %s | voms-proxy-init -voms %s -verify -valid %s -bits 1024 -pwstdin -out %s "%(self.PASSWORD,self.VO,valid_period,proxy))
        
        if OUTPUT[0] == 0 :
            self.dbg("voms-proxy-init output: %s"%(OUTPUT[1]))
            os.putenv("X509_USER_PROXY",proxy)
            self.info("Set environment variable X509_USER_PROXY to %s"%(proxy))
        else:
            logging.critical("Failed to create a valid user proxy")
            self.error("voms-proxy-init output : %s"%(OUTPUT[1]))
            self.exit_failure("Failed to create a valid user proxy")


    def set_conf(self,filename):

        """
            Create a WMS configuration file
        """

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


    def str2bool(self,value):

        """
            Convert a string value to boolean
        """

        return value.lower() in ["yes", "true", "t", "1"]

    
    def load_configuration(self,conf):

       """
           Read configuration parameters from the test configuration file and set the appropriate variables 
           at Performance_utils object
       """

       attributes=['WMS','LB','VO','MYPROXYSERVER','LOG_LEVEL','REQUIREMENTS','NUM_STATUS_RETRIEVALS','SLEEP_TIME']
       attributes.extend(['PASSWORD','JDL_FILE','EXTERNAL_JDL','AUTOMATIC_DELEGATION','SLEEP_TIME_RANGE'])
       attributes.extend(['TOTAL_NUMBER_OF_NODES','TARGET_CES','DEFAULTREQ'])

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

                    if ret[0]=="EXTERNAL_JDL" or ret[0]=="AUTOMATIC_DELEGATION":
                       setattr(self,'%s'%(ret[0]),self.str2bool(ret[1]))
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
            opts,args = getopt.getopt(args,'hvd:c:W:L:V:n:j:r:')
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
            elif option =="-V":
                self.VO=value
            elif option =="-n":
                self.TOTAL_NUMBER_OF_NODES=value
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

        if len(self.VO)==0 :
            self.exit_failure("Required parameter VO is not set")

        if len(self.PASSWORD)==0 :
            self.exit_failure("Required parameter PASSWORD is not set")

        if len(self.JDL_FILE) == 0 and self.EXTERNAL_JDL == True :
            self.exit_failure("Required parameter JDL_FILE is not set")

        #create temporary directory
        self.MYTMPDIR="%s/WMS-Performance-Test_%s"%(os.getcwd(),self.ID)

        try:
            os.mkdir(self.MYTMPDIR,0755)
        except os.error, e:
            self.exit_failure("Fail to create temporary directory")
            return 0
          
        self.TESTLOGFILE='%s/Performance-Test_%s.log'%(self.MYTMPDIR, self.ID)
        
        logging.basicConfig(filename='%s'%(self.TESTLOGFILE),format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S',level=self.NUM_LOG_LV)

        self.info("Start log file for test %s"%(self.ID)) 

        self.myecho ("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        self.myecho ("+ Description: %s "%(self.DESCRIPTION))
        self.myecho ("+++++++++++++++++++++++++++++++++++++++++++++++++++++")

        self.PROXY="%s/proxy.file"%(self.MYTMPDIR)
        self.CONFIG_FILE="%s/wms.conf"%(self.MYTMPDIR)
        self.STATISTICS_FILE="%s/statistics.txt"%(self.MYTMPDIR)

        if self.EXTERNAL_JDL == False :
            self.JDLFILE="%s/example.jdl"%(self.MYTMPDIR)
        else :
            if os.path.isfile(self.JDL_FILE):
                os.system("cp %s %s/%s"%(self.JDL_FILE,self.MYTMPDIR,self.JDL_FILE))
                self.JDLFILE="%s/%s"%(self.MYTMPDIR,self.JDL_FILE)
                self.set_requirements()
            else:
                self.exit_failure("Unable to find file: %s"%(self.JDL_FILE))

        if self.EXTERNAL_JDL == False:
            self.set_jdl(self.JDLFILE)

        self.set_conf(self.CONFIG_FILE)

        self.info("Check for voms proxy ...")

        voms_info=commands.getstatusoutput("voms-proxy-info -timeleft")

        if voms_info[1].isdigit() == False or int(voms_info[1])==0 :

            self.info("Unable to find a valid voms proxy , try to create a new ....")

            self.set_proxy(self.PROXY) 

            voms_info=commands.getstatusoutput("voms-proxy-info -timeleft")
            
            if voms_info[1].isdigit() == False :
                self.exit_failure("I don't find neither create any valid proxy")

        if self.AUTOMATIC_DELEGATION == False:

            DELEGATIONID="deleg-%s"%(os.getpid())

            self.run_command_continue_on_error("glite-wms-job-delegate-proxy -c %s --delegationid %s"%(self.get_config_file(),DELEGATIONID))

            self.DELEGATION_OPTIONS="-d %s"%(DELEGATIONID)

        else:
            self.DELEGATION_OPTIONS="-a"
