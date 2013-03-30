#
# Bug: 82687
# Title: EMI WMS problems with ISB tar file handling
# Link: https://savannah.cern.ch/bugs/?82687
#
#

from lib.Exceptions import *


def run(utils):

    bug='82687'

    utils.log_info("Start regression test for bug %s"%(bug))

    utils.log_info("Prepare jdl file for submission")

    #Neccessary to avoid overwrite of the external jdls
    utils.use_external_jdl("%s.jdl"%(bug))    
    utils.add_jdl_attribute(utils.get_jdl_file(),"VirtualOrganisation","%s"%utils.VO)

    utils.log_info("Submit the job")

    JOBID=utils.run_command("glite-wms-job-submit %s --config %s --nomsg %s "%(utils.get_delegation_options(),utils.get_config_file(),utils.get_jdl_file()))

    utils.log_info("Wait until job finishes")

    utils.wait_until_job_finishes(JOBID)

    utils.log_info("Check job stauts")

    utils.job_status(JOBID)

    if utils.get_job_status().find("Done (Success)")!=-1:

        utils.log_info("Retrieve the output")

        utils.run_command("glite-wms-job-output --nosubdir --noint --dir %s %s "%(utils.get_job_output_dir(),JOBID))

        utils.log_info("Check if the output files are correctly retrieved")

        FILE=open("%s/ls.out"%(utils.get_job_output_dir()))
        lines=FILE.readlines()
        FILE.close()

        ok=0

        for line in lines:
           if line.find("82687.jdl")!=-1:
               ok=ok+1
           if line.find("supercalifragilistichespiralidose.txt")!=-1:
               ok=ok+1


        if ok==2:
            utils.log_info("Output files are collectly retrieved")
        else:
             logging.error("Test failed. Output files are not correctly retrieved")
             raise GeneralError("Check output files","Test failed. Output files are not correctly retrieved")
                

    else:
      logging.error("Job status is not 'Done (Success)', job failed to terminated successfully. Status reason %s"%(utils.get_StatusReason(JOBID)))
      raise GeneralError("Check job status","Job status is not 'Done (Success)' but %s. Status reason %s"%(utils.get_job_status(),utils.get_StatusReason(JOBID)))


    utils.log_info("End of regression test for bug %s"%(bug))
