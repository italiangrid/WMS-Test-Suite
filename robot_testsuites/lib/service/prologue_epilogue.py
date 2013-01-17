
import re

from Exceptions import *

# Check the correctness of the prologue output or raise GeneralError exception
def check_prologue(utils):

    utils.log_info("Check prologue output")
    FILE=open("%s/prologue.out"%(utils.get_job_output_dir()),"r")
    prolog=FILE.read()
    FILE.close()
    utils.log_info("Prologue output is: \n%s"%(prolog),'DEBUG')
    if ( prolog.find("Prologue Arguments") == -1 or 
         prolog.find("TestVariable") == -1 ):
        utils.log_info("TEST FAILS. Prologue output is not correct.")
        raise GeneralError("Check the output files","prologue.out is not correct.")
        
# Check the correctness of the std output or raise GeneralError exception
def check_stdout(utils, prolog=0):  

    utils.log_info("Check executable output")
    FILE=open("%s/std.out"%(utils.get_job_output_dir()),"r")
    exe=FILE.read()
    FILE.close()
    utils.log_info("Executable output is: \n%s"%(exe),'DEBUG')
    if ( exe.find("Executable Arguments") == -1 or 
         exe.find("TestVariable") == -1 or
         ( prolog and not len(re.findall("-rw-r--r-- .* prologue", exe)))):
        utils.log_info("TEST FAILS. Std output is not correct.")
        raise GeneralError("Check the output files","std.out is not correct.")           

# Check the correctness of the epilogue output or raise GeneralError exception
def check_epilogue(utils, prolog=0):  

    utils.log_info("Check epilogue output")
    FILE=open("%s/epilogue.out"%(utils.get_job_output_dir()),"r")
    epilogue=FILE.read()
    FILE.close()
    utils.log_info("Epilogue output is: \n%s"%(epilogue),'DEBUG')
    if ( epilogue.find("Epilogue Arguments") == -1 or 
         epilogue.find("TestVariable") == -1  or 
         ( prolog and not len(re.findall("-rw-r--r-- .* prologue", epilogue))) or
         not len(re.findall("-rw-r--r-- .* executable", epilogue))):
        utils.log_info("TEST FAILS. Epilogue output is not correct.")
        raise GeneralError("Check the output files","epilogue.out is not correct.")   
