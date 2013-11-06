import re
import os.path
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

##
def check_prologue_test_output(utils,jobid):

	status = utils.get_job_status(jobid)

	# Check job's final status	
	if status.find("Done(Success)")==-1:

		utils.log_info("TEST FAILS. Job finishes with status: %s cannot retrieve output"%(status))
		raise GeneralError("Check job final status","Job finishes with status %s cannot retrieve output"%(status))

	else:

		utils.run_command("glite-wms-job-output --dir %s --noint --nosubdir %s"%(utils.get_job_output_dir(),jobid))

		utils.log_info("Check if the output files are correctly retrieved")

		if( os.path.isfile("%s/prologue.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) ):

			utils.log_info("All output files are retrieved")

			# Check prologue output
			check_prologue(utils)

			# Check executable output
			check_stdout(utils,1)

			utils.log_info("Output files are as expected")

			## remove used files
			utils.remove("%s/prologue.sh"%(utils.get_tmp_dir()))
			utils.remove("%s/exe.sh"%(utils.get_tmp_dir()))
			os.system("rm -rf %s/*"%(utils.get_job_output_dir()))

		else:

			utils.log_info("TEST FAILS. Output files are not retrieved")
			raise GeneralError("Check the output files","Output files are not retrieved")

####
def check_epilogue_test_output(utils,jobid):

	status = utils.get_job_status(jobid)

	# Check job's final status	
	if status.find("Done(Success)")==-1:

		utils.log_info("TEST FAILS. Job finishes with status: %s cannot retrieve output"%(status))
		raise GeneralError("Check job final status","Job finishes with status %s cannot retrieve output"%(status))

	else:

		utils.log_info("Retrieve the output")

		utils.run_command("glite-wms-job-output --dir %s --noint --nosubdir %s"%(utils.get_job_output_dir(),jobid))

		utils.log_info("Check if the output files are correctly retrieved")

		if( os.path.isfile("%s/epilogue.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.out"%(utils.get_job_output_dir()))) :

			utils.log_info ("All output files are retrieved")

			# Check executable output
			check_stdout(utils)

			# Check epilogue output
			check_epilogue(utils)

			utils.log_info("Output files are as expected")

			## remove used files
			utils.remove("%s/epilogue.sh"%(utils.get_tmp_dir()))
			utils.remove("%s/exe.sh"%(utils.get_tmp_dir()))
			os.system("rm -rf %s/*"%(utils.get_job_output_dir()))

		else:
			utils.log_info("TEST FAILS. Output files are not retrieved")
			raise GeneralError("Check the output files","Output files are not retrieved")


###
def check_prologue_epilogue_test_output(utils,jobid):

	# Get job's final status	
	status = utils.get_job_status(jobid)
	
	if status.find("Done(Success)")==-1:

		utils.log_info("TEST FAILS. Job finishes with status: %s cannot retrieve output"%(status))
		raise GeneralError("Check job final status","Job finishes with status %s cannot retrieve output"%(status))

	else:

		utils.log_info("Retrieve the output")

		utils.run_command("glite-wms-job-output --dir %s --noint --nosubdir %s"%(utils.get_job_output_dir(),jobid))

		utils.log_info("Check if the output files are correctly retrieved")

		if( os.path.isfile("%s/prologue.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/std.out"%(utils.get_job_output_dir())) & os.path.isfile("%s/epilogue.out"%(utils.get_job_output_dir()))):

			utils.log_info("All output files are retrieved")

			# Check prologue output
			check_prologue(utils)

			# Check executable output
			check_stdout(utils,1)

			# Check epilogue output
			check_epilogue(utils,1)

			utils.log_info("Output files are as expected")

			## remove used files
			utils.remove("%s/prologue.sh"%(utils.get_tmp_dir()))
			utils.remove("%s/exe.sh"%(utils.get_tmp_dir()))
			utils.remove("%s/epilogue.sh"%(utils.get_tmp_dir()))
			os.system("rm -rf %s"%(utils.get_job_output_dir()))

		else:
			utils.log_info("TEST FAILS. Output files are not retrieved")
			raise GeneralError("Check the output files","Output files are not retrieved")

